
const input = document.querySelector("#phone");
const world = window.intlTelInput(input, {
    initialCountry: "us",
    strictMode: true,
    loadUtils: () => import("https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/25.2.1/build/js/utils.min.js") // for formatting/placeholders etc
});
document.getElementById('contactform').addEventListener('submit', function (e) {
    if (world.isValidNumber()) {
        input.value = world.getNumber();
    }
    else {
        e.preventDefault();
    }
})