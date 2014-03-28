/**
 * Created with PyCharm.
 * User: vitalyantonenko
 * Date: 24.09.13
 * Time: 14:39
 * To change this template use File | Settings | File Templates.
 */

function Draw_sigma(div, size_x, size_y){
    var sigmadiv = div+ ' #sigmadiv';
//    $(sigmadiv).append('<div class="label">FUCK!</div>');
    $(sigmadiv).append('<div id="sig" class="graph_editor_canvas" ' +
        'style="width: '+ size_x + 'px; height: '+ size_y +'px;"></div>').hide();

    var sig = sigmadiv + ' #sig';

    // include Sigma
    $(sig).append('<script src="lib/sigma/src/sigma.core.js"></script>');
    $(sig).append('<script src="lib/sigma/src/conrad.js"></script>');
    $(sig).append('<script src="lib/sigma/src/utils/sigma.utils.js"></script>');
    $(sig).append('<script src="lib/sigma/src/utils/sigma.polyfills.js"></script>');
    $(sig).append('<script src="lib/sigma/src/sigma.settings.js"></script>');
    $(sig).append('<script src="lib/sigma/src/classes/sigma.classes.dispatcher.js"></script>');
    $(sig).append('<script src="lib/sigma/src/classes/sigma.classes.configurable.js"></script>');
    $(sig).append('<script src="lib/sigma/src/classes/sigma.classes.graph.js"></script>');
    $(sig).append('<script src="lib/sigma/src/classes/sigma.classes.camera.js"></script>');
    $(sig).append('<script src="lib/sigma/src/classes/sigma.classes.quad.js"></script>');
    $(sig).append('<script src="lib/sigma/src/captors/sigma.captors.mouse.js"></script>');
    $(sig).append('<script src="lib/sigma/src/captors/sigma.captors.touch.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/sigma.renderers.canvas.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/sigma.renderers.def.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.labels.def.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.hovers.def.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.nodes.def.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.edges.def.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.edges.arrow.js"></script>');
    $(sig).append('<script src="lib/sigma/src/renderers/canvas/sigma.canvas.edges.curve.js"></script>');
    $(sig).append('<script src="lib/sigma/src/middlewares/sigma.middlewares.rescale.js"></script>');
    $(sig).append('<script src="lib/sigma/src/middlewares/sigma.middlewares.copy.js"></script>');
    $(sig).append('<script src="lib/sigma/src/misc/sigma.misc.animation.js"></script>');
    $(sig).append('<script src="lib/sigma/src/misc/sigma.misc.bindEvents.js"></script>');
    $(sig).append('<script src="lib/sigma/src/misc/sigma.misc.drawHovers.js"></script>');

    $(sig).append('<script src="lib/sigma/plugins/sigma.plugins.animate/sigma.plugins.animate.js"></script>');

    $(sig).append('<div id="sigma-container" style="width: '+ size_x + 'px; height: '+ size_y +'px;"></div>');

    var i,
    s,
    o,
    L = 10,
    N = 100,
    E = 500,
    g = {
      nodes: [],
      edges: []
    },
    step = 0;

    // Generate a random graph:
    for (i = 0; i < N; i++) {
      o = {
        id: 'n' + i,
        label: 'Node ' + i,
        circular_x: L * Math.cos(Math.PI * 2 * i / N - Math.PI / 2),
        circular_y: L * Math.sin(Math.PI * 2 * i / N - Math.PI / 2),
        circular_size: Math.random(),
        circular_color: '#' + (
          Math.floor(Math.random() * 16777215).toString(16) + '000000'
        ).substr(0, 6),
        grid_x: i % L,
        grid_y: Math.floor(i / L),
        grid_size: 1,
        grid_color: '#ccc'
      };

      ['x', 'y', 'size', 'color'].forEach(function(val) {
        o[val] = o['grid_' + val];
      });

      g.nodes.push(o);
    }

    for (i = 0; i < E; i++)
      g.edges.push({
        id: 'e' + i,
        source: 'n' + (Math.random() * N | 0),
        target: 'n' + (Math.random() * N | 0)
      });

    // Instanciate sigma:
    s = new sigma({
      graph: g,
      container: 'sigma-container',
      settings: {
        animationsTime: 1000
      }
    });

    setInterval(function() {
      var prefix = ['grid_', 'circular_'][step = +!step];
      sigma.plugins.animate(
        s,
        {
          x: prefix + 'x',
          y: prefix + 'y',
          size: prefix + 'size',
          color: prefix + 'color'
        }
      );
    }, 2000);


}
