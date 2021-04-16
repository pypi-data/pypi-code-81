graphNodeTypes = {"simpleCircle" : ("simpleCircle","SimpleCircle.png"), "doubleCircle" : ("doubleCircle","DoubleCircle.png"), "simpleDiamond" : ("simpleDiamond","SimpleDiamond.png"), "doubleDiamond" : ("doubleDiamond","DoubleDiamond.png")}
# JS-code for starting a canvas with graph-editing functionality
GRAPH_EDITOR ="""
if(typeof(HGGraphEditorNum) == "undefined"){HGGraphEditorNum = 0;} // note that this numbering deals with copies when reviewing answers

function HGGraphEditor(container, directedness, usedTypes){
   /* the container is used as a handle for the graph editor */

   container.innerHTML =""" + """'<style type="text/css">

  #graphEditorMenu' + HGGraphEditorNum + ' {
    position: fixed;
    z-index: 9999; /* Most times is 2000 used as middle */
    visibility: hidden;
    opacity: 0;
    
    padding: 0px;
    font-family: sans-serif;
    font-size: 11px;
    background: #fff;
    color: #555;
    border: 1px solid #C6C6C6;
    
    -webkit-transition: opacity .5s ease-in-out;
    -moz-transition: opacity .5s ease-in-out;
    transition: opacity .5s ease-in-out;
    
    -webkit-box-shadow: 2px 2px 2px 0px rgba(143, 144, 145, 1);
    -moz-box-shadow: 2px 2px 2px 0px rgba(143, 144, 145, 1);
    box-shadow: 2px 2px 2px 0px rgba(143, 144, 145, 1);
  }

  #graphEditorMenu' + HGGraphEditorNum + ' a {
    display: block;
    color: #555;
    text-decoration: none;
    padding: 6px 8px 6px 30px;
    width: 250px;
    position: relative;
  }

  #graphEditorMenu' + HGGraphEditorNum + ' a img,
  #graphEditorMenu' + HGGraphEditorNum + ' a i.fa {
    height: 20px;
    font-size: 17px;
    width: 20px;
    position: absolute;
    left: 5px;
    top: 2px;
  }

  #graphEditorMenu' + HGGraphEditorNum + ' a span {
    color: #BCB1B3;
    float: right;
  }

  #graphEditorMenu' + HGGraphEditorNum + ' a:hover {
    color: #fff;
    background: #3879D9;
  }

  #graphEditorMenu' + HGGraphEditorNum + ' hr {
    border: 1px solid #EBEBEB;
    border-bottom: 0;
  }
    
    #graphEditorNetwork' + HGGraphEditorNum + ' {
      width: 600px;
      height: 400px;
      background: #FFFFFF;
      border: 1px solid lightgray;
    }
  </style>
  <div id="graphEditorMenu' + HGGraphEditorNum + '">
      <a href="#n" class="HGGraphControl" onclick="HGElement(\\'graphEditorNetwork' + HGGraphEditorNum + '\\').HGEraseElement()">
        Löschen (Muss zweifach geklickt werden!)
      </a>
      <a href="#n" class="HGGraphControl"  onclick="HGElement(\\'graphEditorNetwork' + HGGraphEditorNum + '\\').HGChangeType()">
  Art ändern
      </a>
  </div>

  <div id="graphEditorNetwork' + HGGraphEditorNum + '"></div>'""".replace("\n","\\n") + """

  var nodes = [];
  var edges = [];

  var edgeStyles = ['to', 'from', 'to,from', '']; // warning, this will get cut down in the lines right below depending on the directedness of the graph
  if(directedness == "directed"){ // arrow to and arrows from
    edgeStyles = edgeStyles.slice(0, 2);
  }
  else if(directedness == "undirected"){ // only ''
    edgeStyles = edgeStyles.slice(3, 4);
  }
  else{ // in all other cases use any
    edgeStyles = edgeStyles.slice(0, 3); // arrows to, from or both
  }

  var nodePicNames = [];
  var nodePics = [];
  var nodePicNamesReverse = {};

  for (pic of usedTypes){
    nodePicNames.push(pic[0]);
    nodePics.push(pic[1]);
  }

  for (var a = 0; a < nodePicNames.length; a++){
    nodePicNamesReverse[nodePicNames[a]] = a; 
  }

  var fontOffset = -40; // assuming 100px x 100px images this offset puts the labels into the centre of the image

  nodes = new vis.DataSet(nodes);
  edges = new vis.DataSet(edges);

  // create a network
  var networkContainer = HGElement('graphEditorNetwork' + HGGraphEditorNum);
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {};
  var network = new vis.Network(networkContainer, data, options);

  var selfReferenceNumbers = {};
  var selfReferenceWarningGiven = false;

  function selfReferenceRadius(num){
    console.log(num);
    console.log(selfReferenceNumbers);
    if(!selfReferenceWarningGiven && num > 4){
      alert("Warnung:\\nZu viele Schleifen an einem Knoten führen zu einer eigenartigen Darstellung.")
      selfReferenceWarningGiven = true;
    } 
    return (15 * num);
  }

  // counts number of self-references for all nodes and assigns radii to loops, with given id only refreshes one node
  function manageSelfReferences(id = null){
    if(id == null){
      selfReferenceNumbers = {};
      var gNodes = nodes.get();
      for(var a = 0; a < gNodes.length; a++){
        selfReferenceNumbers[gNodes[a].id] = 0
      }
    }
    else{
      selfReferenceNumbers[id] = 0;
    }
    var gEdges;
    if(id == null){
      gEdges = edges.get();
    }
    else{
      gEdges = network.getConnectedEdges(id);
      for(var a = 0; a < gEdges.length; a++){
        gEdges[a] = edges.get(gEdges[a]); // from ids to complete edges
      }
    }
    for(var a = 0; a < gEdges.length; a++){
      if(gEdges[a].from == gEdges[a].to){
        selfReferenceNumbers[gEdges[a].from] = (++selfReferenceNumbers[gEdges[a].from] || 1);
        edges.update({id : gEdges[a].id, selfReference : {size : selfReferenceRadius(selfReferenceNumbers[gEdges[a].from])}});
      }
    }
  }

  var erasePrimed = false;
  var lastSelected = undefined;
  var hasSelectedNodes = function(){
    return network.getSelectedNodes().length != 0;
  }
  
  networkContainer.HGEraseElement = function(){ // note: this assumes selection of at most one element
    if(erasePrimed == true){
      if(network.getSelection().nodes.length != 0){
        network.deleteSelected();
      }
      else if (network.getSelection().edges.length != 0){
        var delEdge = network.getSelection().edges[0];
        var fr = delEdge.from;
        var to = delEdge.to;
        network.deleteSelected();
        if(fr == to){
          manageSelfReferences(to);
        }
      }
      menuStyle.visibility = "hidden";
      erasePrimed = false;
    }
    else{
      erasePrimed = true;
    }
  }
  
  networkContainer.HGChangeType = function(){
    if(hasSelectedNodes()){
      var sel = network.getSelectedNodes()[0];
      var useStyle = (nodes.get(sel).HGType + 1) % nodePics.length;
      nodes.update([{id : sel, HGType : useStyle, image : nodePics[useStyle]}]);
    }
    else{
      var sel = network.getSelectedEdges()[0];
      var useStyle = (edges.get(sel).HGType + 1) % edgeStyles.length;
      edges.update([{id : sel, HGType : useStyle, arrows : edgeStyles[useStyle]}]);
    }
  }

  var selectAt = function(e, select = true){
    var sel = network.getNodeAt(e.pointer.DOM);
    if(sel != undefined){
      if(select){
        network.selectNodes([sel]);
      }
    }
    else{
      sel = network.getEdgeAt(e.pointer.DOM);
      if(sel != undefined){
        if(select){
          network.selectEdges([sel]);
        }
      }
      else{
        return undefined;
      }
    }
    return sel;
  }
  
  
  //context menu modified from one made by Stephan Stanisic (license free)
  var menuStyle = HGElement('graphEditorMenu' + HGGraphEditorNum).style;
  network.addEventListener('oncontext', function(e) {
    menuStyle.visibility = "hidden";
    
    if(!selectAt(e)){
      return;
    }

    var posX = e.event.clientX;
    var posY = e.event.clientY;
    menu(posX, posY);
    catchEv = e;
  }, false);

  container.addEventListener('contextmenu', function(e) {
    e.preventDefault();
  }, false);
  
  nodeIDCounter = 1;

  // nodes must be unfixed and fixed when moving them by dragging
  network.on('dragEnd', function (e) {
    var nodeId = selectAt(e, false);
    if(typeof nodeId != "undefined"){
      nodes.update({id: nodeId, fixed: true});
    }
  });
  network.on('dragStart', function(e) {
    var nodeId = selectAt(e, false);
    if(typeof nodeId != "undefined"){
      nodes.update({id: nodeId, fixed: false});
      lastSelected = nodeId;
    }
  });

  network.addEventListener('click', function(e) {
    var madeCon = false;
    if(e.event.changedPointers[0].shiftKey){
      var selA = lastSelected;
      var selB = selectAt(e, false);
      if(selA && selB){
        edges.add([{from : selA, to : selB, arrows : "to", HGType : 0, label : ""}])
        if(selA == selB){
          manageSelfReferences(selA);
        }
        network.selectNodes([lastSelected])
        madeCon = true;
      }
    }
    if(!madeCon){
      lastSelected = network.getSelectedNodes()[0];
    }
    menuStyle.opacity = "0";
    erasePrimed = false;
    menuStyle.visibility = "hidden";
  }, false);
  network.addEventListener('doubleClick', function(e) {
    var sel = network.getNodeAt(e.pointer.DOM);
    if(sel != undefined){
      var newLabel = prompt("Beschriftung eintragen:", nodes.get(sel).label) || nodes.get(sel).label;
      nodes.update({id : sel, label : newLabel});
    }
    else{
      sel = network.getEdgeAt(e.pointer.DOM);
      if(sel != undefined){
        var newLabel = prompt("Beschriftung eintragen:", edges.get(sel).label) || edges.get(sel).label;
        edges.update({id : sel, label : newLabel});
      }
      else{
        nodes.add([{id : nodeIDCounter, x : e.pointer.canvas.x, y : e.pointer.canvas.y, label:'Knoten', shape:'image', HGType:0, image: nodePics[0], font : {vadjust : fontOffset}, fixed : true}]);
        nodeIDCounter += 1;
      }
    }
  }, false);

  var menu = function(x, y) {
    menuStyle.top = y + "px";
    menuStyle.left = x + "px";
    menuStyle.visibility = "visible";
    menuStyle.opacity = "1";
  }


  // Note: due to the encoding/decoding used when saving and loading, using utf-16 code points for saving and loading did not work properly the last time I tried (the inputs were different in the results screen)

  var fromStringWithLength = function(inp, pos, lenLen){
    var len = parseInt(inp.slice(pos, pos + lenLen), 36);
    pos += lenLen;
    var out = inp.slice(pos, pos + len);
    return [len + lenLen, out];
  }

  container.HGRefit = function(){
    network.fit();
  }

  var replaceGraphContents = function(newNodes, newEdges){
    nodes.clear();
    edges.clear();
    for(var a = 0; a < newNodes.length; a++){
      nodes.add(newNodes[a]);
    }
    for(var a = 0; a < newEdges.length; a++){
      edges.add(newEdges[a]);
    }
    network.redraw();
    container.HGRefit();
  }

  container.HGSetter = async function(inp){
    var dPos = 0;
    var readPos = 0;
    var nodeNum;
    [dPos, nodeNum] = fromStringWithLength(inp, readPos, 1);
    nodeNum = parseInt(nodeNum);
    readPos += dPos;
    var newNodes = [];
    for(var a = 0; a < nodeNum; a++){
      var useX, useY, useID, useType, useLabel;
      [dPos, useX] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useY] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useID] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useType] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useLabel] = fromStringWithLength(inp, readPos, 2);
      readPos += dPos;
      newNodes.push({x : parseInt(useX), y : parseInt(useY), id : parseInt(useID), HGType : parseInt(useType), label : useLabel, font : {vadjust : fontOffset}, shape : "image", image : nodePics[parseInt(useType)], fixed : true});
    }

    var edgeNum;
    [dPos, edgeNum] = fromStringWithLength(inp, readPos, 1);
    edgeNum = parseInt(edgeNum);
    readPos += dPos;
    var newEdges = [];
    for(var a = 0; a < edgeNum; a++){
      var useFrom, useTo, useType, useLabel;
      [dPos, useFrom] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useTo] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useType] = fromStringWithLength(inp, readPos, 1);
      readPos += dPos;
      [dPos, useLabel] = fromStringWithLength(inp, readPos, 2);
      readPos += dPos;
      newEdges.push({from : parseInt(useFrom), to : parseInt(useTo), HGType : parseInt(useType), label : useLabel, arrows : edgeStyles[parseInt(useType)]});
    }
    replaceGraphContents(newNodes, newEdges);
    manageSelfReferences();
  };

  var toStringWithLength = function(inp, lenLen){
    inp = String(inp);
    var inpLen = (inp.length).toString(36);
    inpLen = "0".repeat(lenLen - inpLen.length) + inpLen;
    return inpLen + inp;
  }  

  container.HGGetter = function(){
    var out = "";
    var saveNodes = nodes.get();
    var nodePositions = network.getPositions();
    out += toStringWithLength(saveNodes.length,1);
    for(var a = 0; a < saveNodes.length; a++){
      var curNode = saveNodes[a];
      var curPos = nodePositions[curNode.id]
      out += toStringWithLength(Math.round(curPos.x), 1);
      out += toStringWithLength(Math.round(curPos.y), 1);
      out += toStringWithLength(curNode.id, 1);
      out += toStringWithLength(curNode.HGType, 1);
      out += toStringWithLength(curNode.label, 2);
    }
    var saveEdges = edges.get();
    out += toStringWithLength(saveEdges.length, 1);
    for(var a = 0; a < saveEdges.length; a++){
      var curEdge = saveEdges[a];
      out += toStringWithLength(curEdge.from, 1);
      out += toStringWithLength(curEdge.to, 1);
      out += toStringWithLength(curEdge.HGType, 1);
      out += toStringWithLength(curEdge.label, 2);
    }
    return out;
  };

  container.HGSetGraph = async function(inp, stabilize = false){
    var newNodes = [];
    var newEdges = [];
    var getNodes = inp.nodes;
    var getEdges = inp.edges;
    for(var a = 0; a < getNodes.length; a++){
      var curNode = getNodes[a];
      var useType = nodePicNamesReverse[curNode.type];
      var newNode = {id : curNode.id + 1, HGType :useType, label : curNode.label, font : {vadjust : fontOffset}, shape : "image", image : nodePics[useType], fixed : !stabilize} // note the conversion between nodeIds going up from 0 and going up from 1 (the id 0 causes problems with visjs)
      if(curNode.x != undefined && curNode.y != undefined){
        newNode["x"] = curNode.x;
        newNode["y"] = curNode.y;
      }
      newNodes.push(newNode);
    }
    for(var a = 0; a < getEdges.length; a++){
      var curEdge = getEdges[a];
      var useType = 0;
      if(directedness != "undirected" && curEdge.bidirectional){
        useType = 2;
      }
      newEdges.push({from : curEdge.from + 1, to : curEdge.to + 1, arrows : edgeStyles[useType], HGType : useType, label : curEdge.label})
    }
    if(stabilize){
      network.setOptions({physics: {enabled : true}});
      replaceGraphContents(newNodes, newEdges);
      await (new Promise(resolve => setTimeout(resolve, 5000)));
      network.setOptions({physics: {enabled : false}});
      var gNodes = nodes.get();
      for(var a = 0; a < gNodes.length; a++){
        nodes.update({id : gNodes[a].id, fixed : true});
      }
    }
    else{
      replaceGraphContents(newNodes, newEdges);
    }
    manageSelfReferences();
  }

  container.HGGetGraph = function(){
    var convNodes = [];
    var convEdges = [];
    var edgeList = {forwards : {}, backwards : {}};
    var getNodes = nodes.get();
    var getEdges = edges.get();
    var reID = {}; // nodes get renumbered so the IDs are easier to deal with
    var curID = 0;
    var nodePositions = network.getPositions();
    for(var a = 0; a < getNodes.length; a++){
      edgeList["forwards"][a] = [];
      edgeList["backwards"][a] = [];
      var curNode = getNodes[a];
      reID[curNode.id] = curID;
      var curPos = nodePositions[curNode.id]
      convNodes.push({'id' : curID, 'label' : curNode.label, 'type' : nodePicNames[curNode.HGType], 'x' : curPos.x, 'y' : curPos.y})
      curID++;
    }
    for(var a = 0; a < getEdges.length; a++){
      var curEdge = getEdges[a];
      var directed = !(curEdge.arrows == 'to,from' || curEdge.arrows == '');
      var from = reID[curEdge.from];
      var to = reID[curEdge.to];
      if(curEdge.arrows == 'from'){
        var tmp = from;
        from = to;
        to = tmp;
      }
      edgeList["forwards"][from].push(a);
      edgeList["backwards"][to].push(a);
      if(!directed){
        edgeList["forwards"][to].push(a);
        edgeList["backwards"][from].push(a);
      }
      convEdges.push({'from' : from, 'to' : to, 'label' : curEdge.label, 'bidirectional' : !directed});
    }
    return {"nodes" : convNodes, "edges" : convEdges, "edgeList" : edgeList}
  }

  HGGraphEditorNum++;
  return container;
}
"""
