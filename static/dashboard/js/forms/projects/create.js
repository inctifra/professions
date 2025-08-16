import { FormAction } from "../handler";
import $ from "jquery";


class ProjectForm extends FormAction {
    constructor() {
        super();
    }
    create(form) {
        const data = this.getFormData(form);
        const csrfToken = this.getCsrfToken(form);
        return this.axiosInstance.post($(form).attr("action"), data, {
            headers: { "X-CSRFToken": csrfToken },
        });
    }
}

const projectForm = new ProjectForm();

$("form.project-form").each(function () {
    $(this).on("submit", function (event) {
        event.preventDefault();
        const $form = $(this);
        $form.find("button[type='submit']").prop("disabled", true);

        projectForm
            .create(this)
            .then(async (response) => {
                $form.trigger("reset");
                const { next_url, hold, is_secret_key } = response.data;
                console.log(response.data)
                if (next_url && !hold && !is_secret_key) {
                    projectForm.handleResponseMessage(this, response, true);
                    setTimeout(() => {
                        window.location.href = next_url;
                    }, 1000);
                }

                if(hold && is_secret_key){
                const { Modal } = await import("bootstrap");
                const { InvalidateAndLoadNewKeys, showApiKeyModal } = await import("./snippets");

                const modalEl = document.getElementById("createAPIKEY");
                const modalInstance = Modal.getInstance(modalEl);

                if (modalInstance) {
                    modalInstance.hide();
                    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('padding-right');
                }
                showApiKeyModal(response.data.message);
                InvalidateAndLoadNewKeys();
                }
            })
            .catch((error) => {projectForm.handleResponseMessage(this, error, false);})
            .finally(() => {
                setTimeout(() => {$form.find("button[type='submit']").prop("disabled", false);}, 1000);
            });
    });
});
