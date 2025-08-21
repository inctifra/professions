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

    let editorOptions = {}
  const editor = new JSONEditor(container, options);


    try {
      const resourceChoices = presetChoices(resourceInput, Choices);
      const apiChoices = presetChoices(apiKeyInput, Choices);
      let keyUrl = "/api/partials/keys/"

      Promise.all([
        axiosInstance.get('/api/resources/'),
        axiosInstance.get(keyUrl),
      ])
      .then(([resourcesRes, keysRes]) => {
        const resources = resourcesRes.data.map(r => {
        // convert array of search fields → object with empty values
        const searchFieldsObj = (r.schema.search_fields || []).reduce((acc, field) => {
          acc[field] = ""; // default empty string value
          return acc;
        }, {});

        return {
          value: `/api/v1/professions/${r.value}`,
          label: `/api/v1/professions/${r.value}`,
          customProperties: {
            // ...r.schema,
            search_fields: searchFieldsObj,
          }
        };
      });
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

    // handle editor options
    resourceChoices.passedElement.element.addEventListener("change", async (event)=>{
       const selectedOption = resourceChoices.getValue();
       const {customProperties } = selectedOption;
       editorOptions = customProperties
       editor.set({ "search": editorOptions });
    })
    } catch (error) {
      console.error(error);
    }
    

  
    editor.set(editorOptions);

    $("#simulateApiForm").on("submit", async function (e) {
      e.preventDefault();

      const form = $(this);
      form.find("button[type='submit']").prop("disabled", true);

      const json = editor.get();
      const params = new URLSearchParams();

      Object.entries(json).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          value.forEach(v => {
            if (typeof v === "object") {
              params.append(key, JSON.stringify(v)); // serialize object
            } else {
              params.append(key, v);
            }
          });
        } else if (typeof value === "object") {
          // if it's a nested object like { filterset_fields: [...] }
          params.append(key, JSON.stringify(value));
        } else {
          params.append(key, value);
        }
      });

      console.log(JSON.stringify(params, undefined, 2))

    const queryString = params.toString();
    console.log(queryString);

      const resource = $("select#resource");
      if (!resource) {
        resource.focus();
        return;
      } else {
      }

      try {
        const response = await axiosInstance.get(`${resource.val()}?${queryString}`, {
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
        setTimeout(() => {
          editor.set({ search: editorOptions});
        }, 10000);
      }
    });
  });
}
