// Responsive navigation bar (collapse)
function respNav() {
  var x = document.getElementById("myTopnav");
  if (x.className === "navbar" || x.className === "navbar sticky") {
    x.classList.add("responsive");
  } else {
    x.classList.remove("responsive");
  }
}


// Collabsible
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("act");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}
