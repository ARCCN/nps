//onerror = function (msg) {
//      log(msg);
//    }
//    function log(msg) {
//      document.getElementById('log').appendChild(document.createTextNode(new Date() + '   ' + msg + '\n'));
//    }
    function console_output(msg) {
//      document.getElementById('log').appendChild(document.createTextNode(new Date() + '   ' + msg + '\n'));
      document.getElementById('ConsoleOutputArea').appendChild(document.createTextNode(msg));
    }
    function controller_output(msg) {
//      document.getElementById('log').appendChild(document.createTextNode(new Date() + '   ' + msg + '\n'));
      document.getElementById('ControllerOutputArea').appendChild(document.createTextNode(msg));
    }
    function status(msg) {
//      log(msg);
      document.getElementById('status').textContent = msg;
    }


var socket;
   function connect() {
     var url = document.getElementById('url').value;
     socket = new WebSocket(url);
     status('Connecting to "' + url + '"...');
     socket.onopen = function (event) {
       status('Connected to "' + socket.url + '".');
     };
     socket.onmessage = function (event) {
//       log('RCVD: ' + event.data);
        if (event.data.indexOf('msg::groups::') == 0) {
            var groups = event.data.slice('msg::groups::'.length);
            json_groups = JSON.parse(groups);
        }
        else if (event.data.indexOf('msg::controller::') == 0) {
            controller_output(event.data.slice('msg::controller::'.length));

            var textArea = document.getElementById('ControllerOutputArea');
            textArea.scrollTop = textArea.scrollHeight;
        }
        else {
            console_output(event.data);

            var textArea = document.getElementById('ConsoleOutputArea');
            textArea.scrollTop = textArea.scrollHeight;
        }


     };
     socket.onclose = function (event) {
       status('Disconnected.');
     };

   }

   function disconnect() {
     if (socket) {
       status('Disconnecting.');
       socket.close();
     } else {
//       log('Not connected.');
     }
   }

   function send() {
       socket.send(document.getElementById('text').value);
       document.getElementById('text').value = "";
   }

    function send_data(data) {
       socket.send(data);
    }


   function update() {
     if (socket) {
       document.getElementById('readyState').textContent = socket.readyState;
       document.getElementById('bufferedAmount').textContent = socket.bufferedAmount;
     } else {
       document.getElementById('readyState').textContent = '-';
       document.getElementById('bufferedAmount').textContent = '-';
     }
   }
   setInterval(update, 10);


