// get the buttons by id
//let CNNsourcerating = document.getElementById('sourcebiasrating');
//alert("Test");

let sourceratingbias = document.getElementById('sourceratingbias');

window.addEventListener('load', (event) => {
  sourcebias();
});

function sourcebias() {
    //if (!(url.indexOf("//www.cnn.com") <= -1)) {
        sourceratingbias.innerText = "CNN";
    //}
}
