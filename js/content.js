// get the URL of the page
var url = document.location.href;

 //if not on a docs.microsoft.com domain
if ((url.indexOf("//docs.microsoft.com") <= -1) &&
    (url.indexOf("//www.cnn.com") <= -1)) {
    // send inactive icons
    browser.runtime.sendMessage({
        "iconPath20": "images/inactive-ata20.png",
        "iconPath40": "images/inactive-ata40.png"
    });
}