export const captureMicrophoneData = () => {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const scriptNode = audioContext.createScriptProcessor(0, 1, 1);

  // Create a WebSocket connection to the server
  const socket = new WebSocket('wss://bramka:443'); // Replace with your server's IP and WebSocket port

  scriptNode.onaudioprocess = (event) => {
    const audioData = event.inputBuffer.getChannelData(0);

    // Convert audio data to Signed 16-bit Little Endian format
    const int16Array = new Int16Array(audioData.length);
    for (let i = 0; i < audioData.length; i++) {
      int16Array[i] = audioData[i] * 0x7fff; // Scale to 16-bit range
    }

    // Send the audio data to the WebSocket server
    socket.send(int16Array.buffer);
  };

  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      const audioSource = audioContext.createMediaStreamSource(stream);
      audioSource.connect(scriptNode);
      scriptNode.connect(audioContext.destination);
      console.log('Started audio streaming');
    })
    .catch((error) => {
      console.error('Error accessing microphone:', error);
    });
};
