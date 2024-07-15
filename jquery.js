/* javascript to accompany jquery.html */
$(document).ready(
  /* this defines a function that gets called after the document is in memory */
  function () {
    var cue = false;

    $(document).on('mousedown', "circle[fill='WHITE']",
      function () {
        cue = true;
        console.log("cue is in mousedown" + cue);
      });

    $("*").mousemove(function (event) {
      // Calculate angle and length of line
      var cueBallX = $("circle[fill='WHITE']").offset().left + $("circle[fill='WHITE']").attr("r") / 2;
      var cueBallY = $("circle[fill='WHITE']").offset().top + $("circle[fill='WHITE']").attr("r") / 2;

      var deltaX = event.pageX - cueBallX;
      var deltaY = event.pageY - cueBallY;
      var length = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      //console.log("deltaX is " + deltaX + " and deltaY is " + deltaY + " and cue is " + cue);
      $('#line').remove();
      var cueX = $("circle[fill='WHITE']").attr("cx");
      var cueY = $("circle[fill='WHITE']").attr("cy");

      var newElement = document.createElementNS("http://www.w3.org/2000/svg", 'line'); //Create in SVG's namespace
      newElement.setAttribute("x1", cueX);
      newElement.setAttribute("y1", cueY);
      if (deltaX < 0) {
        newElement.setAttribute("x2", cueX - (Math.sqrt(deltaX * deltaX)));
      } else {
        newElement.setAttribute("x2", cueX - -(Math.sqrt(deltaX * deltaX)));
      }
      if (deltaY < 0) {
        newElement.setAttribute("y2", cueY - (Math.sqrt(deltaY * deltaY)));
      } else {
        newElement.setAttribute("y2", cueY - -(Math.sqrt(deltaY * deltaY)));
      }
      newElement.setAttribute("id", "line");
      newElement.setAttribute("style", "stroke:red;stroke-width:5")

      if (cue) {
        $('#svgPoolTable').append(newElement);
        $("#line").css({
          transformOrigin: '0 0',
        });

        $('#valx').remove();
        $('#valy').remove();

        /*if (($("#line").attr("x2") - cueX)*9 > 10000) {
          $('<div id="valx">' + 10000 + '</div>').appendTo("#xVel");
          $('<div id="valy">' + 10000 + '</div>').appendTo("#yVel");
          document.getElementById("xInput").value = 10000;
          document.getElementById("yInput").value = 10000;*/
        //} else {
          $('<div id="valx">' + ($("#line").attr("x2") - cueX)*9 + '</div>').appendTo("#xVel");
          $('<div id="valy">' + ($("#line").attr("y2") - cueY)*9 + '</div>').appendTo("#yVel");
          document.getElementById("xInput").value = ($("#line").attr("x2") - cueX)*9;
          document.getElementById("yInput").value = ($("#line").attr("y2") - cueY)*9;
        //}
      }

    });


    $(this).mouseup(
      function () {
        if (cue) {
          $('#line').remove();
          $('#shootScript').remove();
          getTurn(submitValues);
          //document.getElementById("shot").submit();
          //$("#poolTable").load("table-1.svg", alert( 'better?' ) );

          //submitValues(makeShot);

          //makeShot();
          //intervalID = setInterval(makeShot, 500);
        }
        //cue = false;
        //console.log("cue is in mouseup" + cue);
      });

      function getTurn (submitValues) {
        //$('#playerTurn').remove();
        //$('<div id="playerTurn">' + $("#player1Name").text() + '</div>').appendTo("#currentTurn");
        document.getElementById("current").value = $("#currentTurn").text();
        submitValues();
      }

      function submitValues() {
        document.getElementById("shot").submit();
      }

  });  
