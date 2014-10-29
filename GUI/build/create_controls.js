
function create_controls(div, UIside_panel_opened) {
    //Create controls and attach click functions
    var result_gr, vizualizer, tweaks, canvaspos = $(div +' canvas').offset(), buttondiv = div + ' #graph_editor_button_container',
    canvas = $(div +' canvas')[0];


    // Create graph editor buttons tab
    $(div).prepend('<div id="graph_editor_button_container"></div>');

    // Rusult button controller
    $('<div id="result_button" class="graph_editor_button">result</div>').appendTo(buttondiv)
    .toggle(function() {
        document.getElementById('result_graph_image').src = "result.png?random="+new Date().getTime();
        $(div + ' #result_graph').show();
        $(canvas).hide()
        $(div+' #result_button').toggleClass('graph_editor_button_on');
    },
    function() {
        $(canvas).show()
        $(div + ' #result_graph').hide();
        $(div+' #result_button').toggleClass('graph_editor_button_on');
    });
    // Create result tab html code
    $(div).append('<div id="result_graph"></div>');
    result_gr = div+' #result_graph';
    $(result_gr).append("<table>\
        <img src='result.png' width='700' height='500' id='result_graph_image' />\
        </table>").hide();

    // Tougle physics button controller
    $('<div id="live_button" class="graph_editor_button">live</div>').appendTo(buttondiv).click(toggle_live);
    toggle_live(); // comment if you dont want to animate graph at start

    // Show options button controller
    $('<div id="tweaks_button" class="graph_editor_button">options</div>').appendTo(buttondiv)
    .toggle(function() {
        $(div).animate({'width': SIZE.x + 185 + 'px'},
            {queue: true, duration: 'fast', easing: 'linear', complete: function (){
                $(div + ' #graph_editor_tweaks').slideToggle('fast');
                UIside_panel_opened = true;
            }
        });
        $(div+' #tweaks_button').toggleClass('graph_editor_button_on');
    },
    function() {
        $(div + ' #graph_editor_tweaks').slideToggle('fast', function (){
            $(div).animate({'width': SIZE.x +'px'},
            {queue: true, duration: 'fast', easing: 'linear'});
            UIside_panel_opened = undefined;
        });
        $(div+' #tweaks_button').toggleClass('graph_editor_button_on');
    });
    // Create options button html code
    $(div).append('<div id="graph_editor_tweaks"></div>');
    tweaks = div+' #graph_editor_tweaks';
//    <span id='pos'>Position: (<span id='posx'></span>, <span id='posy'></span>)<br></span>\
    $(tweaks).append("<div class='infobox'><h4 id='title'>Info</h4>\
    <div id='info'>Index: <span id='index'></span><br>\
    <span id='vert'>Vertices: <span id='v1'></span>-><span id='v2'></span><br></span>\
    Label: <input type='text' id='label'>\
    <div id='dhcp'>DHCP: <input type='checkbox' id='dhcp_check'></div>\
    <div id='networkapp'>NetApps:<br>\
        <select id='networkapp_list' multiple='multiple'>\
            <option>WEB</option>\
            <option>VIDEO</option>\
            <option>FTP</option>\
            <option>P2P</option>\
            <option>SMTP</option>\
        </select>\
    </div>\
    </div>\
    <div id='none_selected'>No node is selected</div></div>");

    // Help button controller
    $('<div id="help_button" class="graph_editor_button">?</div>').appendTo(buttondiv)
    .click(function() {
        $('#help_dialog').dialog('open');
    });
    // Create help dialog html code
    $(div).append("<div id='help_dialog'> <ul><li><h3>create vertex</h3>Click on empty space not too close to existing vertices. <li><h3>create/erase edge</h3>Select the first vertex. Click on another vertex (different than the selected one) to turn on/off (toggle) the edge between them. <li><h3>increase/decrease multiplicity</h3> Use +/-. When multiplicity is 0 the edge disappears.<li><h3>remove a vertex</h3>Press '-' when vertex is selected.<li><h3>keep the selected vertex after edge toggle</h3>Hold 'SHIFT' to preserve the selected vertex after creating/erasing an edge.<li><h3>split an edge</h3> press 's' when esge is selected<li><h3>freeze a vertex</h3> pressing 'r' freezes the selected vertex (it will not move in live mode)<li><h3>add/remove loop</h3> press 'o'<li><h3>undo vertex deletion</h3>Click on the Undo button. Only the last deleted vertex can be recovered.  <li><h3>turn on realtime spring-charge model</h3>Press 'l' or click on the live checkbox.  </ul> </div>");
    $('#help_dialog').dialog({
        autoOpen : false,
        width : 700,
        title : "Graph Editor Help",
        modal : true
    });

    // Undo button controller
    $('<div id="undo_button" class="graph_editor_button">undo</div>').appendTo(buttondiv)
    .click(undo_remove).toggleClass('graph_editor_undo_disabled');

    // Erase graph button controller
    $('<div id="reset_button" class="graph_editor_button">reset</div>').appendTo(buttondiv)
    .click(function() {
        erase_graph();
     });

    // Togle vizualizer button controller
    $('<div id="viz_button" class="graph_editor_button">vizualization</div>').appendTo(buttondiv)
    .toggle(function() {
        $(div + ' #vizualizer').show();
        $(canvas).hide()
        $(div+' #viz_button').toggleClass('graph_editor_button_on');
    },
    function() {
        $(canvas).show()
        $(div + ' #vizualizer').hide();
        $(div+' #viz_button').toggleClass('graph_editor_button_on');
    });
    // Create Visualizer tab html code
    $(div).append('<div class="graph_editor_canvas" id="vizualizer"></div>');
    vizualizer = div+ ' #vizualizer';
    $(vizualizer).append('<canvas id="viz_canvas" class="graph_editor_canvas" width = "700" height = "500"></canvas>').hide();
    // Include Rgraph lib
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.core.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.effects.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.tooltips.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.dynamic.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.bar.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.line.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.pie.js" ></script>');
    var cvs  = document.getElementById("viz_canvas");
    var context = cvs.getContext('2d');

    var bar = new RGraph.Bar('viz_canvas', [5,4,8,7,6,3,6]);
    bar.Set('chart.gutter.top', 35);
    bar.Set('chart.labels', ['h1','h2','h3','h4','h5','h6','h7']);
    bar.Set('chart.tooltips', ['h1','h2','h3','h4','h5','h6','h7']);
    bar.Set('chart.gutter.right', 300);
    bar.Set('chart.gutter.bottom', 100);

    var line = new RGraph.Line('viz_canvas', [1.5,2.5,2.1,1.3,1.9,2.1,1.1]);
    line.Set('chart.linewidth', 3);
    line.Set('chart.colors', ['black']);
    line.Set('chart.ymax', 10);
    line.Set('chart.tickmarks', 'endcircle');
    line.Set('chart.tooltips', ['h1','h2','h3','h4','h5','h6','h7']);

    var combo = new RGraph.CombinedChart(bar, line);
    combo.Draw();

    /**
    * Create the  larger Pie chart
    */
    var pie = new RGraph.Pie('viz_canvas', bar.data);
    pie.Set('chart.centerx', 550);
    pie.Set('chart.radius', 90);
    pie.Set('chart.labels', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER']);
    pie.Set('chart.tooltips', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER'] );
    pie.Draw();

//    function DrawGraph ()
//        {
//          var data;
//
//            var line = new RGraph.Line('viz_canvas', data)
//                .Set('colors', ['green'])
//                .Set('linewidth', 1)
//                .Set('filled', true)
//                .Set('fillstyle', 'rgba(128,255,128,0.5)')
//                .Set('ymax', 60)
//                .Set('numxticks', 5)
//                .Set('labels', ['Now','25s','50s','75s','100s','125s'])
//                .Set('chart.gutter.top', 235)
//                .Set('chart.gutter.right', 300)
//                .Set('chart.gutter.bottom', 100)
//                .Draw();
//            var r    = RGraph.random(45,55);
//            data = [r].concat(data);
//            data.pop();
//            setTimeout(DrawGraph, 250);
//        }
//    DrawGraph();


    // Create Options tab code and controllers - create "INFOBOX"
    $(div + ' .infobox #info').hide();
    $(div + ' .infobox #label').keyup(function() {
        var index = $(div + ' .infobox #index').html(),
        title = $(div + ' .infobox #title').html();
        if (title === "Vertex Info"){
            nodes[index].label = $(div + ' .infobox #label').val();
        } else if (title === "Edge Info"){
            edge_list[index].label = $(div + ' .infobox #label').val();
        }
    });
    $(div + ' .infobox #dhcp_check').click(function() {
        var index = $(div + ' .infobox #index').html();
        nodes[index].service_dhcp = $(div + ' .infobox #dhcp_check').is(":checked");
    });
    $(div + ' .infobox #networkapp_list').change(function() {
        var netapp_list = document.getElementById("networkapp_list")
        var index = $(div + ' .infobox #index').html();
        var x = 0;
        for (x=0;x<netapp_list.length;x++) {
            nodes[index].netapps[netapp_list[x].text] = netapp_list[x].selected;
        }
    });
    $(tweaks).append("<h4>Tweaks</h4>");
    $(tweaks).append('<table>');
    add_checkbox('Vertex numbers', NODE_NUMBERS, tweaks, function() {
                NODE_NUMBERS = !NODE_NUMBERS;
                draw();
                });
    add_slider('Vertex Size', NODE_RADIUS, tweaks, 0, 30, function(newval) {
        NODE_RADIUS = newval;
        draw();
        });
    add_slider('Edge Strength', 50, tweaks, 0, 100, function(newval) {
        SPRING = (1 - 1e-2) + 1e-4 * (100 - newval);
        SPEED = newval / 50.0;
        SPEED *= 2 * SPEED;
    });
    add_slider('Edge Length', FIXED_LENGTH, tweaks, 0, 200, function (newval){
        FIXED_LENGTH = newval;
    });
    add_slider('Orientation', 0, tweaks, 0, 360, change_orientation);
    $(tweaks).append('</table>').hide();

}