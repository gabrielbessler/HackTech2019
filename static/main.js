let DEBUG_MODE = true; 
let DEBUG_LEVEL = 0;
let mode = "text";


function showVideo() {
    const constraints = {
        video: true
    };
    
    const video = document.querySelector('video');
    
    function hasGetUserMedia() {
        return !!(navigator.mediaDevices &&
          navigator.mediaDevices.getUserMedia);
    }
    
    if (hasGetUserMedia()) {
        navigator.mediaDevices.getUserMedia(constraints).
        then((stream) => {video.srcObject = stream});
    } else {
        console.log("User media not supported");
    }
}

function clearImage() {
    hideImage();
    showText();
}

function loadLogin() {
    console.log("hello");
}

function tryLogin() {
    let elt1 = document.getElementById("message_one");
    let elt2 = document.getElementById("message_two");
    let elt3 = document.getElementById("message_three");

    elt1.innerHTML = "";
    elt2.innerHTML = "";
    elt3.innerHTML = "";

    let email = document.getElementById("email");
    let pw = document.getElementById("password");
    let name = document.getElementById("name");

    if (name.value == "") {
        console.log("hello");
        elt1.innerHTML = "Required field";
    }
    if (pw.value == "") {
        elt2.innerHTML = "Required field";
    }
    if (email.value == "") {
        elt3.innerHTML = "Required field"; 
    
    }
}

function loadPage() {
    hideImage();
    // showVideo();

    $('#textArea').on('keyup keydown', updateCount);
    document.getElementById("textArea").value = getSavedValue("textArea");

    function updateCount() {
        $('#characters').text($(this).val().length);
        $('#words').text($(this).val().split(' ').length);
        saveValue(this);
    }
}


function hideImage() {
    document.getElementById("submitBtn").innerHTML = "Upload Text";
    document.getElementById("toHide1").style.display = "inline";
    document.getElementById("toHide2").style.display = "inline";
    $("#fileSelect").val("");
    document.getElementById("imgDisplay").style.display = "none"; 
}

function showImage() {
    document.getElementById("toHide1").style.display = "inline";
    document.getElementById("toHide2").style.display = "none";
    document.getElementById("submitBtn").innerHTML = "Upload Image"
    document.getElementById("imgDisplay").style.display = "inline-block"; 
}

function showText() {
    document.getElementById("textArea").style.display = "inline-block";
    document.getElementById("characters").style.display = "inline-block"; 
    document.getElementById("word").style.display = "inline-block";

}

function saveValue(e) {
    var id = e.id;
    var val = e.value;
    localStorage.setItem(id, val);
    console.log("value saved!")
}

function getSavedValue(v) {
    console.log("I was called");
    if (!localStorage.getItem(v)) {
        console.log("failed");
        return "Input Here";
    }
    console.log("succeeded");
    return localStorage.getItem(v);
}

function hideText() {
    document.getElementById("textArea").style.display = "none"; 
    document.getElementById("characters").style.display = "none"; 
    document.getElementById("words").style.display = "none"; 
}

function sendText() {
    if (mode === "text") {
        let textArea = document.getElementById("textArea");
        
        url = "/text"
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);

        xhr.setRequestHeader("Content-type", "application/json");
        
        var data = JSON.stringify({"text": textArea.value});
        
        debugMessage(data, 0);

        xhr.send(data);
    } else {
        uploadImage();
    }
}

function convertToBase64() {
    return document.getElementById("imgDisplay").src;
};

function uploadImage() {
    result = convertToBase64();
    let textArea = document.getElementById("textArea");
        
    url = "/img"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"img": JSON.stringify(result)});
    
    xhr.send(data);
}

function previewFile(){
    showImage();
    hideText(); 
    mode = "image";
    var preview = document.querySelector('img'); //selects the query named img
    var file    = document.querySelector('input[type=file]').files[0]; //sames as here
    
    if (file === undefined) {
        hideImage();
        showText();
    } else {
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
}

function debugMessage(message, level) {
    if (DEBUG_MODE && level >= DEBUG_LEVEL) {
        console.log(message);
    }
}
    
function login() {
    
}
