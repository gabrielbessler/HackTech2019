let DEBUG_MODE = true; 
let DEBUG_LEVEL = 0;

function loadPage() {
   hideImage();
}

function hideImage() {
    document.getElementById("imgDisplay").style.display = "none"; 
}

function showImage() {
    document.getElementById("imgDisplay").style.display = "inline-block"; 
}

function showText() {
    document.getElementById("textArea").style.display = "inline-block";
}

function hideText() {
    document.getElementById("textArea").style.display = "none"; 
}

function sendText() {
    let textArea = document.getElementById("textArea");
    
    url = "/text"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"text": textArea.value});
    
    debugMessage(data, 0);

    xhr.send(data)
}

function previewFile(){
    showImage();
    console.log("hiding text");
    hideText(); 
    var preview = document.querySelector('img'); //selects the query named img
    var file    = document.querySelector('input[type=file]').files[0]; //sames as here
    var reader  = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file); //reads the data as a URL
    } else {
        preview.src = "";
    }
}

function debugMessage(message, level) {
    if (DEBUG_MODE && level >= DEBUG_LEVEL) {
        console.log(message);
    }
}
    
function login() {
    
}