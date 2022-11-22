
var up = false,
right = false,
down = false,
left = false,
wheel = false,
inverted = false; // Invert WASD movement

var mousePosX = 0, mousePosY = 0;

var offset = 10; // default: 10 px per frame
var zoom_scale = -0.001;
var zoom_max = 4;
var zoom_min = 0.125;
var zoom_delta = 0;
var scale = 1;

document.addEventListener('keydown', press);
function press(e){
if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
  if (inverted) up = true;
  else down = true;

}
if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
if (inverted) right = true;
else left = true;
}
if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
if (inverted) down = true;
else up = true;
}
if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
if (inverted) left = true;
else right = true;
}
}

document.addEventListener('keyup',release)
function release(e){
if (e.keyCode === 38 /* up */ || e.keyCode === 87 /* w */ || e.keyCode === 90 /* z */){
if (inverted) up = false;
  else down = false;
}
if (e.keyCode === 39 /* right */ || e.keyCode === 68 /* d */){
if (inverted) right = false;
else left = false;
}
if (e.keyCode === 40 /* down */ || e.keyCode === 83 /* s */){
if (inverted) down = false;
else up = false;
}
if (e.keyCode === 37 /* left */ || e.keyCode === 65 /* a */ || e.keyCode === 81 /* q */){
if (inverted) left = false;
else right = false;
}
}

document.addEventListener("mousewheel", zoom);

function zoom(e){
// e.preventDefault();

zoom_delta = e.deltaY;
//wheel = true;

var new_scale = scale + zoom_delta * zoom_scale;

// restriction of scaling
new_scale = Math.min(Math.max(zoom_min, new_scale), zoom_max);

var element = $("#movable_scene");
var position = element.position();
const x = position.left, y = position.top;
const parentRect = document.getElementById("movable_scene").parentNode.getBoundingClientRect();
// element.css("transform-origin", (mousePosX * scale - x * scale).toString() + "px " + (mousePosY * scale - y * scale).toString() + "px")
// element.css("left", 0);
// element.css("top", 0);
// (mousePosX - x) * (scale - 1)
var xPercent = ((mousePosX - x)).toFixed(2);
var yPercent = ((mousePosY - y)).toFixed(2);
var left = Math.round(mousePosX - parentRect.left - (xPercent * (new_scale / scale)));
var top = Math.round(mousePosY - parentRect.top - (yPercent * (new_scale / scale)));

element.css("transform", "scale(" + new_scale + ")");
element.css("left", left);
element.css("top", top);

scale = new_scale;
}

document.onmousemove = getCursorXY;
function getCursorXY(e){
mousePosX = (window.Event) ? e.pageX : e.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
mousePosY = (window.Event) ? e.pageY : e.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
}

// main movement function

function mainMovement(){
var element = $("#movable_scene");
var position = element.position();
var y = parseInt(position.top);
var x = parseInt(position.left);
var scale;

if (up){
    y = y - offset;
}
if (right){
    x = x + offset;
}
if (down){
    y = y + offset;
}
if (left){
    x = x - offset;
}

element.css("left", x);
element.css("top", y);
// wheel = false;

window.requestAnimationFrame(mainMovement)
}

window.requestAnimationFrame(mainMovement)
