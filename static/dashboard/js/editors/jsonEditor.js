import "../../css/editors/jsonEditor.css";

export default function initJsonEditor() {
  Promise.all([
    import("jsoneditor/dist/jsoneditor.css"),
    import("jsoneditor")
  ]).then(([_, module]) => {
    const JSONEditor = module.default;
    const container = document.getElementById("payloadEditor");
    const options = { mode: 'code', modes: ['code', 'tree'] };
    if (container) {
        const editor = new JSONEditor(container, options)
        editor.set({
            "name": "Jeckonia Kwasa",
            "license_no": "Hello World"
        });
             document
        .getElementById("simulateApiForm")
        .addEventListener("submit", function (e) {
          e.preventDefault();
          const json = editor.get();
          alert(JSON.stringify(json, null, 2));
        });
    };
  });
}

