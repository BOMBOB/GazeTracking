

import cv2
import numpy as np
import dlib
import os
class CaffeModel(object):
    def __init__(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        trainmodel = os.path.abspath(os.path.join(cwd, "facedetector/deploy.prototxt"))
        facedetect = os.path.abspath(os.path.join(cwd, "facedetector/res10_300x300_ssd_iter_140000_fp16.caffemodel"))
        self.net = cv2.dnn.readNetFromCaffe(trainmodel,
                               facedetect)

    def _analyze(self, inputframe):
        net = self.net
        frame = inputframe.copy()
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),  # the fixed-size input image
                                     1.0,  # scaleFactor
                                     (300, 300),  # spatial size of the CNN
                                     (104.0, 177.0, 123.0))  # mean subtraction values

        # Pass the blob to the network
        net.setInput(blob)
        detections = net.forward()

        # Loop over the resultant detections
        for i in range(0, detections.shape[2]):
            # Extract the confidence (i.e., probability)
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections by ensuring the confidence is greater than the threshold
            if confidence < 0.5:
                continue

            # Compute the (x, y)-coordinates of the bounding box
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')

            # Draw the bounding box of the face with the associated probability
            #text = '{:.2f}%'.format(confidence * 100)
            #y = startY - 10 if startY - 10 > 10 else startY + 10
            # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
            # cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            return dlib.rectangle(startX,startY, endX, endY)
