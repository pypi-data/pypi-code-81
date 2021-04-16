VARIABLE_TABLE_ROW_SEPARATOR = "HGJSVARIABLETABLEROWSEPARATOR";
VARIABLE_TABLE_COLUMN_SEPARATOR = "HGJSVARIABLETABLECOLUMNSEPARATOR";

VARIABLE_TABLE = """
if(typeof(HGVariableTableNum) == "undefined"){HGVariableTableNum = 0;} // note that this numbering deals with copies when reviewing answers

function HGVariableTable(container, baseX, baseY, defaultEntry){
  var currentNum = HGVariableTableNum;
  container.innerHTML = '""" + """
<style type="text/css">
.HGVTableDatColumn{num}{
  float: left;
  width: 90%;
}

.HGVTableNavColumn{num}{
  float: left;
  width: 10%;
}

.HGVTableRow{num}:after{
  content: "";
  display: table;
  clear: both;
}

</style>
<div id = "HGVTableContainer{num}" class = "HGVTableRow{num}">
<div class = "HGVTableNavColumn{num}">
<p align = "center">
<button type = "button" onclick="HGElement(\\'HGVTableContainer{num}\\').extendY()">Y+</button>
</p>
<p align = "center">
<button type = "button" onclick="HGElement(\\'HGVTableContainer{num}\\').shrinkX()">X-</button> 
<button type = "button" onclick="HGElement(\\'HGVTableContainer{num}\\').extendX()">X+</button>
</p>
<p align = "center">
<button type = "button" onclick="HGElement(\\'HGVTableContainer{num}\\').shrinkY()">Y-</button>
</p>
</div>
<div class = "HGVTableDatColumn{num}">
</div>
</div>
""".replace("\n","\\n") + """'.replace(/{num}/g, currentNum)

  var innerContainer = HGElement("HGVTableContainer" + currentNum)

  var values = [[defaultEntry]] // note we start with a 1x1 table, so the steps which read the DOM do not need to detect a size of 0 in any dimension
  var xSize = 1;
  var ySize = 1;
  var rowSeparator = '""" + VARIABLE_TABLE_ROW_SEPARATOR + """';
  var columnSeparator = '""" + VARIABLE_TABLE_COLUMN_SEPARATOR + """';
  function readEntries(){
    var rows = innerContainer.children[1].children[0].children[0].children; // container (with control buttons and table) -> right part (table) -> body -> rows
    for(var y = 0; y < ySize; y++){
    var cells = rows[y].children;
    for(var x = 0; x < xSize; x++){
      values[x][y] = cells[x].children[0].value; // cell -> input -> value
    }
    }
    values;
  }
  function reDisplay(){
    var tableContent = "<table>";
    for(var y = 0; y < ySize; y++){
    tableContent += "<tr>"
    for(var x = 0; x < xSize; x++){
      var insertValue = values[x][y].replace(/"/g,'&#34;').replace(/'/g,"&#39;") // escape quotation marks so they do not interfere with the DOM attributes in the next step
      tableContent += '<th><input class="ilc_qinput_TextInput" type="text" spellcheck="false" autocomplete="off" autocorrect="off" value="' + insertValue + '" autocapitalize="off" size = 10></th>'
    }
    tableContent += "</tr>"
    }
    tableContent += "</table>";
    innerContainer.children[1].innerHTML = tableContent; // container -> right part (table)
  }
  innerContainer.extendX = function(){
    readEntries();
    if(values.length < xSize + 1){
    values.push([]);
    }
    while(values[xSize].length < ySize){
    values[xSize].push(defaultEntry);
    }
    xSize += 1;
    reDisplay();
  }
  innerContainer.extendY = function(){
    readEntries();
    ySize += 1;
    for(var x = 0; x < xSize; x++){
    while(values[x].length < ySize){
      values[x].push(defaultEntry);
    }
    }
    reDisplay();
  }
  innerContainer.shrinkX = function(){
    readEntries();
    xSize = Math.max(1, xSize - 1);
    reDisplay();
  }
  innerContainer.shrinkY = function(){
    readEntries();
    ySize = Math.max(1, ySize - 1);
    reDisplay();
  }

  reDisplay(); // just to set up the dom for readEntries() during expansion

  for(var x = 0; x < baseX - 1; x++){ // rather inefficient way of getting to initial size, should be changed at some point
    innerContainer.extendX();
  }
  for(var y = 0; y < baseY - 1; y++){
    innerContainer.extendY();
  }

  container.HGGetter = function(){
    readEntries();
    var output = "";
    var firstX = true;
    for(var x = 0; x < xSize; x++){
      if(!firstX){
        output += columnSeparator;
      }
      firstX = false;
      var firstY = true;
      for(var y = 0; y < ySize; y++){
        if(!firstY){
          output += rowSeparator;
        }
        firstY = false;
        output += values[x][y];
      }
    }
    return output;
  }
  container.HGSetter = function(value){
    values = [];
    var columns = value.split(columnSeparator);
    xSize = columns.length;
    for(var x = 0; x < xSize; x++){
    values.push([]);
    var rows = columns[x].split(rowSeparator);
    ySize = rows.length; // should write the same value over and over again, but performance impact should be relatively low (even compared to alternatives)
    for(var y = 0; y < ySize; y++){
      values[x].push(rows[y]);
    }
    }
    reDisplay();
  }
  container.HGGetEntries = function(){
    readEntries();
    var valCopy = [];
    for(var x = 0; x < xSize; x++){
    valCopy.push(values[x].slice(0, ySize));
    }
    return valCopy;
  }
  container.HGSetEntries = function(newVals){
    values = [];
    xSize = newVals.length;
    ySize = newVals[0].length;
    for(var x = 0; x < xSize; x++){
    values.push([...newVals[x]]);
    }
    reDisplay();
  }
  return container;
}
"""
