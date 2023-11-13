// WebSocket support
var targetUrl = `ws://${location.host}/ws`;
var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  initializeSocket();
}

function initializeSocket() {
  console.log("Opening WebSocket connection MicroPython Server...");
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}
function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(message) {
  //const parsedMessage = JSON.parse(message);
  console.log("WebSocket message received:", message);
  const textarea = document.getElementById('message');
  
  
  textarea.value += message.data + '\r\n';

}

function sendMessage(message) {
  websocket.send(message);
}

function updateValues(data) {
//   sensorData.unshift(data);
//   if (sensorData.length > 20) sensorData.pop();
//   sensorValues.value = sensorData.join("\r\n");
}
