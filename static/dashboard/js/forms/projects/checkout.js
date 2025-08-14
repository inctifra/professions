import $ from "jquery";
import { FormAction } from "../handler";

$(function () {
    $("input[name='paymentMethod']").on("change", function () {
        if ($(this).is(":checked") && $(this).attr("id") === "card") {
            $("div.card-payment-option").show();
        } else {
            $("div.card-payment-option").hide();
        }
    });

    // Run on page load to set the correct initial state
    $("input[name='paymentMethod']:checked").trigger("change");
});


class CheckoutForm extends FormAction {
    constructor() {
        super()
    }

    checkout(form) {
        const data = this.getFormData(form);
        const csrfToken = this.getCsrfToken(form);

        return this.axiosInstance.post($(form).attr("action"), data, {
            headers: { "X-CSRFToken": csrfToken }
        });
    }
}

const checkout = new CheckoutForm();


// $("form#checkout-form").on("submit", async(event)=>{
//     event.preventDefault();
//     checkout.checkout(this).then(response=>{
//         const {data} = response;
//         console.log(data)
//     }).catch(err=>{
//         console.log(err)
//     })
// })

