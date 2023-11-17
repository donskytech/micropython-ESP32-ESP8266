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
  const parsedMessage = JSON.parse(message.data);
  console.log("WebSocket message received:", parsedMessage);

  if (parsedMessage) {
    switch (parsedMessage.event_type) {
      case "updateSensorReadings":
        updateSensorReadings(parsedMessage);
        break;
      case "updateWaterCycle":
        updateWaterCycle(parsedMessage);
        break;
      case "updateSystemTime":
        updateSystemTime(parsedMessage);
        break;
      default:
        console.log("Unknown event type received");
    }
  }
}

function sendMessage(message) {
  websocket.send(message);
}

function updateValues(data) {
  //   sensorData.unshift(data);
  //   if (sensorData.length > 20) sensorData.pop();
  //   sensorValues.value = sensorData.join("\r\n");
}

function updateSensorReadings(message) {
  console.log(`updateSensorReadings :: ${message}`);
  let item = document.getElementById(message.soil_monitor_id);
  item.textContent = `${message.soil_monitor} : ${message.sensor_reading}`;
}

function updateWaterCycle(message) {
  console.log(`updateWaterCycle :: ${message}`);
  let cycleList = document.getElementById("cycle-list");
  let noCycleItem = document.getElementById("no-cycle-list");
  if (noCycleItem) {
    cycleList.removeChild(noCycleItem);
  }

  var newItem = document.createElement("li");
  newItem.textContent = `${message.soil_module} - ${message.date_time}`;
  cycleList.insertBefore(newItem, cycleList.firstChild);
  // item.textContent = `${message.soil_monitor} : ${message.sensor_reading}`;
}

function updateSystemTime(message) {
  console.log(`updateSystemTime :: ${message}`);
  let systemTime = document.getElementById("system-time");
  systemTime.textContent = `${message.date_time}`;
}
