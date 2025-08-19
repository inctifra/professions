import "../../css/editors/jsonEditor.css";

export default function initJsonEditor() {
  Promise.all([
    import("jsoneditor/dist/jsoneditor.css"),
    import("jsoneditor")
  ]).then(async ([_, module]) => {
    let PK_API_KEY = null;
    const JSONEditor = module.default;
    const {default: Choices} = await import("choices.js");
    const {default: axiosInstance} = await import("../libs/main");
    const { presetChoices } = await  import("../forms/projects/snippets");

    const apiKeyInput = document.getElementById('selectedApiKey');
    const resourceInput = document.getElementById('resource');
    const container = document.getElementById("payloadEditor");
    const options = { mode: 'code', modes: ['code', 'tree'] };

    if (!container || !resourceInput || !apiKeyInput) return;



try {
  const resourceChoices = presetChoices(resourceInput, Choices);
  const apiChoices = presetChoices(apiKeyInput, Choices);
  let keyUrl = "/api/partials/keys/"

  Promise.all([
    axiosInstance.get('/api/resources/'),
    axiosInstance.get(keyUrl),
  ])
  .then(([resourcesRes, keysRes]) => {
    const resources = resourcesRes.data.map(r => ({
      value: `/api/v1/professions/${r.value}`,
      label: `/api/v1/professions/${r.value}`
    }));
    const keyResources = keysRes.data
      .filter(d => d.status === "active")
      .map(d => ({
        value: d.name,
        label: d.name,
        customProperties: {
          id: d.uuid,
          status: d.status,
          access_type: d.access_type
        }
      }));
    apiChoices.setChoices(keyResources, 'value', 'label', false);
    resourceChoices.setChoices(resources, 'value', 'label', false);

  })
  .catch(error => {console.error("One of the requests failed:", error)});
  
  
  apiChoices.passedElement.element.addEventListener('change', async (event) => {
    const selected = apiChoices.getValue(true);
    const selectedOption = apiChoices.getValue();

    const keyIdParam = new URLSearchParams({uuid: selectedOption.customProperties.id}).toString();

    const keyResponse = await axiosInstance.get(keyUrl, {
      params: {
        uuid: selectedOption.customProperties.id
      }
    });

    const {key} = keyResponse.data;
    PK_API_KEY = key;
});

} catch (error) {
  console.error(error);
}
    

    const editor = new JSONEditor(container, options);
    editor.set({ search: "kwasa", ordering: "name", license: ''});

    // Handle form submit
    $("#simulateApiForm").on("submit", async function (e) {
      e.preventDefault();

      const form = $(this);
      form.find("button[type='submit']").prop("disabled", true);

      const json = editor.get();
      const params = new URLSearchParams(json).toString();

      const resource = $("select#resource");
      if (!resource) {
        resource.focus();
        return;
      } else {
      }

      try {
        const response = await axiosInstance.get(`${resource.val()}?${params}`, {
          headers: {"PK-Api-Key": PK_API_KEY}
        });

        editor.set(response.data);

      } catch (err) {
        if (err.response) {
          editor.set({
            status: err.response.status,
            statusText: err.response.statusText,
            headers: err.response.headers,
            data: err.response.data
          });
        } else if (err.request) {
          editor.set({
            error: "No response from server",
            request: err.request
          });
        } else {
          editor.set({ error: err.message });
        }

      } finally {
        form.find("button[type='submit']").prop("disabled", false);

        // Reset editor 10 seconds after submit, only once
        setTimeout(() => {
          editor.set({ search: "kwasa", ordering: "name", license: ''});
        }, 10000);
      }
    });
  });
}
