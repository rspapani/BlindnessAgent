import React, { useEffect, useRef } from 'react';
import axios from 'axios';

const WebcamCapture = () => {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    async function setupWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          setupMediaRecorder(stream);
        }
      } catch (err) {
        console.error("Failed to get media devices:", err);
      }
    }

    function setupMediaRecorder(stream) {
      if (!stream.active) return;
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = event => {
        audioChunksRef.current.push(event.data);
      };
      mediaRecorderRef.current.onstop = sendAudioToServer;
    }

    setupWebcam();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  useEffect(() => {
    const imageInterval = setInterval(() => {
      if (videoRef.current && videoRef.current.srcObject) {
        captureAndSendImage();
      }
    }, 5000);
    const audioInterval = setInterval(() => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'inactive') {
        mediaRecorderRef.current.start();
        setTimeout(() => {
          if (mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
          }
        }, 30000); // Stops after 30 seconds of recording
      }
    }, 30000);

    return () => {
      clearInterval(imageInterval);
      clearInterval(audioInterval);
    };
  }, []);

  function sendAudioToServer(audioBlob) {
    const audioFile = new File([audioBlob], "recording.webm", { type: 'audio/webm' });
    const formData = new FormData();
    formData.append("file", audioFile);
  
    axios.post('http://localhost:5000/upload_audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      console.log('File sent successfully:', response.data);
    })
    .catch(error => {
      console.error('Error sending file:', error);
    });
  }

  function captureAndSendImage() {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
  
    // Draw the video content into the canvas
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
  
    // Get the data URL (base64 string of the image)
    const dataURL = canvas.toDataURL('image/png'); // You can adjust the format if needed
  
    const timestamp = new Date().getTime(); // Get current timestamp
  
    // Send POST request with the image data and timestamp
    axios.post('http://localhost:5000/upload_image', {
      image_base64: dataURL,
      timestamp: timestamp
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('Image uploaded successfully');
    })
    .catch(error => {
      console.error('Failed to upload image:', error);
    });
  }

  return (
    <div>
      <video ref={videoRef} autoPlay muted style={{ width: '640px', height: '480px' }}></video>
    </div>
  );
};

export default WebcamCapture;
