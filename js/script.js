// addLineRoad(100, 200, 400, 0);
// addTcrossing(50, 50, 0);
// addXcrossing(50, 50, 0);
// addSetCrossing(50, 50);

const root = document.body;

function addLineRoad(x, y, length, incline){
    const road = document.createElement('div');
    road.classList.add('road');

    road.style.left = x + 'px';
    road.style.top = y + 'px';
    road.style.width = length + 'px';
    road.style.transform = 'rotate(' + incline + 'deg)';

    root.prepend(road);
}

function addTcrossing(x, y, incline){
    const Tcross = document.createElement('div');
    Tcross.classList.add('t_cross');

    Tcross.style.left = x + 'px';
    Tcross.style.top = y + 'px';
    Tcross.style.transform = 'rotate(' + incline + 'deg)';

    root.prepend(Tcross);
}

function addXcrossing(x, y, incline){
    const Xcross = document.createElement('div');
    Xcross.classList.add('x_cross');

    Xcross.style.left = x + 'px';
    Xcross.style.top = y + 'px';
    Xcross.style.transform = 'rotate(' + incline + 'deg)';

    root.prepend(Xcross);
} 
function addSetCrossing(x, y){
    const mainCircle = document.createElement('div');
    const pavement = document.createElement('div');
    mainCircle.classList.add('main_circle');
    pavement.classList.add('main_circle_border');

    mainCircle.style.left = x + 15 + 'px';
    mainCircle.style.top = y + 15 + 'px';
    pavement.style.left = (x + 10) + 'px';
    pavement.style.top = (y + 10) + 'px';

    root.prepend(mainCircle);
    root.prepend(pavement);
}
