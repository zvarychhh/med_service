const toast = document.querySelector(".my_toast"),
    closeIcon = document.querySelector(".close"),
    progress = document.querySelector(".progress");

if (toast) {
    toast.classList.add("active")
    progress.classList.add("active")

    setTimeout(() => {
        toast.classList.remove("active")
    }, 5000)
}
if (closeIcon) {
    closeIcon.addEventListener("click", () => {
        toast.classList.remove("active")
    })
}
