/**
 * Created by vitalyantonenko on 13.08.14.
 */
function send_input_json() {
       var json_data = export_json(nodes, edges);
       var input_flag_str = "msg::input_json::";
       send_data(input_flag_str + json_data);
   }

function simulate() {
//       connect();
//       setTimeout(1000);
       send_input_json();
       send_data("msg::simulate::");
   }

function controller() {
       send_data("msg::controller::");
   }

function malwarecenter() {
        send_data("msg::malwarecenter::");
    }

function export_json(nodes, edges) {
    var data = {}, pos, i, exec = '';
    data.vertices = nodes.map(function(n) {
        return n.id;
    });
    data.edges = edges.map(function(e) {
        if (e.label == null) {
            return [e.from, e.to, {}];
        }
        else {
            return [e.from, e.to, e.label];
        }

    });
    data.name = "test";
    data.netapps = {};
//    for (i = 0; i < nodes.length; i++) {
//        if (typeof nodes[i].title == 'string') {
////            data.netapps[nodes[i].id] = nodes[i].title.split(" ");
//        }
////        var netapp_list = nodes[i].title.split(" ");
////
////        for (x=0;x<netapp_list.length;x++)
////        {
////            data.netapps[nodes[i].label][netapp_list[x]] = true;
////        }
//    }
    return JSON.stringify(data);
}

var nodes = null;
var inf_nodes = [];

var edges = null;

var network = null;
//    var directionInput = document.getElementById("layoutOn");
var malwareOn = false;

var json_groups = null;
var json_hosts = null;
var leaves;



function show_json() {
    var span = document.getElementById("debug");
    span.textContent = export_json(nodes, edges);
}

function changeLayout (l_cb) {
    if (l_cb.checked) {
        var options = global_options;
        options.hierarchicalLayout = true;
        network.setOptions(options);
    }
    else {
        var options = global_options;
        options.hierarchicalLayout = false;
        network.setOptions(options);
    }
    draw();
}

function changeGroups (g_cb) {
    if (g_cb.checked) {
        if (json_groups == null) {
            send_data('msg::groups::');
            g_cb.checked = false;
        }
        else {
            for (var g in json_groups) {
                    if (g != "no_group") {
                        for (var k = 0; k < json_groups[g]["vertexes"].length; k++) {
                            nodes.update({
                                id: parseInt(json_groups[g]["vertexes"][k]),
//                                label: String(parseInt(json_groups[g]["vertexes"][k])),
                                group: parseInt(g)+1
                            });
                        }
                    }
                }
        }
    }
    else {
          for (var g in json_groups) {
                    if (g != "no_group") {
                        for (var k = 0; k < json_groups[g]["vertexes"].length; k++) {
                            nodes.update({
                                id: parseInt(json_groups[g]["vertexes"][k]),
//                                label: String(parseInt(json_groups[g]["vertexes"][k])),
                                group: 'base_group'
                            });
                        }
                    }
           }
//        for (node_ID in nodes.getIds()) {
//            nodes.update({
//                id: node_ID,
//                group: 'base_group'
//            });
//        }
    }
}

function changeMalware (m_cb) {
    if (m_cb.checked) {
        malwareOn = true;
        if (json_hosts == null) {
            send_data('msg::hosts::');
            m_cb.checked = false;
            malwareOn = false;
        }
        else {
            for (var i in inf_nodes) {
                nodes.update({
                    id: inf_nodes[i],
                    group: 'malware_group'
                });
            }
        }
    }
    else {
        malwareOn = false;
        for (node_ID in nodes.getIds()) {
            nodes.update({
                id: node_ID,
                group: 'base_group'
            });
        }
    }
}


function create_graph() {
    nodes = new vis.DataSet();
    edges = new vis.DataSet();
    var connectionCount = [];
    var nodeCount = document.getElementById('nodeCount').value;
    for (var i = 0; i < nodeCount; i++) {
        nodes.add({
          id: i,
          label: String(i),
          group: 'base_group'
        });
        connectionCount[i] = 0;

        // create edges in a scale-free-network way
        if (i == 1) {
          var from = i;
          var to = 0;
          edges.add({
            from: from,
            to: to
          });
          connectionCount[from]++;
          connectionCount[to]++;
        }
        else if (i > 1) {
//          alert(edges.get().length);
          var conn = edges.get().length * 2;
          var rand = Math.floor(Math.random() * conn);
          var cum = 0;
          var j = 0;
          while (j < connectionCount.length && cum < rand) {
            cum += connectionCount[j];
            j++;
          }

          var from = i;
          var to = j;
          edges.add({
            from: from,
            to: to
          });
          connectionCount[from]++;
          connectionCount[to]++;
        }
    }

}


function draw() {
  var container = document.getElementById('mynetwork');

  var data = {
      nodes: nodes,
      edges: edges
  };

  var options = global_options;

  network = new vis.Network(container, data, options);

  // add event listeners
  network.on("select", function(params) {
    document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });

  network.on("resize", function(params) {console.log(params.width,params.height)});

}




