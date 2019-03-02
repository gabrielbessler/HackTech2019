let DEBUG_MODE = true; 
let DEBUG_LEVEL = 0;

function sendText() {
    let textArea = document.getElementById("textarea");
    
    url = "/text"
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-type", "application/json");
    
    var data = JSON.stringify({"text": textArea.value});
    
    debugMessage(data, 0);

    xhr.send(data)
}

function debugMessage(message, level) {
    if (DEBUG_MODE && level >= DEBUG_LEVEL) {
        console.log(message);
    }
}
    