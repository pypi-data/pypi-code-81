# JS-code for starting a canvas with drawing functionality
DRAWING_CANVAS = """ 
if(typeof(HGCanvasNum) == "undefined"){HGCanvasNum = 0;} // note that this numbering deals with copies when reviewing answers

function HGDrawingCanvas(container, useWidth, useHeight, maxStack){
/**
* Creates a canvas with drawing functionality inside the given container (replaces inner HTML) along with UI-components.
*/
  container.innerHTML = // container used as as handle
    "<canvas id = 'HGDrawingCanvas" + HGCanvasNum + "' width='" + useWidth + "' height='" + useHeight + "' style = 'border:2px solid;'></canvas>"
    +"<div style = 'float:left; width:250px; padding:10px;'>" // column
    +"<p>Farbe:</p>"
    +"<input id = 'HGDrawingCanvasColorPicker" + HGCanvasNum + "' type = 'color' value = '#009000'>"
    +"<p>Strichstärke:</p>"
    +"<input id = 'HGDrawingCanvasLineSizeRange" + HGCanvasNum + "' type = 'range' min = '1' max = '20' style = 'width:80%;'>"
    +"<input id = 'HGDrawingCanvasUndo" + HGCanvasNum + "' type = 'button' value = 'Rückgängig machen' size = '23' onclick = 'HGElement(\\"HGDrawingCanvas" + HGCanvasNum + "\\").HGUndo()'>"
    +"<input id = 'HGDrawingCanvasRedo" + HGCanvasNum + "' type = 'button' value = 'Wiederherstellen' size = '23' onclick = 'HGElement(\\"HGDrawingCanvas" + HGCanvasNum + "\\").HGRedo()'>"
    +"<input id = 'HGDrawingCanvasClear" + HGCanvasNum + "' type = 'button' value = 'Löschen' size = '23' onclick = 'HGElement(\\"HGDrawingCanvas" + HGCanvasNum + "\\").HGClear()'>"
    +"<p>Werkzeug:</p>"
    +"<input type='radio' name='HGDrawingCanvasToolSelector" + HGCanvasNum + "' value='pencil' checked='checked'>Stift<br>" // note that pencil is selected by default (additional enforcement through checked attribute)
    +"<input type='radio' name='HGDrawingCanvasToolSelector" + HGCanvasNum + "' value='textStamp'>Textstempel<br>"
    +"<input id = 'HGDrawingCanvasTextInput" + HGCanvasNum + "'  class='ilc_qinput_TextInput' type='text' spellcheck='false' autocomplete='off' autocorrect='off' autocapitalize='off' size='25' maxlength='100' value = 'Hier Text zum Stempeln eingeben!'>" // class copied from ILIAS
    +"</div>"
  var picker = HGElement("HGDrawingCanvasColorPicker" + HGCanvasNum);
  var canvas = HGElement("HGDrawingCanvas" + HGCanvasNum);
  var clearer = HGElement("HGClearDrawingCanvas" + HGCanvasNum);
  var context = canvas.getContext("2d");
  var slider = HGElement("HGDrawingCanvasLineSizeRange" + HGCanvasNum);
  var toolSelectors = document.getElementsByName("HGDrawingCanvasToolSelector" + HGCanvasNum);
  var textInput = HGElement("HGDrawingCanvasTextInput" + HGCanvasNum);
  var drawingMode = "pencil";
  textInput.style.display = "none"; // hide input for text stamp in beginning (pencil is selected by default)
  var toolSelectionProcessor = function() { // to be called on change of selected tool
    drawingMode = this.value;
    switch(this.value){
      case "pencil":
        textInput.style.display = "none";
        break;
      case "textStamp":
        textInput.style.display = "";
        break;
      default:
    }
  }
  for (var tool = 0; tool < toolSelectors.length; tool++){
    toolSelectors[tool].addEventListener('change', toolSelectionProcessor);
  }
  canvas.HGUndoPoints = []; // every time something is drawn the picture is pushed onto this list (acts as stack) beforehand
  canvas.HGRedoPoints = []; // on every undo the undone picture is pushed onto this list (acts as stack) and it is emptied whenever something is drawn
  var drawing = false; // indicates whether currently drawing, notice closure

  var pushToUndo = function () {
    canvas.HGUndoPoints.push(canvas.toDataURL());
    if(canvas.HGUndoPoints.length == maxStack + 1){ // note, that when maxStack == -1 this will allow an infinite stack
      canvas.HGUndoPoints.shift();
    }
    canvas.HGRedoPoints = [];
  }

  var mouseProcessor = function (type, event) { // used for processing mouse inputs on the canvas
    var mpx = event.clientX - canvas.getClientRects()[0].x;//mouse positions
    var mpy = event.clientY - canvas.getClientRects()[0].y;
    switch(drawingMode){
      case "pencil":
        if (type == 'move') { // mouse moved
          if (drawing) { // if currently drawing, draw line
            prevX = currX;
            prevY = currY;
            currX = mpx;
            currY = mpy;
            context.strokeStyle = picker.value;
            context.lineWidth = slider.value;
            context.lineTo(currX, currY);
            context.stroke();
          }
        }
        else if (type == 'down') { // start to draw when mouse pressed
          currX = mpx;
          currY = mpy;
          pushToUndo();
          drawing = true;
          context.beginPath();
          context.lineJoin = "round"; // important to avoid weird spiky lines
        }
        else if (type == 'up' || type == "out") { // moved out of canvas or stopped pressing mouse, stop drawing
          context.closePath();
          drawing = false;
        }
        break;
      case "textStamp":
        if (type == 'down') { // start to draw when mouse pressed
          pushToUndo();
          context.font = slider.value * 2 + "px Arial"; // Arial assumed to always be available, multiplier to get a reasonable range for text sizes
          context.fillStyle = picker.value;
          context.fillText(textInput.value, mpx, mpy); 
        }
        break;
    }
  }
  canvas.addEventListener("mousemove", function (event) {
      mouseProcessor('move', event)
    },
    false);
  canvas.addEventListener("mousedown", function (event) {
        mouseProcessor('down', event)
    },
    false);
  canvas.addEventListener("mouseup", function (event) {
        mouseProcessor('up', event)
    },
    false);
  canvas.addEventListener("mouseout", function (event) {
        mouseProcessor('out', event)
    },
    false);
  container.HGGetter = function() {
    return canvas.toDataURL();
  }
  container.HGSetter = async function(dataURL) {
    var img = new Image;
    img.onload = function(){context.drawImage(img, 0, 0)};
    img.src = dataURL;
  }
  canvas.HGUndo = function(){
    if(canvas.HGUndoPoints.length != 0){
      canvas.HGRedoPoints.push(canvas.toDataURL());
      container.HGSetter(canvas.HGUndoPoints.pop());
    }
    else{
      alert("Kein Schritt kann rückgängig gemacht werden!")
    }
  }
  canvas.HGRedo = function(){
    if(canvas.HGRedoPoints.length != 0){
      canvas.HGUndoPoints.push(canvas.toDataURL());
      container.HGSetter(canvas.HGRedoPoints.pop());
    }
    else{
      alert("Kein Schritt kann wiederhergestellt werden!")
    }
  }
  canvas.HGClear = function(){
    context.rect(0, 0, canvas.width, canvas.height); // doing this only once sometimes results in only partial results (???), twice alway worked, so we do it three times
    context.rect(0, 0, canvas.width, canvas.height);
    context.rect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "white";
    context.fill();
  }
  canvas.HGClear(true); // initially fully white
  HGCanvasNum += 1;
  return container;
}
"""
