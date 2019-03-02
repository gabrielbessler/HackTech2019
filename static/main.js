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

function tryLogin() {
    let elt1 = document.getElementById("message_one");
    let elt2 = document.getElementById("message_two");

    elt1.innerHTML = "";
    elt2.innerHTML = "";

    let name    = document.getElementById("name");
    let pw      = document.getElementById("password");

    let validLogin = true;

    if (name.value == "") {
        elt1.innerHTML = "Required field";
        validLogin = false;
    }
    if (pw.value == "") {
        elt2.innerHTML = "Required field";
        validLogin = false;
    }

    if (validLogin) {
        login_handle(name.value, pw.value);
    }

}

function failLogin() {
    let resp = document.getElementById("response_msg");
    resp.innerHTML = "Login Failed";
}

function succeedLogin() {
    window.location.href = "/";
}

function tryRegister() {
    let elt1 = document.getElementById("message_one");
    let elt2 = document.getElementById("message_two");
    let elt3 = document.getElementById("message_three");

    elt1.innerHTML = "";
    elt2.innerHTML = "";
    elt3.innerHTML = "";

    let email   = document.getElementById("email");
    let pw      = document.getElementById("password");
    let name    = document.getElementById("name");

    let validReg = true;

    if (name.value == "") {
        elt1.innerHTML = "Required field";
        validReg = false;
    }
    if (pw.value == "") {
        elt2.innerHTML = "Required field";
        validReg = false;
    }
    if (email.value == "") {
        elt3.innerHTML = "Required field"; 
        validReg = false;
    }
    else if (!email.value.includes("@")) {
        elt3.innerHTML = "Invalid email";
        validReg = false;
    }

    if (validReg) {
        register_handle(name.value, pw.value, email.value);
    }
}

function failRegister() {
    let resp = document.getElementById("response_msg");
    resp.innerHTML = "Registration Failed (Try new Email or Username)";
}

function succeedRegister() {
    window.location.href = "/";
}

function loadThePDFBoi() {
   // atob() is used to convert base64 encoded PDF to binary-like data.
// (See also https://developer.mozilla.org/en-US/docs/Web/API/WindowBase64/
// Base64_encoding_and_decoding.)
var pdfData = atob(
    'JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwog' +
    'IC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAv' +
    'TWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0K' +
    'Pj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAg' +
    'L1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+' +
    'PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9u' +
    'dAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2Jq' +
    'Cgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJU' +
    'CjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVu' +
    'ZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4g' +
    'CjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAw' +
    'MDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9v' +
    'dCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G');
  
  // Loaded via <script> tag, create shortcut to access PDF.js exports.
  var pdfjsLib = window['pdfjs-dist/build/pdf'];
  
  // The workerSrc property shall be specified.
  pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';
  
  // Using DocumentInitParameters object to load binary data.
  var loadingTask = pdfjsLib.getDocument({data: pdfData});
  loadingTask.promise.then(function(pdf) {
    console.log('PDF loaded');
    
    // Fetch the first page
    var pageNumber = 1;
    pdf.getPage(pageNumber).then(function(page) {
      console.log('Page loaded');
      
      var scale = 1.5;
      var viewport = page.getViewport({scale: scale});
  
      // Prepare canvas using PDF page dimensions
      var canvas = document.getElementById('the-canvas');
      var context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
  
      // Render PDF page into canvas context
      var renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      var renderTask = page.render(renderContext);
      renderTask.promise.then(function () {
        console.log('Page rendered');
      });
    });
  }, function (reason) {
    // PDF loading error
    console.error(reason);
  });
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
        
        xhr.send(data);
    } else {
        uploadImage();
    }
}

function login_handle(name, pw) {
    console.log("login");
    url = "/login_attempt"
    var xhr = new XMLHttpRequest();
    xhr.open("POST",url,true);

    xhr.setRequestHeader("Content-type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.response.value == "Succeed") {
                succeedLogin();
            }
            else {
                failLogin();
            }
        }
    }

    var data = JSON.stringify({"name":name, "pass":pw});

    console.log(data);

    xhr.send(data);
}

function register_handle(name, pw, email) {
    url = "/register_attempt"
    var xhr = new XMLHttpRequest();
    xhr.open("POST",url,true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.response.value == "Succeed") {
                succeedRegister();
            }
            else {
                failRegister();
            }
        }
    }

    var data = JSON.stringify({"name":name, "pass":pw, "email":email});

    xhr.send(data);
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
