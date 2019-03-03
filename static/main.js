let DEBUG_MODE = true; 
let DEBUG_LEVEL = 0;
let mode = "text";
let words_found = {};

function getSelectionText() {
    var text = '';
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != 'Control') {
        text = document.selection.createRange().text;
    }
    
    if (text in words_found) {
        document.getElementById("result1").innerHTML = words_found[text];
    }  else {
        if (text.length >= 3 && /[\w']+/.test(text)) {

            url = "/word/" + text; 
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
    
            xhr.setRequestHeader("Content-type", "application/json");
    
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    
                    resp = JSON.parse(xhr.response);
                    S = `${text} - definition:`;
                    for (let i = 0; i < resp.length; i++) {
                        S += "<div>" + resp[i] + "</div>";
                    }
                    words_found[text] = S
                    document.getElementById("result1").innerHTML = S
                }
            }
            xhr.send();
        }
    }    
}       

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

function updateCount() {
    $('#characters').text($(this).val().length);
    $('#words').text($(this).val().split(' ').length);
    saveValue(this);
}

function loadPage() {
    hideImage();
    // showVideo();

    $('#textArea').on('keyup keydown', updateCount);
    document.getElementById("textArea").value = getSavedValue("textArea");

    $('#submitBtn').on('click', getResult); 

    function getResult() {
        sendText();
    }

    $('#characters').text(document.getElementById("textArea").value.length);
    $('#words').text(document.getElementById("textArea").value.split(' ').length);
}

function hideImage() {
    if (document.getElementById("imgDisplay").style.display != "none") {
        document.getElementById("submitBtn").innerHTML = "Upload Text";
        document.getElementById("toHide1").style.display = "inline";
        document.getElementById("toHide2").style.display = "inline";
        $("#fileSelect").val("");
        document.getElementById("imgDisplay").style.display = "none"; 
    }
}

function showImage() {
    document.getElementById("toHide1").style.display = "inline";
    document.getElementById("toHide2").style.display = "inline";
    document.getElementById("submitBtn").innerHTML = "Upload Image"
    document.getElementById("imgDisplay").style.display = "inline-block"; 
}

function showText() {
    if (document.getElementById("textArea").style.display != "inline-block") {
        document.getElementById("textArea").style.display = "inline-block";
        document.getElementById("characters").style.display = "inline-block"; 
        document.getElementById("words").style.display = "inline-block"; 
    }
}

function saveValue(e) {
    var id = e.id;
    var val = e.value;
    localStorage.setItem(id, val);
}

function getSavedValue(v) {
    if (!localStorage.getItem(v)) {
        return "Input Here";
    }
    return localStorage.getItem(v);
}

function hideText() {
    document.getElementById("textArea").style.display = "none"; 
    document.getElementById("characters").style.display = "none"; 
    document.getElementById("words").style.display = "none"; 
    document.getElementById("toHide2").style.display = "none"; 
    document.getElementById("toHide1").style.display = "none"; 
}

function getPDF() {
    if (mode !== "text") {
        result = convertToBase64();
            
        url = "/toPDF"
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);

        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                console.log(xhr.response);
            }
        }
        
        var data = JSON.stringify({"img": JSON.stringify(result)});
        
        xhr.send(data);
    }
}

function formatText(text) {
    url = "/text"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"text": text});
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById("mainContent").innerHTML = xhr.response;
           
        }
    }

    xhr.send(data);
}

function sendText() {
    let text = "";
    
    if (mode === "text") {
        text = document.getElementById("textArea").value;
        formatText(text)
    } else {
        uploadImage();
    }
    
}

function loadResultImage(result) {
    formatText(result);
}

function login_handle(name, pw) {
    url = "/login_attempt"
    var xhr = new XMLHttpRequest();
    xhr.open("POST",url,true);

    xhr.setRequestHeader("Content-type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            console.log(xhr.response);
            if (xhr.response == "Succeed") {
                succeedLogin();
            }
            else {
                failLogin();
            }
        }
    }

    var data = JSON.stringify({"name":name, "pass":pw});

    xhr.send(data);
}

function createProfile() {
    pic = document.getElementById("mycanvas");
    ctx = pic.getContext('2d');
    info = pic.getAttribute("data");
    for (let i = 0; i < info.length; i++) {
        if (info[i] == 0) {
            ctx.fillStyle = "#FF0000";
            ctx.fillRect(3*i % 50, i*3 / 50, 3, 3);
        } 
        if (info[i] == 1) {
            ctx.fillStyle = "#00FF00";
            ctx.fillRect(3*i % 50, i*3 / 50, 3, 3);
        } 
        if (info[i] == 2) {
            ctx.fillStyle = "#0000FF";
            ctx.fillRect(3*i % 50, i*3 / 50, 3, 3);
        } 
    }
}

function register_handle(name, pw, email) {
    url = "/register_attempt"
    var xhr = new XMLHttpRequest();
    xhr.open("POST",url,true);
    xhr.setRequestHeader("Content-type", "application/json");
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.response == "Succeed") {
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
    return document.getElementById("imgDisplay").data;
};

function uploadImage() {
    result = convertToBase64();

    url = "/img"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            loadResultImage(xhr.response);
        }
    }
    
    var data = JSON.stringify({"img": JSON.stringify(result)});
    
    xhr.send(data);
}

function displayAnnotations(annotations) {
    var ann_divs = annotations.map(function(e) {
        s = `
            <div class='annotationModule' annId=${e[0]['id']}> ${e[0]['user']} 
                <div class="score"> ${getStars(e[0]['rating'], e[0]['id'], e[1])}
                </div>
                <div class="notes">
                    ${e[0]['annotation']}
                </div>
            </div>`
        return s;
    })

    console.log(annotations);
    
    document.getElementById("annotation").innerHTML = ann_divs.join('\n');
}

function addAnnotationEvents() {
    $('.star').on('click', function(event) {
        if ($(this).attr("edit") == "true") {
            $(this).parent().html(getStars(1 + parseInt(event.currentTarget.getAttribute("count")), false));
            score = 1 + parseInt(event.currentTarget.getAttribute("count"));

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/addRating", true); 

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    document.getElementById("alerts").innerHTML = xhr.response;
                }
            }
    
            var data = JSON.stringify({"score":score, "id": $(this).attr("annId")});

            xhr.send(data);
        }
    });

    $('.star').on('mouseover', function(event) {
        if ($(this).attr("edit") == "true") {
            let num = parseInt(event.currentTarget.getAttribute("count"));
            for(let i = 0; i < 5; i++) {
                if (i <= num) {
                    obj = $(this).parent().children("img[count=" + i + "]");
                    type = obj.attr("type");
                    if (type != "full") {
                        obj.attr("src", "/static/fullstar.png")
                    }
                } else {
                    obj = $(this).parent().children("img[count=" + i + "]");
                    type = obj.attr("type");
                    if (type != "over") {
                        obj.attr("src", "/static/star.png")
                    }
                }
            }
        }
    });

    $('.star').on('mouseout', function(event) {
        if ($(this).attr("edit") == "true") {
            // Update to old type
            let num = parseInt(event.currentTarget.getAttribute("count"));
            for(let i = 0; i < 5; i++) {
                obj = $(this).parent().children("img[count=" + i + "]");
                type = obj.attr("type");
                if (type == "over") {
                    obj.attr("src", "/static/star.png")
                } else if (type == "full") {
                    obj.attr("src", "/static/fullstar.png")
                } else if (type == "locked") {
                    obj.attr("src", "/static/locked.png")
                } else if (type == "half") {
                    obj.attr("src", "/static/halfstar.png")
                }
                
            }
        }
    });

}


function getAnnotations(sentence) {
    
    url = "/getAnnotations";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.response == undefined || xhr.response == "Not valid" || xhr.response == "Cannot be empty") {
                console.log("No response")
            } else {
                displayAnnotations(JSON.parse(xhr.response));
                addAnnotationEvents();
            }
        }
    }
    
    var data = JSON.stringify({"sentence":sentence});
    
    xhr.send(data);
}

function annotate(sentence, annotation) {

    url = "/annotate";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            getAnnotations(sentence);
            document.getElementById('alerts').innerHTML = xhr.response;
        }
    }
    
    //var data = {'sentence':sentence, 'annotation':annotation};
    var data = JSON.stringify({"sentence":sentence, "annotation":annotation});

    xhr.send(data);

}

function getRandomTextbook() {
    showImage();
    hideText(); 
    mode = "image"; 
    var preview = document.getElementById("imgDisplay");
    preview.src = "/static/example" + Math.floor((Math.random() * 5))
}

function previewFile(){
    showImage();
    hideText(); 
    mode = "image";
    var preview = document.querySelector('img'); //selects the query named img
    var file    = document.querySelector('input[type=file]').files[0]; //sames as here
    let ext = file.name.split(".").pop();
    
    if (file === undefined) {
        hideImage();
        showText();
    } else if (ext == "pdf") {
        preview.src = "static/pdf_logo.jpeg";
        var reader  = new FileReader();

        reader.onloadend = function() {
            preview.data = reader.result;
        }
        
        if (file) {
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
            preview.data = "";
        }

    } else {
        var reader  = new FileReader();

        reader.onloadend = function () {
            preview.src = reader.result;
            preview.data = reader.result;
        }
    
        if (file) {
            reader.readAsDataURL(file); //reads the data as a URL
        } else {
            preview.src = "";
            preview.data = "";
        }
    }   
}

/* Takes a score from 0-5 */
function getStars(score, id, editable) {
    console.log(score);
    if (score == undefined || score == "Unrated") {
        fullStars = 0;
        halfStars = 0;
        leftOver = 0;
        locked = 5;
    } else {
        stars = Math.round((score * 2)) / 2;
        fullStars = Math.floor(stars);
        // Will be 0 or 1
        halfStars = Math.round((score - fullStars) * 2);
        leftOver = 5 - fullStars - halfStars;
        locked = 0;
    }
    
    S = "";
    count = 0
    for (let i = 0; i < fullStars; i++) {
        S += "<img edit='" + !editable + "' type='full' annId='" + id + "' count='" + count + "' class='star' src='/static/fullstar.png'></img>"; 
        count++;
    }
    for (let i = 0; i < halfStars; i++) {
        S += "<img edit='" + !editable + "' type='half' annId='" + id + "' count='" + count + "' class='star' src='/static/halfstar.png'></img>"; 
        count++;
    }
    for (let i = 0; i < leftOver; i++) {
        S += "<img edit='" + !editable + "' type='over' annId='" + id + "' count='" + count + "' class='star' src='/static/star.png'></img>"; 
        count++;
    }
    for (let i = 0; i < locked; i++) {
        S += "<img edit='" + !editable + "' type='locked' annId='" + id + "' count='" + count + "' class='star' src='/static/locked.png'></img>";
        count++; 
    }
    return S;
}

function debugMessage(message, level) {
    if (DEBUG_MODE && level >= DEBUG_LEVEL) {
        console.log(message);
    }
}

function deleteFromFavorites() {
    // Make HTTP request to save to favorites     
    url = "/unfavorite"
    var xhr = new XMLHttpRequest(Star);
    xhr.open("POST", url, true);

    let info = document.getElementById('ogText').getAttribute('info');

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"text": info});
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById('alerts').innerHTML = xhr.response;
        }
    }

    xhr.send(data);   
}

function saveToFavorites() {
    // Make HTTP request to save to favorites     
    url = "/favorite"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    let info = document.getElementById('ogText').getAttribute('info');

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"text": info});
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById('alerts').innerHTML = xhr.response;
        }
    }

    xhr.send(data);   
}

function getEntities(position, sentence) {

    url = "/getEntities"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");

    var data = JSON.stringify({'pos':position, 'sentence':sentence})

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById("passage").setAttribute("data",JSON.parse(xhr.response))
        }
    }

    xhr.send(data);
}
