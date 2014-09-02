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
    function malwarecenter_output(msg) {
//      document.getElementById('log').appendChild(document.createTextNode(new Date() + '   ' + msg + '\n'));
      document.getElementById('MalwareCenterOutputArea').appendChild(document.createTextNode(msg));
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
        else if (event.data.indexOf('msg::leaves::') == 0) {
            var leaves_str = event.data.slice('msg::leaves::'.length);

        }
        else if (event.data.indexOf('msg::controller::') == 0) {
            controller_output(event.data.slice('msg::controller::'.length));

            var textArea = document.getElementById('ControllerOutputArea');
            textArea.scrollTop = textArea.scrollHeight;
        }
        else if (event.data.indexOf('msg::malwarecenter::') == 0) {
            var mal_mess = event.data.slice('msg::malwarecenter::'.length);
            var host_id = 'None';

            if (mal_mess.indexOf("new worm instance") >= 0) {
                var mess = mal_mess.split(' ');
                var tmp_mess = mess[3];
                var host_intf_name = tmp_mess.split(':');
                tmp_mess = host_intf_name[0];
                var host_name = tmp_mess.split('-');
                tmp_mess = host_name[0];
                host_id = tmp_mess.substring(1);
                if (inf_nodes.indexOf(parseInt(host_id)) == -1) {
                    inf_nodes.append(parseInt(host_id));

                }
            }


            malwarecenter_output(event.data.slice('msg::malwarecenter::'.length));
//            malwarecenter_output(host_id);

            var textArea = document.getElementById('MalwareCenterOutputArea');
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

   function add_node_test() {
       nodes.update({
           id: 1,
           label: 'FUCK'
       });

       var node_ids = nodes.getIds();

       for (n_id in node_ids) {
           nodes.update({
               id: n_id,
               label: 'FUCK'
           });
       }

//       nodes.forEach(function (node) {node.group = 6; });

   }


