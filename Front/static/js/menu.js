let paused = false;
let started = false;
let speed = 2000; // 1/2 call per second
let eventCars = null;
let eventLights = null;


const onPause = () => {
    paused = !paused;

    if (started && !paused)
    {
        setIntervals();
        hide_all();
        $("#button_pause").text("Pause");
        $("#navigator").css("visibility", "hidden");  
        // $("#button_start").text("Stop");
        
    }
        
    if (paused)
    {
        clearIntervals();
        // $("#button_start").text("Start");
        $("#button_pause").text("Resume");
        $("#navigator").css("visibility", "visible");  
    }
    
}

const onStart = () => {
    started = !started;

    if (started)
    {
        setMap();
        setIntervals();
        $("#button_pause").text("Pause");
        $("#button_start").text("Stop");
        $("#button_pause").css("visibility", "visible");
        $("#speed_menu").css("visibility", "visible");
        $("#price").css("visibility", "visible");
    }
    else
    {
        $("#button_pause").css("visibility", "hidden");
        $("#button_pause").text("Pause");
        $("#button_start").text("Start");
        $("#speed_menu").css("visibility", "hidden");
        $("#map").html("");
        $("#cars").html("");
        $("#lights_movable").html("");        
        clearIntervals();
        paused = false;
    }
}

function setIntervals(){
    eventCars = setInterval(setCars, speed);
    eventPrice = setInterval(setPrice, speed+100);
}

function clearIntervals(){
    clearInterval(eventCars);
    clearInterval(eventPrice);
}

const setSpeed = (value) => {
    $("#speed_display").text("Speed in ms: " + value.toString());
    speed = parseInt(value);
    clearIntervals();
    setIntervals();
}
