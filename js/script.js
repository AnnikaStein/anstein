function respNav() {
  var x = document.getElementById("myTopnav");
  if (x.className === "navbar" || x.className === "navbar sticky") {
    x.classList.add("responsive");
  } else {
    x.classList.remove("responsive");
  }
}
