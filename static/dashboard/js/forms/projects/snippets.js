
export async function showApiKeyModal(apiKey) {
  const { default: Swal } = await import("sweetalert2");

  Swal.fire({
    title: "API Key Generated!",
    html: `
      <div class='d-flex flex-column align-items-center justify-content-center'>
        <p class="text-muted mb-2 text-center">
          Copy and save your API key now. You will <b>not</b> be able to see it again.
        </p>
        <div id="apiKeySnippet" class="border rounded p-2 text-center" style="width:100%; overflow-x:auto;">
          ${apiKey}
        </div>
        <button id="copyApiKey" class="swal2-confirm swal2-styled" style="background:#3085d6; margin-top:10px;">
          Copy API Key
        </button>
      </div>
    `,
    showConfirmButton: false,
    allowOutsideClick: false,
    didOpen: () => {
      document.getElementById("copyApiKey").addEventListener("click", () => {
        navigator.clipboard.writeText(apiKey).then(() => {
          Swal.fire({
            icon: "success",
            title: "Copied!",
            text: "Your API key has been copied to clipboard.",
            timer: 2000,
            showConfirmButton: false
          });
        });
      }, { once: true });
    }
  });
}


export function presetChoices(field, ChoicesLib) {
  if (field.choicesInstance) {
    return field.choicesInstance;
  }

  const instance = new ChoicesLib(field, {
    searchPlaceholderValue: 'Type a resource...',
    shouldSort: false,
    searchResultLimit: 10,
    placeholder: true,
    searchEnabled: true,
    removeItemButton: true,
  });
  field.choicesInstance = instance;
  return instance;
}


export async function InvalidateAndLoadNewKeys() {
  const apiKeyInput = document.getElementById('selectedApiKey');
  const { default: Choices } = await import("choices.js");
  const { default:axiosInstance } = await import("../../libs/main");

  let apiChoices;
  if (apiKeyInput.choicesInstance) {
    apiChoices = apiKeyInput.choicesInstance;
  } else {
    apiChoices = presetChoices(apiKeyInput, Choices);
    apiKeyInput.choicesInstance = apiChoices;
  }

  const keysRes = await axiosInstance.get("/api/partials/keys/");
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
  apiChoices.setChoices(keyResources, 'value', 'label', true);
}
