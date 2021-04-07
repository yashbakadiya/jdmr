editableGrid = new EditableGrid("DemoGridAttach");
// we build and load the metadata in Javascript
editableGrid.load({
  metadata: [
    { name: "id", datatype: "integer", editable: false },
    { name: "coursename", datatype: "string", editable: true },
    {
      name: "class", datatype: "string", editable: true
    },
    { name: "archived", datatype: "boolean", editable: true }
  ]
});

// then we attach to the HTML table and render it
editableGrid.attachToHTMLTable('htmlgrid');
editableGrid.renderGrid();