/**
 * Created with PyCharm.
 * User: vitalyantonenko
 * Date: 24.09.13
 * Time: 14:39
 * To change this template use File | Settings | File Templates.
 */


function Draw_visgraph(div, size_x, size_y){

    var visgraph = div+ ' #visgraph';
//    $(visgraph).append('<div class="label">FUCK!</div>');

    $(visgraph).append('<div id="mygraph" ' +
        'style="width: '+ size_x + 'px; height: '+ size_y +'px;"></div>').hide();


    $(visgraph).append('<script src="lib/vis/vis.js"></script>');

    $(visgraph).append('<link href="css/vis.css" rel="stylesheet" type="text/css" />');

    var nodes = null;
    var edges = null;
    var graph = null;

    function draw() {
        nodes = [];
        edges = [];
        // randomly create some nodes and edges
        var nodeCount = 500;

        for (var i = 0; i < nodeCount; i++) {
            nodes.push({
                id: i,
                label: String(i)
            });
        }
        for (var i = 0; i < nodeCount; i++) {
            var from = i;
            var to = i;
            to = i;
            while (to == i) {
                to = Math.floor(Math.random() * (nodeCount));
            }
            edges.push({
                from: from,
                to: to
            });
        }
        // create a graph
        var container = document.getElementById('mygraph');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            edges: {
                length: 80
            },
            autoResize: true,
            clustering: {
                enabled: true
            },
            stabilize: false
        };
        graph = new vis.Graph(container, data, options);

    }

    draw();

}