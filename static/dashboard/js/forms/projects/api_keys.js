$(function() {
  const $permissionRadios = $("input[name='permission_type']");
  const $projectField = $("#project-field");
  const $domainField = $("#domain-field");
  const $projectSelect = $projectField.find("select");
  const $domainSelect = $domainField.find("select");

  function toggleFields() {
    const selected = $("input[name='permission_type']:checked").val();

    if (selected === "manage_project") {
      $projectField.show();
      $domainField.hide();

      $projectSelect.prop("required", true);
      $domainSelect.prop("required", false).val(""); // reset
    } else if (selected === "manage_domain") {
      $projectField.hide();
      $domainField.show();

      $projectSelect.prop("required", false).val(""); // reset
      $domainSelect.prop("required", true);
    }
  }

  $permissionRadios.on("change", toggleFields);

  toggleFields();

// Toggle active class for buttons
$("input[name='permission_type']").each(function() {
    const $radio = $(this);
    const $label = $radio.closest("label");

    // On page load, set active class according to checked radio
    if ($radio.is(":checked")) {
        $label.addClass("active");
    } else {
        $label.removeClass("active");
    }

    // On change, update active classes
    $radio.on("change", function() {
        $("input[name='permission_type']").each(function() {
            const $r = $(this);
            const $l = $r.closest("label");
            if ($r.is(":checked")) {
                $l.addClass("active");
            } else {
                $l.removeClass("active");
            }
        });
    });
});


});
