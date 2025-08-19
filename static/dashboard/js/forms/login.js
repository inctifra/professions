import { FormAction } from "./handler";
import $ from "jquery";


class LoginFormAction extends FormAction {
    constructor() {
        super();
    }
    submitLogin(form) {
        const data = this.getFormData(form);
        const csrfToken = this.getCsrfToken(form);

        return this.axiosInstance.post($(form).attr("action"), data, {
            headers: { "X-CSRFToken": csrfToken }
        });
    }
}


const loginForm = new LoginFormAction();

$("#account_login_form").on("submit", function(event) {
  event.preventDefault();
  const $form = $(this);
  $form.find("button[type='submit']").prop("disabled", true);

  loginForm.submitLogin(this)
    .then(response => {
      loginForm.handleResponseMessage(this, response, true);
      const {redirect_url} = response.data;
      if(redirect_url){
        setTimeout(() => {
          window.location.href = redirect_url;
        }, 2000);
      }
    })
    .catch(error => {
      loginForm.handleResponseMessage(this, error, false);
    })
    .finally(() => {
      $form.find("button[type='submit']").prop("disabled", false);
    });
});
