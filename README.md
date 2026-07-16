# Real-Time Face Mask Detection using YOLO

A computer vision project that detects whether people are wearing face masks using the YOLO object detection model.

The system supports two modes:
- Image detection through Hugging Face interface.
- Real-time detection using a laptop webcam.

When a person without a mask is detected, the system captures an image, records the detection time, and sends an email alert with the captured image to the responsible person.

## Technologies
Python • YOLO • OpenCV • Computer Vision • Deep Learning • Hugging Face • SMTP

## Screenshots

### Hugging Face Image Detection
![Hugging Face](screenshots/huggingface-test.png)

### Real-Time Webcam Detection
![Webcam](screenshots/webcam-detection.png)

### Email Alert
![Email Alert](screenshots/email-alert.jpg)


Face-Mask-Detection-YOLO/
│
├── app.py
├── best.pt
├── requirements.txt
│
├── huggingface/
│   ├── app
│   ├── app.py
│   ├── best.pt
│   └── requirements.txt
│
├── screenshots/
│
└── README.md



## Screenshots

### Hugging Face Image Detection

![Hugging Face Detection](screenshots/huggingface-test.png)

### Real-Time Webcam Detection

![Webcam Detection](screenshots/live_test.jpg)

### Email Notification

![Email Alert](screenshots/email-alert.png)

## Author

Anas Al-Awadhi
