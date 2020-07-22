/**
 * Created by Marcin Wykret / dismedia on 04/09/2014.
 */


var gradientEditor=function(resX,resY,container){

    var biObject=bi(resX,resY,container);

    var canvas=biObject.getCanvas();

    var currentR,currentG,currentB;


    var setCurrentColor=function(cr,cg,cb){
        currentR=cr;
        currentG=cg;
        currentB=cb;

    }


    /*var init=function(){

        // Color created when clicking a spot on the gradient
        setCurrentColor(255,255,0);

        jQuery(canvas).click(function(e){

            var offset_t = $(this).offset().top - $(window).scrollTop();
            var offset_l = $(this).offset().left - $(window).scrollLeft();

            var left =  (e.clientX - offset_l)/resX;
            var top =    (e.clientY - offset_t)/ resY;

            createEditPoint(left,top,currentR,currentG,currentB)

        });

    }*/

    var createEditPoint=function(x,y,r,g,b){


        var point=biObject.addPoint(x,y,r,g,b);
        var indicator=jQuery('<div class="colorIndiactor" style="position:absolute;"></div>');

        //debugger;
        // don't need the individual point rects
        /*var jIndicator= jQuery(indicator);

        jIndicator.css("position","absolute");
        jIndicator.css("top",y*resY-5);
        jIndicator.css("left",x*resX-5);
        jIndicator.css("width",10);
        jIndicator.css("height",10);
        jIndicator.css("border-top","black solid 1px");
        jIndicator.css("border-bottom","black solid 1px");
        jIndicator.css("border-left","white solid 1px");
        jIndicator.css("border-right","white solid 1px");
        jIndicator.css("background","rgb("+r+","+g+","+b+")");

        jQuery(container).append(indicator);

       jIndicator.click(function(e){

            biObject.removePoint(point);
            jIndicator.remove();

           delete  jIndicator;
        });*/


    }

    //init();


    // declaring the points and its colors here.
    /*
    *   let's say we had 8 points of interest
    *   provide the x,y and the rgb for each in a list
    *   and loop thru the list to createEditPoint
    */



    return {
        setCurrentColor:setCurrentColor
    }
}
