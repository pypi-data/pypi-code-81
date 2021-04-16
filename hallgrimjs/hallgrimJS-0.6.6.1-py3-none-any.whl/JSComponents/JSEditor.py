# JS-code for starting an ACE-editor (source-code-editor).
CODE_EDITOR = """ 
if(typeof(HGEditorNum) == "undefined"){HGEditorNum = 0;} // note that this numbering deals with copies when reviewing answers


function HGEditor(container, language){
/**
* Creates an editor inside the given container (replaces inner HTML) with highlighting in the given language.
*/
  container.innerHTML = "<div id=HGInnerEditor" + HGEditorNum + "></div>"; // container used as a handle
  var editor = ace.edit("HGInnerEditor" + HGEditorNum);
  editor.setTheme("ace/theme/monokai");
  editor.session.setMode("ace/mode/" + language);
  editor.setOptions({minLines: 10, maxLines: 10000}); // maxLines have to be set, else always size of about one line
  editor.setFontSize(16);
  container.editor = editor;
  HGEditorNum += 1;
  return container;
}
"""
