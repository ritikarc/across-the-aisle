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
        var links = payload[1];
        sourceratingbias.innerText = payload[0];
        // alert(JSON.stringify(links.value[0]));
        urls = [
          [links.value[0].url, links.value[0].name], 
          [links.value[1].url, links.value[1].name],
          [links.value[2].url, links.value[2].name],
          [links.value[3].url, links.value[3].name]  
        ];
        
        let urlDiv = document.getElementById('newsLinks');
        for (var i = 0; i < 4; i++) {
          urlDiv.innerHTML += '<li><a href="' + urls[i][0] + '">' + urls[i][1] + '</a></li>';
        }
        //alert(JSON.stringify(urls));
      } else {
        sourceratingbias.innerText = "Error: Not a valid article"
      }
    });
  
  });
}


function bingnewsapi() {
  
}
// function sendHighlightMessage() {
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//     chrome.tabs.sendMessage(tabs[0].id, {highlight: true}, function(response) {
//       console.log(response);
//     });
//   });
// }
