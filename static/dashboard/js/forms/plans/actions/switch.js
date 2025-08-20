import $ from "jquery";

const $priceSwitch = $("input#price-switch");

// formatter for Kenyan locale
const fmt = v => Number(v).toLocaleString("en-KE", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

// update function
function updatePrices() {
  const isYearly = $priceSwitch.is(":checked");

  $("div.plan-pricing").each(function () {
    const $wrap = $(this);
    const monthly = $wrap.data("monthly");
    const yearly  = $wrap.data("yearly");

    $wrap.find(".amount").text(isYearly ? fmt(yearly) : fmt(monthly));
    $wrap.find(".period").text(isYearly ? "Yearly" : "Monthly");
  });
}

$(function () {updatePrices()})

$priceSwitch.on("change", updatePrices);
