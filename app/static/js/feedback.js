let uploadButton = document.getElementById("file")
let fileName = document.getElementById("filename")
let filenameContainer = document.getElementById("filenameContainer");

const icon = document.createElement("i");
icon.classList.add("fa-solid");
icon.classList.add("fa-check");

uploadButton.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadButton.files[0])
    filenameContainer.insertBefore(icon, fileName);
    fileName.textContent = " " + uploadButton.files[0].name;
}