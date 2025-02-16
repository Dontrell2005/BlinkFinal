from flask import Flask
from flask_socketio import SocketIO, emit
import base64
import cv2
import mediapipe as mp
from PIL import Image
import numpy as np
import tensorflow as tf  # In production, use TensorFlow for your CNN model
import random

mp_face_detection = mp.solutions.face_detection


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# In a real implementation, load your pre-trained CNN model here.
# model = tf.keras.models.load_model('path_to_your_model.h5')

def detect_blink(frame):
    """
    Dummy blink detector.
    In production, preprocess the frame, extract features/landmarks,
    and run your CNN to detect blink characteristics.
    """
    # Simulate a blink with a random chance (e.g., 5% chance per frame)
    
    second_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_detection.FaceDetection(min_detection_confidence=0.5).process(second_frame)

    if not results.detections:
        return False

    # print([direction for direction in results.directions])
    return True

@socketio.on('frame')
def handle_frame(data):
    """
    Receives a frame from the frontend, decodes the image,
    runs blink detection, and if a blink is detected, emits a letter.
    """
    img_data = data.get('image', '')
    if not img_data:
        return

    # Remove the header if present (e.g., "data:image/jpeg;base64,")
    if ',' in img_data:
        img_data = img_data.split(',')[1]

    # Decode the base64 string to bytes
    img_bytes = base64.b64decode(img_data)
    # Convert bytes to a NumPy array and decode into an image
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    Image.fromarray(frame).save('frame.jpg')
    # print("hello")
    
    # Run the (dummy) blink detector on the frame
    if detect_blink(frame):
        # For demonstration, map a detected blink to the letter "A"
        letter = 'A'
        emit('blinkText', {'letter': letter})
    # In a real implementation, you might accumulate blink sequences and then convert them to words

if __name__ == '__main__': # when we change it to __app__
    # Using eventlet for async support; you can also use gevent.
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)


