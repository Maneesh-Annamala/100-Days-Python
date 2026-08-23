document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".task-complete-checkbox").forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            if (checkbox.checked) {
                checkbox.form.submit();
            }
        });
    });
});
