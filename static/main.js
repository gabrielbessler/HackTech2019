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

function loadThePDFBoi() {
   // atob() is used to convert base64 encoded PDF to binary-like data.
// (See also https://developer.mozilla.org/en-US/docs/Web/API/WindowBase64/
// Base64_encoding_and_decoding.)
var url = 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/compressed.tracemonkey-pldi-09.pdf';

// Loaded via <script> tag, create shortcut to access PDF.js exports.
var pdfjsLib = window['pdfjs-dist/build/pdf'];

// The workerSrc property shall be specified.
pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

var pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = .9,
    canvas = document.getElementById('the-canvas'),
    ctx = canvas.getContext('2d');

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
 */
function renderPage(num) {
  pageRendering = true;
  // Using promise to fetch the page
  pdfDoc.getPage(num).then(function(page) {
    var viewport = page.getViewport(canvas.width / page.getViewport(1.0).width);
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);

    // Wait for rendering to finish
    renderTask.promise.then(function() {
      pageRendering = false;
      if (pageNumPending !== null) {
        // New page rendering is pending
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });

  // Update page counters
  document.getElementById('page_num').textContent = num;
}

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
function queueRenderPage(num) {
  if (pageRendering) {
    pageNumPending = num;
  } else {
    renderPage(num);
  }
}

/**
 * Displays previous page.
 */
function onPrevPage() {
  if (pageNum <= 1) {
    return;
  }
  pageNum--;
  queueRenderPage(pageNum);
}
document.getElementById('prev').addEventListener('click', onPrevPage);

/**
 * Displays next page.
 */
function onNextPage() {
  if (pageNum >= pdfDoc.numPages) {
    return;
  }
  pageNum++;
  queueRenderPage(pageNum);
}
document.getElementById('next').addEventListener('click', onNextPage);

/**
 * Asynchronously downloads PDF.
 */
pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
  pdfDoc = pdfDoc_;
  document.getElementById('page_count').textContent = pdfDoc.numPages;

  // Initial/first page rendering
  renderPage(pageNum);
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
