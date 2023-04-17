import firebase_admin
from firebase_admin import credentials,storage

import numpy as np
import cv2

cred = credentials.Certificate('C:\\Users\\praty\\PycharmProjects\\fish_size_detection\\key.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'fir-storageproject-2999f.appspot.com'})


def image_extractor():
    bucket = storage.bucket()
    blob = bucket.get_blob("phone_aruco_marker.jpg")
    arr = np.frombuffer(blob.download_as_string(),np.uint8)
    # img = cv2.imdecode(arr,cv2.COLOR_BGR2BGR555)
    #
    #
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    return arr