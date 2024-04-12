import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "attendance-48364.appspot.com"
})

bucket = storage.bucket()

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    imgList.append(img)
    student_id = os.path.splitext(path)[0]
    studentIds.append(student_id)

    file_name = f'{folderPath}/{path}'
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img_rgb)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file_path = "EncodeFile.p"
with open(file_path, 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("File Saved")
