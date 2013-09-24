/**
 * Created with PyCharm.
 * User: vitalyantonenko
 * Date: 24.09.13
 * Time: 14:39
 * To change this template use File | Settings | File Templates.
 */

function Draw_vizualization(div){
    var vizualizer = div+ ' #vizualizer';
    $(vizualizer).append('<canvas id="viz_canvas" class="graph_editor_canvas" width = "700" height = "500"></canvas>').hide();

    // include Rgraph
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.core.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.effects.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.tooltips.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.common.dynamic.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.bar.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.line.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.pie.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.hprogress.js" ></script>');
    $(vizualizer).append('<script src="lib/rgraph/RGraph.gauge.js" ></script>');
    var cvs  = document.getElementById("viz_canvas");
    var context = cvs.getContext('2d');


    var line1 = new RGraph.Line("viz_canvas", [4,5,8,7,6,4,3], [7,1,6,9,4,6,5]);
    line1.Set('chart.labels', ['h1','h2','h3','h4','h5','h6','h7']);
    line1.Set('chart.linewidth', 2);
    line1.Set('chart.hmargin', 10);
    line1.Set('chart.shadow', true);
    line1.Set('chart.adjustable', true);
//    line.Set('chart.title', 'An adjustable line chart');
    line1.Set('chart.title.vpos', 0.5);
    line1.Set('chart.spline', true);
    line1.Set('chart.tickmarks', 'circle');
    line1.Set('chart.gutter.top', 35);
    line1.Set('chart.gutter.right', 300);
    line1.Set('chart.gutter.bottom', 300);
    line1.Draw();

//    var bar = new RGraph.Bar('viz_canvas', [5,4,8,7,6,3,6]);
//    bar.Set('chart.gutter.top', 35);
//    bar.Set('chart.labels', ['h1','h2','h3','h4','h5','h6','h7']);
//    bar.Set('chart.tooltips', ['h1','h2','h3','h4','h5','h6','h7']);
//    bar.Set('chart.gutter.right', 300);
//    bar.Set('chart.gutter.bottom', 200);
//
//    var line = new RGraph.Line('viz_canvas', [1.5,2.5,2.1,1.3,1.9,2.1,1.1]);
//    line.Set('chart.linewidth', 3);
//    line.Set('chart.colors', ['black']);
//    line.Set('chart.ymax', 10);
//    line.Set('chart.tickmarks', 'endcircle');
//    line.Set('chart.tooltips', ['h1','h2','h3','h4','h5','h6','h7']);
//
//    var combo = new RGraph.CombinedChart(bar, line);
//    combo.Draw();

    var pie = new RGraph.Pie('viz_canvas', [5,4,8,7,6,3,6]);
    pie.Set('chart.centerx', 550);
    pie.Set('chart.gutter.bottom', 250);
    pie.Set('chart.radius', 90);
    pie.Set('chart.labels', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER']);
    pie.Set('chart.tooltips', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER'] );
    pie.Draw();

    var hprogress = new RGraph.HProgress('viz_canvas', 0, 100, 0);
    hprogress.Set('chart.gutter.top', 450);
    hprogress.Set('chart.color', 'green');
    hprogress.Set('chart.adjustable', true);
    hprogress.Set('chart.margin', 5);
    hprogress.Set('chart.tickmarks.inner', true);
    hprogress.Set('chart.tickmarks.zerostart', true);
    hprogress.Set('chart.units.post', '%');
    hprogress.Draw();

    RGraph.AddCustomEventListener(hprogress, 'onadjustbegin', function () {console.log('Old value: ' + hprogress.value  );});
    RGraph.AddCustomEventListener(hprogress, 'onadjust', function () {console.log('Value during adjustment: ' + hprogress.value  );});
    RGraph.AddCustomEventListener(hprogress, 'onadjustend', function () {console.log('New value: ' + hprogress.value  );});


    var gauge = new RGraph.Gauge('viz_canvas', 0,100,77);
    gauge.Set('chart.adjustable', true);
    gauge.Set('chart.gutter.top', 300);
    gauge.Set('chart.centerx', 550);
    gauge.Set('chart.gutter.bottom', 100);
    gauge.Set('chart.radius', 90);
    gauge.Draw();

    RGraph.AddCustomEventListener(gauge, 'onadjustbegin', function (obj) {cl('START VALUE: ' + obj.value.toFixed(2));});
    RGraph.AddCustomEventListener(gauge, 'onadjust', function (obj) {cl('VALUE: ' + obj.value.toFixed(2));});
    RGraph.AddCustomEventListener(gauge, 'onadjustend', function (obj) {cl('END VALUE: ' + obj.value.toFixed(2));});

    var labels = ['h1','h2','h3','h4','h5','h6'];

    var bar2 = new RGraph.Bar("viz_canvas", [4.5,28,13,26,35,36]);
    bar2.Set('chart.tooltips', function (idx) {return labels[idx] + 's stats<br/><canvas id="__tooltip_canvas__" width="400" height="150">[No canvas support]</canvas>';});
    bar2.Set('chart.hmargin', 10);
    bar2.Set('chart.tickmarks', 'endcircle');
    bar2.Set('chart.colors', ['blue']);
    bar2.Set('chart.ymax', 100);
    bar2.Set('chart.labels', labels);
    bar2.Set('chart.gutter.top', 235);
    bar2.Set('chart.gutter.right', 300);
    bar2.Set('chart.gutter.bottom', 100);
    bar2.Draw();

    RGraph.AddCustomEventListener(bar2, 'ontooltip', CreateTooltipGraph);

    d1  = [];
    l   = 0; // The letter 'L' - NOT a one

    // Pre-pad the arrays with 250 null values
    for (var i=0; i<1000; ++i) {
        d1.push(null);
    }

    drawGraph();


}

function CreateTooltipGraph(obj)
    {
        // This data could be dynamic
        var line  = new RGraph.Line('__tooltip_canvas__', [5,8,7,6,9,5,4,6,3,5,4,4]);
        line.Set('chart.labels', ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']);
        line.Set('chart.hmargin', 5);
        line.Set('chart.tickmarks', 'endcircle');
        line.Set('chart.background.grid.autofit', true);
        line.Draw();
    }



function getGraph(id, d1)
{
    // After creating the chart, store it on the global window object
    if (!window.__rgraph_line__) {
        window.__rgraph_line__ = new RGraph.Line(id, d1);
        window.__rgraph_line__.Set('chart.xticks', 100);
        window.__rgraph_line__.Set('chart.background.barcolor1', 'rgba(255,255,255,0.1)');
        window.__rgraph_line__.Set('chart.background.barcolor2', 'rgba(255,255,255,0.1)');

//        window.__rgraph_line__.Set('chart.title.xaxis', 'Time >>>');
//        window.__rgraph_line__.Set('chart.title.yaxis', 'Bandwidth (MB/s)');
//        window.__rgraph_line__.Set('chart.title.vpos', 0.5);
//        window.__rgraph_line__.Set('chart.title', 'Bandwidth used');
//        window.__rgraph_line__.Set('chart.title.yaxis.pos', 0.5);
//        window.__rgraph_line__.Set('chart.title.xaxis.pos', 0.5);
        window.__rgraph_line__.Set('chart.colors', ['black']);
        window.__rgraph_line__.Set('chart.linewidth',0.5);
        //obj.Set('chart.ylabels.inside', true);
//        window.__rgraph_line__.Set('chart.yaxispos', 'right');
        window.__rgraph_line__.Set('chart.ymax', 100);
//        window.__rgraph_line__.Set('chart.xticks', 25);
        window.__rgraph_line__.Set('chart.filled', true);
        window.__rgraph_line__.Set('chart.gutter.top', 235);
        window.__rgraph_line__.Set('chart.gutter.right', 300);
        window.__rgraph_line__.Set('chart.gutter.bottom', 100);

        var grad = window.__rgraph_line__.context.createLinearGradient(0,0,0,250);
        grad.addColorStop(0, '#efefef');
        grad.addColorStop(0.9, 'rgba(0,0,0,0)');

        window.__rgraph_line__.Set('chart.fillstyle', [grad]);
    }

    return window.__rgraph_line__;
}

function drawGraph ()
{
//    RGraph.Clear(document.getElementById("viz_canvas"));

    var graph = getGraph('viz_canvas', d1);
    graph.Draw();

    // Add some data to the data arrays
    var r1 = RGraph.random(
                           RGraph.is_null(d1[d1.length - 1]) ? 26 : d1[d1.length - 1] - 2,
                           RGraph.is_null(d1[d1.length - 1]) ? 24 : d1[d1.length - 1] + 2
                          );
   r1 = Math.max(r1, 0);
   r1 = Math.min(r1, 50);

    d1.push(r1);

    if (d1.length > 250) {
        d1 = RGraph.array_shift(d1);
    }

    if (document.all && RGraph.isIE8()) {
        alert('[MSIE] Sorry, Internet Explorer 8 is not fast enough to support animated charts');
    } else {
        window.__rgraph_line__.original_data[0] = d1;
        setTimeout(drawGraph, 100);
    }
}


//ZOOM
//var canvas = document.getElementsByTagName('canvas')[0];
//canvas.width = 700; canvas.height = 500;
//window.onload = function(){
//    var ctx = canvas.getContext('2d');
//    trackTransforms(ctx);
//    var lastX=canvas.width/2, lastY=canvas.height/2;
//    var dragStart,dragged;
//
//
//    var scaleFactor = 1.1;
//    var zoom = function(clicks){
//        var pt = ctx.transformedPoint(lastX,lastY);
//        ctx.translate(pt.x,pt.y);
//        var factor = Math.pow(scaleFactor,clicks);
//        ctx.scale(factor,factor);
//        ctx.translate(-pt.x,-pt.y);
//        draw();
//    }
//
//    var handleScroll = function(evt){
//        var delta = evt.wheelDelta ? evt.wheelDelta/40 : evt.detail ? -evt.detail : 0;
//        if (delta) zoom(delta);
//        return evt.preventDefault() && false;
//    };
//    canvas.addEventListener('DOMMouseScroll',handleScroll,false);
//    canvas.addEventListener('mousewheel',handleScroll,false);
//};
//
//// Adds ctx.getTransform() - returns an SVGMatrix
//// Adds ctx.transformedPoint(x,y) - returns an SVGPoint
//function trackTransforms(ctx){
//    var svg = document.createElementNS("http://www.w3.org/2000/svg",'svg');
//    var xform = svg.createSVGMatrix();
//    ctx.getTransform = function(){ return xform; };
//
//    var savedTransforms = [];
//    var save = ctx.save;
//    ctx.save = function(){
//        savedTransforms.push(xform.translate(0,0));
//        return save.call(ctx);
//    };
//    var restore = ctx.restore;
//    ctx.restore = function(){
//        xform = savedTransforms.pop();
//        return restore.call(ctx);
//    };
//
//    var scale = ctx.scale;
//    ctx.scale = function(sx,sy){
//        xform = xform.scaleNonUniform(sx,sy);
//        return scale.call(ctx,sx,sy);
//        for (var i = 0; i < nodes.length; i += 1) {
//            var pos = nodes[i].get_pos();
//            var n_x = pos.x * sx;
//            var n_y = pos.y * sy;
//            nodes[i].set_pos({x : n_x),
//                              y : n_y);
//        }
//    };
//
//    var rotate = ctx.rotate;
//    ctx.rotate = function(radians){
//        xform = xform.rotate(radians*180/Math.PI);
//        return rotate.call(ctx,radians);
//    };
//    var translate = ctx.translate;
//    ctx.translate = function(dx,dy){
//        xform = xform.translate(dx,dy);
//        return translate.call(ctx,dx,dy);
//    };
//    var transform = ctx.transform;
//    ctx.transform = function(a,b,c,d,e,f){
//        var m2 = svg.createSVGMatrix();
//        m2.a=a; m2.b=b; m2.c=c; m2.d=d; m2.e=e; m2.f=f;
//        xform = xform.multiply(m2);
//        return transform.call(ctx,a,b,c,d,e,f);
//    };
//    var setTransform = ctx.setTransform;
//    ctx.setTransform = function(a,b,c,d,e,f){
//        xform.a = a;
//        xform.b = b;
//        xform.c = c;
//        xform.d = d;
//        xform.e = e;
//        xform.f = f;
//        return setTransform.call(ctx,a,b,c,d,e,f);
//    };
//    var pt  = svg.createSVGPoint();
//    ctx.transformedPoint = function(x,y){
//        pt.x=x; pt.y=y;
//        return pt.matrixTransform(xform.inverse());
//    }
//}