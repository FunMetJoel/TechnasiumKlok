#include <WiFi.h>
#include <WebServer.h>
#include "webinterface.h"
#include "patterns.h"


/*Put your SSID & Password*/
const char* ssid = "WIFISSID";  // Enter SSID here
const char* password = "WIFIPASSWORD";  //Enter Password here
WebServer server(80);

byte currentMode = 0;

Pattern** patternsPtr;

void webinterface_setup(Pattern** newPatternsPtr) {
  Serial.begin(115200);
  delay(100);
  patternsPtr = newPatternsPtr;

  Serial.println("Connecting to ");
  Serial.println(ssid);

  WiFi.setHostname("Klok");

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  server.on("/", handle_OnConnect);
  server.on("/setMode", handle_setMode);
  server.on("/getMode", handle_getMode);
  server.on("/setParameter", handle_setParameter);
  server.on("/status", handle_status);
  server.onNotFound(handle_NotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void webinterface_loop(byte *currentPatternId) {
  server.handleClient();
  *currentPatternId = currentMode;
}


String SendHTML(){
  String ptr = R"html(
  <!DOCTYPE html>
  <html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LED Control</title>
  <style>
  html { 
    font-family: Helvetica; 
    display: inline-block; 
    margin: 0px auto; 
    text-align: center;
  }
  body{
    margin-top: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  } 
  h1 {
    color: #444444;
    margin: 50px auto 30px;
  } 
  h3 {
    color: #444444;
    margin-bottom: 50px;
  }
  p {
    font-size: 14px;
    color: #888;
    margin-bottom: 10px;
  }

  select {
    font-size: 16px;
    padding: 5px;
  }

  input[type=number], input[type=range], input[type=color], input[type=checkbox], input[type=text] {
    font-size: 16px;
    margin: 5px;
  }

  #parameters {
    margin: 10px;
    background-color: #F0f0f0;
    padding: 10px;
    border-radius: 5px;
    width: fit-content;
  }
  </style>
  <script>
    function setMode(mode) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/setMode?mode=' + mode, true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var parameters = JSON.parse(xhr.responseText).params;
          setParameters(parameters);
        }
      };
      console.log(mode)
      xhr.send();
    };

    function setParameter(name, value) {
      console.log(name + ': ' + value);
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/setParameter?name=' + name + '&value=' + value, true);
      xhr.send();
      var mode = document.getElementById('patternSelect').value;
      setMode(mode)
    };

    function setParameters(parameters) {
      var parametersDiv = document.getElementById('parameters');
      while (parametersDiv.firstChild) {
        parametersDiv.removeChild(parametersDiv.firstChild);
      }
      for (var i = 0; i < parameters.length; i++) {
        var parameter = parameters[i];
        var label = document.createElement('label');
        label.innerHTML = parameter[0] + ': ';
        parametersDiv.appendChild(label);
        if (parameter[1] == '1') {
          var input = `<input type='number' step='0.01' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.value)'>`
        } else if (parameter[1] == '2') {
          var input = `<input type='range' min='0' max='255' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.value)'>`
        } else if (parameter[1] == '3') {
          var input = `<input type='color' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.value.replace("#", ""))'>`
        } else if (parameter[1] == '4') {
          var input = `<input type='range' min='0' max='1' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.value)'>`
        } else if (parameter[1] == '5') {
          var input = `<input type='checkbox' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.checked)'>`
        } else {
          var input = `<input type='text' value=` + parameter[2]+ ` onchange='setParameter("`+parameter[0]+`", this.value)'>`
        }
        parametersDiv.innerHTML += input;
        parametersDiv.appendChild(document.createElement('br'));
      };
    };

    function getMode() {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/getMode', true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var mode = JSON.parse(xhr.responseText).mode;
          document.getElementById('patternSelect').value = mode;
          setMode(mode);
        }
      };
      xhr.send();
    };

    getMode();
  </script>
  </head>
  <body>
  <h2>LED Control</h2>
  <p>Select a pattern:</p>
  <select id="patternSelect" onchange="setMode(this.value)">)html";
  for (int i = 0; i < 4; i++) {
    ptr += "<option value=\"" + String(i) + "\">" + patternsPtr[i]->displayName + "</option>";
  }
  ptr += R"html(
  </select>
  <div id="parameters">
  </div>
  </body>
  </html>
  )html";
  return ptr;
}

String SendHTMLold(){
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr +="<title>LED Control</title>\n";
  ptr +="<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr +="body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;} h3 {color: #444444;margin-bottom: 50px;}\n";
  ptr +=".button {display: block;width: 80px;background-color: #3498db;border: none;color: white;padding: 13px 30px;text-decoration: none;font-size: 25px;margin: 0px auto 35px;cursor: pointer;border-radius: 4px;}\n";
  ptr +=".button-on {background-color: #3498db;}\n";
  ptr +=".button-on:active {background-color: #2980b9;}\n";
  ptr +=".button-off {background-color: #34495e;}\n";
  ptr +=".button-off:active {background-color: #2c3e50;}\n";
  ptr +="p {font-size: 14px;color: #888;margin-bottom: 10px;}\n";
  ptr +="</style>\n";
  ptr +="<script>\n";
  ptr +="function setMode(mode) {\n";
  ptr +="  var xhr = new XMLHttpRequest();\n";
  ptr +="  xhr.open('GET', '/setMode?mode=' + mode, true);\n";
  ptr +="  xhr.onreadystatechange = function() {\n";
  ptr +="    if (xhr.readyState == 4 && xhr.status == 200) {\n";
  ptr +="      var parameters = JSON.parse(xhr.responseText).params;\n";
  ptr +="      setParameters(parameters);\n";
  ptr +="    }\n";
  ptr +="  };\n";
  ptr +="  console.log(mode)\n";
  ptr +="  xhr.send();\n";
  ptr +="};\n";
  ptr += "function setParameter(name, value) {\n";
  ptr += "  console.log(name + ': ' + value);\n";
  ptr += "  var xhr = new XMLHttpRequest();\n";
  ptr += "  xhr.open('GET', '/setParameter?name=' + name + '&value=' + value, true);\n";
  ptr += "  xhr.send();\n";
  ptr += "  var mode = document.getElementById('patternSelect').value;\n";
  ptr += "  setMode(mode)\n";
  ptr += "};\n";
  ptr +="function setParameters(parameters) {\n";
  ptr +="  var parametersDiv = document.getElementById('parameters');\n";
  ptr +="  while (parametersDiv.firstChild) {\n";
  ptr +="    parametersDiv.removeChild(parametersDiv.firstChild);\n";
  ptr +="  }\n";
  ptr +="  for (var i = 0; i < parameters.length; i++) {\n";
  ptr +="    var parameter = parameters[i];\n";
  ptr +="    var label = document.createElement('label');\n";
  ptr +="    label.innerHTML = parameter[0] + ': ';\n";
  ptr +="    parametersDiv.appendChild(label);\n";
  ptr +="    if (parameter[1] == '" + String(parameterType::FLOAT) + "') {\n";
  ptr +="       var input = `<input type='number' step='0.01' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.value)'>`\n";
  ptr +="    } else if (parameter[1] == '" + String(parameterType::BYTE) + "') {\n";
  ptr +="       var input = `<input type='range' min='0' max='255' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.value)'>`\n";
  ptr +="    } else if (parameter[1] == '" + String(parameterType::COLOR) + "') {\n";
  ptr +="       var input = `<input type='color' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.value.replace(\"#\", \"\"))'>`\n";
  ptr +="    } else if (parameter[1] == '" + String(parameterType::PERCENTAGE) + "') {\n";
  ptr +="       var input = `<input type='range' min='0' max='1' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.value)'>`\n";
  ptr +="    } else if (parameter[1] == '" + String(parameterType::BOOL) + "') {\n";
  ptr +="       var input = `<input type='checkbox' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.checked)'>`\n";
  ptr +="    } else {\n";
  ptr +="       var input = `<input type='text' value=` + parameter[2]+ ` onchange='setParameter(\"`+parameter[0]+`\", this.value)'>`\n";
  ptr +="    }\n";
  ptr +="    parametersDiv.innerHTML += input;\n";
  ptr +="    parametersDiv.appendChild(document.createElement('br'));\n";
  ptr +="    };\n";
  ptr +="};\n";
  ptr +="function getMode() {\n";
  ptr +="  var xhr = new XMLHttpRequest();\n";
  ptr +="  xhr.open('GET', '/getMode', true);\n";
  ptr +="  xhr.onreadystatechange = function() {\n";
  ptr +="    if (xhr.readyState == 4 && xhr.status == 200) {\n";
  ptr +="      var mode = JSON.parse(xhr.responseText).mode;\n";
  ptr +="      document.getElementById('patternSelect').value = mode;\n";
  ptr +="      setMode(mode);\n";
  ptr +="    }\n";
  ptr +="  };\n";
  ptr +="  xhr.send();\n";
  ptr +="};\n";
  ptr +="getMode();\n";
  ptr +="</script>\n";
  ptr +="</head>\n";
  ptr +="<body>\n";
  ptr +="<h1>Klok</h1>\n";
  ptr +="<h3>Dit is een klok</h3>\n";
  ptr += "<p>Selecteer een patroon:</p>\n";
  ptr += "<select id=\"patternSelect\" onchange=\"setMode(this.value)\">\n";
  for (int i = 0; i < 3; i++) {
    ptr += "<option value=\"" + String(i) + "\">" + patternsPtr[i]->displayName + "</option>\n";
  }
  ptr += "</select>\n";
  ptr +="<div id=\"parameters\">\n";
  ptr +="</div>\n";
  ptr +="</body>\n";
  ptr +="</html>\n";
  return ptr;
}

void handle_OnConnect() {
  Serial.println("Client connected");
  server.send(200, "text/html", SendHTML()); 
}

void handle_setMode() {
  if (server.hasArg("mode")) {
    String paramValue = server.arg("mode");
    int paramValueInt = paramValue.toInt();
    Serial.println("Setting mode to " + paramValue);
    currentMode = paramValueInt;
    Serial.println("Current mode: " + String(currentMode));
    String** parameters = patternsPtr[currentMode]->getParameters();
    int numRows = patternsPtr[currentMode]->numParameters;
    String json = "{ \"params\": ";
    json += "[";
    for (int i = 0; i < numRows; i++) {
      json += "[\"" + parameters[i][0] + "\", \"" + parameters[i][1] + "\", \"" + parameters[i][2] + "\"]";
      if (i < numRows-1) {
        json += ",";
      }
    }
    json += "]}";
    server.send(200, "application/json", json);
  }
}

void handle_setParameter() {
  if (!server.hasArg("name") || !server.hasArg("value")) {
    server.send(400, "text/plain", "400: Invalid Request");
    return;
  }
  String name = server.arg("name");
  String value = server.arg("value");
  Serial.println(name + ": " + value);
  patternsPtr[currentMode]->setParameter(name, value);
  server.send(200, "text/plain", "OK");
}

void handle_status() {
  String json = "{ \"LED1\": " + String(currentMode) + " }";
  server.send(200, "application/json", json);
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

void handle_getMode() {
  server.send(200, "application/json", "{ \"mode\": " + String(currentMode) + " }");
}
