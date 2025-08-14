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
            .then((response) => {
                $form.trigger("reset");
                projectForm.handleResponseMessage(this, response, true);
                const { next_url } = response.data;
                if (next_url) {
                    setTimeout(() => {
                        window.location.href = next_url;
                    }, 1000);
                }
            })
            .catch((error) => {
                projectForm.handleResponseMessage(this, error, false);
            })
            .finally(() => {
                setTimeout(() => {
                    $form.find("button[type='submit']").prop("disabled", false);
                }, 1000);
            });
    });
});
