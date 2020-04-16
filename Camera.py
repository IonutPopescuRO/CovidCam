#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from keras.preprocessing.image import ImageDataGenerator 
from keras.models import load_model
from keras import backend as K 
import time
from PIL import Image
from keras.preprocessing import image

import pandas as pd
import math
import random

import firebase_admin
from firebase_admin import credentials, firestore, storage

import pyrebase

img_width, img_height = 110, 110
validation_data_dir = 'saved/'
batch_size = 64

test_datagen = ImageDataGenerator(rescale = 1. / 255) 

if K.image_data_format() == 'channels_first': 
    input_shape = (3, img_width, img_height) 
else: 
    input_shape = (img_width, img_height, 3) 



model = load_model('model_saved.h5')

config = {
    "apiKey": "AIzaSyCE_8CVn1Zio1f-EXpEgZtp-8aoyxpteVk",
    "authDomain": "bestcamera-7e901.firebaseapp.com",
    "databaseURL": "https://bestcamera-7e901.firebaseio.com/",
    "projectId": "bestcamera-7e901",
    "storageBucket": "bestcamera-7e901.appspot.com",
    "messagingSenderId": "1087271452402",
    "appId": "1:1087271452402:web:9c34a3417a21237ebe5a6b",
    "measurementId": "G-3J20J96NZX"

  };


firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
add = random.randrange(9999999)
faceURL = "imagine/dumi" + str(add) + ".jpg"
path_local = "./saved/face/img.jpg"
imgurl = storage.child(faceURL).put(path_local)
db = firebase.database()
     
camera = cv2.VideoCapture(-1)
_, frame = camera.read()
camera.release()
time.sleep(1)   

while True:
    camera = cv2.VideoCapture(-1)
    _, frame = camera.read()
    camera.release()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    
    print("[INFO] Found {0} Faces.".format(len(faces)))
    
    for (x, y, w, h) in faces:
       # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = frame[y:y + h, x:x + w]
        print("[INFO] Object found. Saving locally.")
        cv2.imwrite('saved/face/faces.jpg', roi_color)
    
    cv2.imwrite('saved/face/img.jpg', frame)
    time.sleep(4)
    test_generator = test_datagen.flow_from_directory(
        directory=validation_data_dir,
        target_size=(img_width, img_height),
        color_mode="rgb",
        batch_size=64,
        class_mode=None,
        shuffle=False
    )
    
    test_generator.reset()
    pred=model.predict_generator(test_generator,verbose=1,steps=1)
    pred = pred + 0.1
    
    predicted_class_indices = [math.floor(x) for x in pred]
    labels = (test_generator.class_indices)
    labels = dict((v,k) for k,v in labels.items())
    predictions = [labels[k] for k in predicted_class_indices]
    
    filenames=test_generator.filenames
    results=pd.DataFrame({"Filename":filenames,
                          "Predictions":predictions})

    temp = random.randrange(36,40)
    risk = (abs(predicted_class_indices[0] - 1) + ((temp-36) / 4) ) / 2;
    
    if predictions[0] == 'face':
        cv2.putText(frame, "Nu porti masca.", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.putText(frame, str(risk), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    else:
        cv2.putText(frame, "Porti masca.", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.putText(frame, str(risk), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    
    
    if risk >= 0.5:
        
        storage = firebase.storage()
        add = random.randrange(9999999)
        faceURL = "imagine/dumi" + str(add) + ".jpg"
        path_local = "./saved/face/img.jpg"
        imgurl = storage.child(faceURL).put(path_local)
        fever = str(temp)
        seen = "0"
        if predictions[0] == 'face':
            initials = "Nu are masca"
        else:
            initials = "Are masca"
        
        danger_level = "Ai riscul: " + str(risk)
        
        storage = firebase.storage()
        
        #imgurl=storage.child(faceURL).put("1.jpg")
        img_url=storage.child(faceURL).get_url(imgurl['downloadTokens'])
        
        data = {
        	"faceURL" : img_url,
        	"febra" : fever,
        	"initials": initials,
        	"pericol" : danger_level
        }
        
        db.child("jale").push(data)

    
    cv2.imshow("Test", frame)
    key=cv2.waitKey(1)
    time.sleep(3)
    if key == 27:# ESC
        break

camera.release()
cv2.destroyAllWindows()