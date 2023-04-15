//Get the button
let mybutton = document.getElementById("btn-back-to-top"),
    callbutton = document.getElementById(id = "btn-call");


// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (
        document.body.scrollTop > 20 ||
        document.documentElement.scrollTop > 20
    ) {
        mybutton.style.display = "block";
        callbutton.style.bottom = "95px"
        callbutton.classList.add("animate__slideInUp")
    } else {
        mybutton.style.display = "none";
        callbutton.style.bottom = "30px"
        callbutton.classList.remove("animate__slideInUp")
        callbutton.classList.add("animate__slideInDown")

    }
}

// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}