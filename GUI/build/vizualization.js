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
    var cvs  = document.getElementById("viz_canvas");
    var context = cvs.getContext('2d');

    var bar = new RGraph.Bar('viz_canvas', [5,4,8,7,6,3,6]);
    bar.Set('chart.gutter.top', 35);
    bar.Set('chart.labels', ['h1','h2','h3','h4','h5','h6','h7']);
    bar.Set('chart.tooltips', ['h1','h2','h3','h4','h5','h6','h7']);
    bar.Set('chart.gutter.right', 300);
    bar.Set('chart.gutter.bottom', 200);

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
    pie.Set('chart.gutter.bottom', 200);
    pie.Set('chart.radius', 90);
    pie.Set('chart.labels', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER']);
    pie.Set('chart.tooltips', ['HTTP','SSH','VIDEO','P2P','FTP','SMTP','OTHER'] );
    pie.Draw();


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