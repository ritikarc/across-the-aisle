const reqUrl = "http://localhost:8081/"

// get the URL and format it for post
const data = {
    url: document.location.href
}

 //if not on a docs.microsoft.com domain
// if ((url.indexOf("//docs.microsoft.com") <= -1) &&
//     (url.indexOf("//www.cnn.com") <= -1)) {
//     // send inactive icons
//     browser.runtime.sendMessage({
//         "iconPath20": "images/inactive-ata20.png",
//         "iconPath40": "images/inactive-ata40.png"
//     });
// }

// Send request

$.post(reqUrl, data, (ret, status) => {
    if (status == "success" && ret != "[]") {
        var payload = JSON.parse(ret);
        var leaning = payload[0];
        var keyTokens = payload[1];
        alert(leaning);
    } 
});
