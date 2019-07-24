const reqUrl = "http://localhost:8081/";
let sourceratingbias = document.getElementById('sourceratingbias');

window.addEventListener('load', (event) => {
  sourcebias();
  document.getElementById('highlight').addEventListener('click', sendHighlightMessage, false);
});

function sourcebias() {
  sourceratingbias.innerText = "Analyzing article..."
  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    const data = {
      url: tabs[0].url
    };
    $.post(reqUrl, data, (ret, status) => {
      if (status == "success" && ret != "[]") {
        var payload = JSON.parse(ret);
        var leaning = payload[0];
        var keyTokens = payload[1];
        sourceratingbias.innerText = payload[0];
        sendHighlightMessage();
      } else {
        sourceratingbias.innerText = "Error: Not a valid article"
      }
    });
  
  });
}

window.addEventListener('load', (event) => {
  chrome.tabs.executeScript(null, {
    file: 'content.js'
  }, () => {
      connect() //this is where I call my function to establish a connection     });
  });
});


function connect() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const port = chrome.tabs.connect(tabs[0].id);
    port.postMessage({ function: 'html' });
    port.onMessage.addListener((response) => {
      html = response.html;
      title = response.title;
      description = response.description;
    });
  });
}

// function sendHighlightMessage() {
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//     chrome.tabs.sendMessage(tabs[0].id, {highlight: true}, function(response) {
//       console.log(response);
//     });
//   });
// }