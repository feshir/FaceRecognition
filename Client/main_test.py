import os
import glob
import face_recognition
import json
import numpy as np
import requests
import pandas as pd
from Models import *
import codecs

df=pd.DataFrame(columns=['filename','result'])

images='test'
jpg_filepaths=glob.glob(os.path.join(images,'*.jpg'))

jpg_filepaths=sorted(jpg_filepaths)

url="https://facerecognitiondbapi20201027214040.azurewebsites.net/employers"

Data=GetFullData(url);


list_encodings=[]

list_names=[]

for j in Data:
    list_encodings.append(j["features"])
    list_names.append(j["name"])

information=[]
anotations=glob.glob(os.path.join(images,'*.txt'))
anotations=sorted(anotations)

for filepath in anotations:    
    with codecs.open(filepath,encoding='utf-8') as myfile:
        mini=[]
        for line in myfile:
            line=line[:-1]
            mini.append(line)
    information.append(mini)

cindex=0;

for filepath in jpg_filepaths:
    image=face_recognition.load_image_file(filepath)
    info=sorted(information[cindex])
    try:
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)      

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        df.loc[cindex]={'filename':filepath,'result':0}
        cindex=cindex+1
        continue
    print(f"File {filepath}")

    faces=[]
    faceCounts=len(info)
    count=0
    for face_encoding in face_encodings:
        results = face_recognition.compare_faces(list_encodings, face_encoding)
        face_distances = face_recognition.face_distance(list_encodings,face_encoding)
        best_match_index=np.argmin(face_distances)
        if (results[best_match_index]):
            person=Data[best_match_index]["name"]
            print(f'This is {person}')
            for i in info:
                if i==person:
                    count=count+1;
                    info.remove(person)
            faces.append(person)    
    count=count/faceCounts
    df.loc[cindex]={'filename':filepath,'result':count}
 
    cindex=cindex+1
    print("End")

print(df.head())
df.to_csv('Tests')