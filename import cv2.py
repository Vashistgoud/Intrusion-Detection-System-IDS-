import cv2
from cvzone.PoseModule import PoseDetector
from twilio.rest import Client

# Initialize Pose Detector
detector = PoseDetector()

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

# List to track detections and flag for SMS
l = []
flag = True

# Twilio account SID and authentication token
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# Send SMS function
def send_sms():
    try:
        message = client.messages.create(
            to='',  # Recipient phone number
            from_='',  # Your Twilio phone number
            body="Human detected in the area! Please check the camera feed.")
        print(f"SMS Sent! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image. Retrying...")
        continue  # If frame is not captured, retry
    
    # Detect pose in the image
    img = detector.findPose(img)
    imlist, bbox = detector.findPosition(img)

    # If a human is detected
    if len(imlist) > 0:
        print("Human Detected")
        l.append(1)
    
    # If a human is detected more than 50 times, send SMS once
    if len(l) > 50 and flag:
        flag = False
        send_sms()  # Call the SMS function
    
    # Show the video feed
    cv2.imshow("Output", img)
    
    # Break loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        print("Exiting program...")
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
