/**
 * Created by vitalyantonenko on 03.09.14.
 */

var global_options = {
    hover: true,
    clustering: true,

    navigation: true,
    keyboard: true,

    hierarchicalLayout: false,

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

    groups: {
        base_group: {
          shape: 'circle',
          color: {
            border: 'black',
            background: 'white',
            highlight: {
              border: 'yellow',
              background: 'orange'
            }
          },
          fontColor: 'black',
          fontSize: 11
        },

        malware_group: {
          shape: 'circle',
          color: {
            border: 'black',
            background: 'red',
            highlight: {
              border: 'yellow',
              background: 'orange'
            }
          },
          fontColor: 'black',
          fontSize: 12
        }
        ,

        1: {
          color: {
            border: 'black',
            background: 'green'
          }
        }



    },

    stabilize: true,
//    freezeForStabilization: true,
    physics: {barnesHut: {gravitationalConstant: -500, springConstant: 0.1, springLength: 20}},

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
      saveButton.onclick = addData.bind(this,data,callback);
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
//      var node_index = _.findIndex(nodes, { 'id': data.id });
      servicesInput.value = nodes.get(data.id).title;

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
        edges.add({
            from: data.from,
            to: data.to
        });
//        callback(data);
      }
    }
  };

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

//    var node_index = _.findIndex(nodes, { 'id': data.id });
//    nodes.splice(node_index, 1);
//    alert(idInput.value);
    if (servicesInput.value == ""){
        nodes.update({
          id: parseInt(idInput.value),
          label: labelInput.value
        });

    }
    else {
        nodes.update({
            id: parseInt(idInput.value),
            label: labelInput.value,
            title: servicesInput.value
        });
    }

    clearPopUp();
//    callback(data);

  }

function addData(data,callback) {
    var idInput = document.getElementById('node-id');
    var labelInput = document.getElementById('node-label');
    var servicesInput = document.getElementById('node-services');
    var div = document.getElementById('network-popUp');
    data.id = idInput.value;
    data.label = labelInput.value;
    data.title = servicesInput.value;

//    var node_index = _.findIndex(nodes, { 'id': data.id });
//    nodes.splice(node_index, 1);
//    alert(idInput.value);
    if (servicesInput.value == ""){
        nodes.add({
          id: parseInt(idInput.value),
          label: labelInput.value,
          group: "base_group"
        });

    }
    else {
        nodes.add({
            id: parseInt(idInput.value),
            label: labelInput.value,
            title: servicesInput.value,
            group: "base_group"
        });
    }

    clearPopUp();
//    callback(data);

  }