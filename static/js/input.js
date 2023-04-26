let my_inputs = document.getElementsByClassName("input-blank");
if (my_inputs) {

    for (const el of my_inputs) {
        el.value = "";
    }

}
let pass_check = document.getElementById("pass-check")

if (pass_check) {
    pass_check.addEventListener("click", function (e) {
        for (const el of ["id_password", "id_password1", "id_password2"]) {
            if (document.getElementById(el)) {
                const type = document.getElementById(el).type === 'password' ? 'text' : 'password';
                document.getElementById(el).type = type
            }


        }
    })
}