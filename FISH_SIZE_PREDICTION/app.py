from flask import Flask,request,jsonify
import cv2
from object_detector import *
import numpy as np
from image_from_firebase import image_extractor




app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict')
def predict():
    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
    # Load Object Detector
    detector = HomogeneousBgDetector()
    arr = image_extractor()
    # load image fom firebase
    img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    # print(corners)
    # Draw polygon around the marker
    int_corners = np.int0(corners)
    cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

    # Aruco Perimeter
    aruco_perimeter = cv2.arcLength(corners[0], True)
    print(aruco_perimeter)

    # Pixel to cm ratio
    pixel_cm_ratio = aruco_perimeter / 20

    contours = detector.detect_objects(img)

    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

    result = {"Object_width":object_width,
              "Object_length":object_height}

    return jsonify(result)

if __name__ =="__main__":
    app.run(debug=True)