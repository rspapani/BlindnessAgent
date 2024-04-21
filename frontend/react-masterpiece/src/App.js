import React from 'react';
import './App.css';
import Autism from './components/Autism'; // Assuming 'Autism.jsx' is in the 'components' directory
import Header from './components/Header.js';
import WebcamCapture from './components/WebcamCapture.js';
function App() {
  const jsonData = {
    "Button 1": [
        ["person1", "response"],
        ["person2", "response"]
    ],
    "Button 2": [
        ["person1", "response"],
        ["person2", "response"]
    ],
    "Button 3": [
        ["person1", "response"],
        ["person2", "response"]
    ],
    "Button 4": [
        ["person1", "response"],
        ["person2", "response"]
    ]
};

  return (
    <div className="App">
      
      <Header/>
      <WebcamCapture/>
      <Autism data={jsonData} />
     
    </div>
  );
}

export default App;
