const reqUrl = "http://localhost:8081/";
let sourceratingbias = document.getElementById('sourceratingbias');

window.addEventListener('load', (event) => {
  sourcebias();
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
      } else {
        sourceratingbias.innerText = "Error: Not a valid article"
      }
    });
  
  });
}
