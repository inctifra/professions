import axios from "axios";

export class FormAction {
        constructor() {
        this.axiosInstance = axios.create({
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
    }

    getCsrfToken(form) {
        return $(form).find('input[name="csrfmiddlewaretoken"]').val();
    }

    getFormData(form) {
        return new FormData(form); ;
    }

  handleResponseMessage(form, response, isSuccess = true) {
    let messageText = "";

    if (isSuccess) {
      messageText = response?.data?.message || "Operation successful!";
      this.showMessageBanner(form, messageText, "success");
    } else {
      if (response?.response?.data?.errors) {
        messageText = response.response.data.errors;
      } else if (response?.message) {
        messageText = response.message;
      } else {
        messageText = "An error occurred. Please try again.";
      }
      this.showMessageBanner(form, messageText, "error");
    }
  }

  showMessageBanner(form, message, type) {
    const target = $(form).find('div.response');
    if (type === "success") {
      target.html(`
        <div class="alert alert-success" role="alert">${message}</div>
        `)
    } else if (type === "error") {
      target.html(`
        <div class="alert alert-danger d-flex align-items-center" role="alert">
          <div>${message}</div>
        </div>
        `)
      
    }
  }

}