TM07 = "http://tm07:1247"
//TM07 = "http://192.168.43.197:1247/"

document.getElementById("capturedFrameDisplay").src = TM07 + "get_video";

setInterval(function() {
  get_temperature();
    get_processor_info();
    get_ram();
    get_gyroscope_info();
},1000);

// Temperature
function get_temperature(){
  var request = new XMLHttpRequest();
  request.open('GET', TM07 + 'get_temperature', true);
  request.onload = function(e){
    // Begin accessing JSON data here
    var data = JSON.parse(request.response);
    if (request.status >= 200 && request.status < 400) {
        document.getElementById("temperatureDisplay").textContent = data.Temperature;
    }
  };
  request.onerror = function(e)
  {
    document.getElementById("temperatureDisplay").textContent = "No data";
  };
  request.send();
}

// Processor
function get_processor_info() {
    var request = new XMLHttpRequest();
    request.open('GET', TM07 + 'get_processor_percentage_usage', true);
    request.onload = function(e){
      // Begin accessing JSON data here
      var data = JSON.parse(request.response);
      if (request.status >= 200 && request.status < 400) {
        document.getElementById("processorUsage").textContent = data.ProcessorUsage;
      }
    };
    request.onerror = function(e) {
      document.getElementById("processorUsage").textContent = "No data";
    };
    request.send();
}

// RAM
function get_ram() {
  var request = new XMLHttpRequest();
  request.open('GET', TM07 + 'get_ram_percentage_usage', true);
  request.onload = function(e){
    // Begin accessing JSON data here
    var data = JSON.parse(request.response);
    if (request.status >= 200 && request.status < 400)
    {
      document.getElementById("RAMUsage").textContent = data.RAMUsage;
    }
  };
  request.onerror = function(e){
    document.getElementById("RAMUsage").textContent = "No data";
  };
  request.send();

}

// Gyroscope
function get_gyroscope_info() {
  var request = new XMLHttpRequest();
  request.open('GET', TM07 + 'get_gyroscope_xyz', true);
  request.onload = function(e){
    var data = JSON.parse(request.response);
    if (request.status >= 200 && request.status < 400)
    {
      document.getElementById("RegX").textContent = data.gyroscope[0];
      document.getElementById("RegY").textContent = data.gyroscope[1];
      document.getElementById("RegZ").textContent = data.gyroscope[2];
    }
  };
  request.onerror = function(e){
    document.getElementById("RegX").textContent = "No data";
    document.getElementById("RegY").textContent = "No data";
    document.getElementById("RegZ").textContent = "No data";
  };
  request.send();
}


function toggle_button(checkbox) {
    var request = new XMLHttpRequest();
    if (checkbox.checked)
    {
      request.open('GET', TM07 + 'toggle_diode/1', true);
    }
    else
    {
      request.open('GET', TM07 + 'toggle_diode/0', true);
    }
    request.send();
}
