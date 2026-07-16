Real-Time Face Mask Detection using YOLO
Overview

This project implements a real-time face mask detection system using the YOLO object detection model. It supports both image-based inference through Hugging Face and live webcam detection using OpenCV.

When a person without a face mask is detected, the system automatically:

Captures an image.
Records the detection timestamp.
Sends an email notification with the captured image to the responsible person.
Features
Real-time webcam detection.
Image inference via Hugging Face.
Face mask classification.
Automatic email alerts.
Image capture with timestamp.
Fast inference using YOLO.
Technologies
Python
YOLO
OpenCV
Deep Learning
Computer Vision
SMTP (Email Notification)
Hugging Face
