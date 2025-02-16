import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import './style.css';

// Connect to the backend Socket.IO server (adjust the URL if needed)
const socket = io('http://localhost:5001');

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [blinkText, setBlinkText] = useState('');

  useEffect(() => {
    // Request webcam access and stream to the video element
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      })
      .catch((err) => {
        console.error("Error accessing webcam: ", err);
      });

    // Listen for blink text events from the backend
    socket.on('blinkText', (data) => {
      setBlinkText(prev => prev + data.letter);
    });

    // Set an interval to capture frames from the video and send them to the backend
    const interval = setInterval(() => {
      captureFrame();
    }, 200); // Capture a frame every 200ms

    // Cleanup on unmount
    return () => {
      clearInterval(interval);
      socket.off('blinkText');
    };
  }, []);

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video && canvas) {
      const ctx = canvas.getContext('2d');
      // Ensure canvas dimensions match the video dimensions
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      // Convert the current canvas image to a JPEG data URL
      const imageData = canvas.toDataURL('image/jpeg');
      // Emit the frame to the backend via Socket.IO
      socket.emit('frame', { image: imageData });
    }
  };

  return (
    <div className="App">
      <h1>Facial Blink-to-Text Conversion</h1>
      <div className="video-container">
        <video ref={videoRef} className="video" autoPlay muted></video>
        {/* The canvas is hidden; it is only used to capture video frames */}
        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
      </div>
      <div className="text-display">
        <h2>Converted Text:</h2>
        <p>{blinkText}</p>
      </div>
    </div>
  );
}

export default App;

