// const reqUrl = "http://localhost:8081/"

// // get the URL and format it for post
// const data = {
//     url: document.location.href
// }


// // Send request
// $.post(reqUrl, data, (ret, status) => {
//     if (status == "success" && ret != "[]") {
//         var payload = JSON.parse(ret);
//         var leaning = payload[0];
//         var keyTokens = payload[1];
//         //alert(payload[0]);
//     }
// });

// chrome.runtime.onMessage.addListener(
//     function(request, sender, sendResponse) {
//       if (request.cmd == "any command") {
//         $.post(reqUrl, data, (ret, status) => {
//             if (status == "success" && ret != "[]") {
//                 var payload = JSON.parse(ret);
//                 var leaning = payload[0];
//                 var keyTokens = payload[1];
//                 sendResponse(payload);
//             }
//         });
//       } else {
//         sendResponse({ result: "error", message: `Invalid 'cmd'` });
//       }
//       return true; 
//     });
