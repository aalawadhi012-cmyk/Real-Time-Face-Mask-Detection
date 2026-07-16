import cv2
import threading
import time
import winsound
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os

# ================== إعداد نموذج YOLO ==================
model = YOLO("best.pt") 
class_names = ["No Mask", "Mask"]

# ================== إعداد الكاميرا ==================
cap = cv2.VideoCapture(0)

# ================== تنبيه صوتي ==================
alarm_on = False

def play_alarm():
    global alarm_on
    while True:
        if alarm_on:
            winsound.Beep(1000, 500)
        else:
            time.sleep(0.1)

threading.Thread(target=play_alarm, daemon=True).start()

# ================== إعداد البريد الإلكتروني ==================
sender_email = "aalawadhi012@gmail.com"
#maafer.it2009@gmail.com
#osamh16760@gmail.com
receiver_email = "aalawadhi012@gmail.com"
app_password = "qidz bvsr zbnd gjhh"  
subject = "تنبيه الكمامة"


os.makedirs("no_mask_shots", exist_ok=True)

EMAIL_COOLDOWN = 4
last_email_time = 0.0
send_lock = threading.Lock()  

def send_email_alert_async(image_path, timestamp_str):
    def worker(img, ts):
        try:
            body_text = f"عزيزي، هناك شخص دخل بدون كمامه.\n\nالتاريخ والوقت: {ts}"
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            with open(img, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(img)}")
                msg.attach(part)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"[+] Email sent at {ts} -> {os.path.basename(img)}")
        except Exception as e:
            print("Error sending email:", e)

    t = threading.Thread(target=worker, args=(image_path, timestamp_str), daemon=True)
    t.start()

# ================== الحلقة الرئيسية ==================
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        alarm_on = False

        now = time.time()
        detected_no_mask = False

        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            conf = float(result.conf[0]) * 100
            cls = int(result.cls[0])
            label = f"{class_names[cls]} {conf:.1f}%"

            if class_names[cls] == "No Mask":
                color = (0, 0, 255)
                alarm_on = True
                detected_no_mask = True

                if now - last_email_time >= EMAIL_COOLDOWN:
                    with send_lock:
                        last_email_time = time.time()
                        timestamp = datetime.datetime.now()
                        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        image_name = f"no_mask_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
                        image_path = os.path.join("no_mask_shots", image_name)
                        cv2.imwrite(image_path, frame)
                        send_email_alert_async(image_path, timestamp_str)
            else:
                color = (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Mask Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
