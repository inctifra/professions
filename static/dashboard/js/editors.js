if (document.getElementById("json-editor")) {
  import(/* webpackChunkName: "jsonEditor" */ "./editors/jsonEditor").then(({ default: initJsonEditor }) => {
    initJsonEditor();
  });
}
