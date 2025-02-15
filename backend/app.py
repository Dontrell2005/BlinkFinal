from flask import Flask
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np
import tensorflow as tf  # In production, use TensorFlow for your CNN model
import random

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
    if random.random() < 0.05:
        return True
    return False

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

    # Run the (dummy) blink detector on the frame
    if detect_blink(frame):
        # For demonstration, map a detected blink to the letter "A"
        letter = 'A'
        emit('blinkText', {'letter': letter})
    # In a real implementation, you might accumulate blink sequences and then convert them to words

if __name__ == '__app__':
    # Using eventlet for async support; you can also use gevent.
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


