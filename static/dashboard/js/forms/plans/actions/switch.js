import $ from "jquery";

const priceSwitch = $("input#price-switch");

priceSwitch.on("change", function() {
    const isYearly = $(this).is(":checked");

    $("div.plan-pricing").each(function() {
        const monthly = $(this).data("monthly");
        const yearly = $(this).data("yearly");

        if (isYearly) {
            $(this).html(`${yearly} <span class="text-muted">Yearly</span>`);
        } else {
            $(this).html(`${monthly} <span class="text-muted">Monthly</span>`);
        }
    });
});