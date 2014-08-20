/**
 * Created by vitalyantonenko on 13.08.14.
 */

function export_json(nodes, edges) {
    var data = {}, pos, i, exec = '';
    data.vertices = nodes.map(function(n) {
        return n.label;
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
    for (i = 0; i < nodes.length; i++) {
        if (typeof nodes[i].title == 'string') {
            data.netapps[nodes[i].label] = nodes[i].title.split(" ");
        }
//        var netapp_list = nodes[i].title.split(" ");
//
//        for (x=0;x<netapp_list.length;x++)
//        {
//            data.netapps[nodes[i].label][netapp_list[x]] = true;
//        }
    }
    return JSON.stringify(data);
}

var nodes = null;
var edges = null;
var network = null;
//    var directionInput = document.getElementById("layoutOn");
var layoutOn = false;
var groupsOn = false;

var json_groups;


function show_json() {
    var span = document.getElementById("debug");
    span.textContent = export_json(nodes, edges);
//        span.textContent = nodes[0].title;
//    var json_groups = JSON.parse(groups);
}

function changeLayout (l_cb) {
    if (l_cb.checked) {
        layoutOn = true;
    }
    else {
        layoutOn = false;
    }
    draw();
}

function changeGroups (g_cb) {
    if (g_cb.checked) {
        groupsOn = true;
        send_data('msg::groups::')
    }
    else {
        groupsOn = false;
    }
    draw();
}

function draw() {
  nodes = [];
  edges = [];
  var connectionCount = [];

  // randomly create some nodes and edges
  if (groupsOn == true) {
        for (var g in json_groups) {
            if (g != "no_group") {
                for (var k = 0; k < json_groups[g]["vertexes"].length; k++) {
                    nodes.push({
                        id: parseInt(json_groups[g]["vertexes"][k]),
                        label: String(parseInt(json_groups[g]["vertexes"][k])),
                        group: parseInt(g)+1
                    });
                }
            }
        }

        for (var g in json_groups) {
            for (var k = 0; k < json_groups[g]["edges"].length; k++) {
                edges.push({
                    from: parseInt(json_groups[g]["edges"][k][0]),
                    to: parseInt(json_groups[g]["edges"][k][1])
                });
            }
        }

  }
  else {
      var nodeCount = document.getElementById('nodeCount').value;
      for (var i = 0; i < nodeCount; i++) {
            nodes.push({
              id: i,
              label: String(i)
            });
            connectionCount[i] = 0;

            // create edges in a scale-free-network way
            if (i == 1) {
              var from = i;
              var to = 0;
              edges.push({
                from: from,
                to: to
              });
              connectionCount[from]++;
              connectionCount[to]++;
            }
            else if (i > 1) {
              var conn = edges.length * 2;
              var rand = Math.floor(Math.random() * conn);
              var cum = 0;
              var j = 0;
              while (j < connectionCount.length && cum < rand) {
                cum += connectionCount[j];
                j++;
              }

              var from = i;
              var to = j;
              edges.push({
                from: from,
                to: to
              });
              connectionCount[from]++;
              connectionCount[to]++;
            }
      }
  }

  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    hover: true,
    clustering: true,

    stabilize: false,
    navigation: true,
    keyboard: true,

    hierarchicalLayout: layoutOn,

    tooltip: {
        delay: 300,
        fontColor: "black",
        fontSize: 14, // px
        fontFace: "candara",
        color: {
          border: "#666",
          background: "#FFFFC6"
        }
    },

    nodes: {
        title:undefined,
        color: {
          border: 'black',
          hover: {
            background: 'pink',
            border: 'red'
          }
        }
    },
    edges: {
      length: 50
    },
    stabilize: false,
    dataManipulation: true,
    onAdd: function(data,callback) {
      var span = document.getElementById('operation');
      var idInput = document.getElementById('node-id');
      var labelInput = document.getElementById('node-label');
      var servicesInput = document.getElementById('node-services');
      var saveButton = document.getElementById('saveButton');
      var cancelButton = document.getElementById('cancelButton');
      var div = document.getElementById('network-popUp');
      span.innerHTML = "Add Node";
      idInput.value = data.id;
      labelInput.value = data.label;
      servicesInput.value = "";
      saveButton.onclick = saveData.bind(this,data,callback);
      cancelButton.onclick = clearPopUp.bind();
      div.style.display = 'block';

    },
    onEdit: function(data,callback) {

      var span = document.getElementById('operation');
      var idInput = document.getElementById('node-id');
      var labelInput = document.getElementById('node-label');
      var servicesInput = document.getElementById('node-services');
      var saveButton = document.getElementById('saveButton');
      var cancelButton = document.getElementById('cancelButton');
      var div = document.getElementById('network-popUp');
      span.innerHTML = "Edit Node";
      idInput.value = data.id;
      labelInput.value = data.label;

      // find Index in nodes array
      var node_index = _.findIndex(nodes, { 'id': data.id });
      servicesInput.value = nodes[node_index].title;

      saveButton.onclick = saveData.bind(this,data,callback);
      cancelButton.onclick = clearPopUp.bind();
      div.style.display = 'block';

    },
    onConnect: function(data,callback) {
      if (data.from == data.to) {
        var r=confirm("Do you want to connect the node to itself?");
        if (r==true) {
          callback(data);
        }
      }
      else {
        edges.push({
            from: data.from,
            to: data.to
        });
        callback(data);
      }
    }
  };
  network = new vis.Network(container, data, options);

  // add event listeners
  network.on('select', function(params) {
    document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });

  network.on("resize", function(params) {console.log(params.width,params.height)});



  function clearPopUp() {
    var saveButton = document.getElementById('saveButton');
    var cancelButton = document.getElementById('cancelButton');
    saveButton.onclick = null;
    cancelButton.onclick = null;
    var div = document.getElementById('network-popUp');
    div.style.display = 'none';

  }

  function saveData(data,callback) {
    var idInput = document.getElementById('node-id');
    var labelInput = document.getElementById('node-label');
    var servicesInput = document.getElementById('node-services');
    var div = document.getElementById('network-popUp');
    data.id = idInput.value;
    data.label = labelInput.value;
    data.title = servicesInput.value;

    if (servicesInput.value == ""){
        nodes.push({
          id: idInput.value,
          label: labelInput.value,
          title: undefined
        })
    }
    else {
        nodes.push({
            id: idInput.value,
            label: labelInput.value,
            title: servicesInput.value
        })
    }

    clearPopUp();
    callback(data);

  }

}


