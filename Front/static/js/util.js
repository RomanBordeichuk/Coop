
function showCars(event){
    var status = true;
    if (status) {
        $("#car").css("visibility", "visible");
        const table_cars_info = document.getElementById('table_cars_info');
        let count =  document.querySelectorAll('.car');
        for(let i = 0; i < count.length; i++){
            const car = count[i];

            let car_lable = document.createElement('div');
            car_lable.classList.add('table_info_span_car');
            car_lable.textContent = 'Car ' + car.id;

            car_lable.addEventListener('click', focus_car);
            function focus_car() {
                const wind = document.querySelector('#movable_scene');
                let x = parseInt(car.style.left);
                let y = parseInt(car.style.top);
                console.log(x, y);
                document.getElementById('cars_editor').style.visibility = 'visible';
                show_car(car.id)
            }

            table_cars_info.append(car_lable);
        }
    }
}

function showLights(event){
    var status = true;
    if (status) {
        $("#lights").css("visibility", "visible");
        const table_lights_info = document.getElementById('table_lights_info');
        let count =  document.querySelectorAll('.light');
        console.log(count);
        for(let i = 0; i < count.length; i++){
            const light = count[i];

            let light_lable = document.createElement('div');
            light_lable.classList.add('table_info_span_light');
            light_lable.textContent = light.id;

            light_lable.addEventListener('click', focus_light);
            function focus_light() {
                let light_id = +light.id.slice(6, light.id.length);
                console.log(light_id);
                get_light_editor(light_id)
                showLightsEditor();
            }

            table_lights_info.append(light_lable);
        }
    }
}

function showRoads(event){
    var status = true;
    if (status) {
        $("#roads").css("visibility", "visible");
        const table_roads_info = document.getElementById('table_roads_info');
        let count =  document.querySelectorAll('.road');
        console.log(count);
        for(let i = 0; i < count.length; i++){
            const road = count[i];

            let road_lable = document.createElement('div');
            road_lable.classList.add('table_info_span_road');
            road_lable.textContent = road.id;

            road_lable.addEventListener('click', focus_road);
            function focus_road() {
                let road_id = +road.id.slice(5, road.id.length);
                show_road(road_id);
            }

            table_roads_info.append(road_lable);
        }
    }
}

function showMenu(event){
    var status = true;
    if (status) {
        $("#menu_param").css("visibility", "visible");
    }
    
}

function closeButton(event){
    var status = true;
    if (status) {
        $("#menu_param").css("visibility", "hidden");
        $("#roads").css("visibility", "hidden");
        $("#lights").css("visibility", "hidden");
        $("#car").css("visibility", "hidden");
    }
    
}

function closeCars(event){
    var status = true;
    if (status) {
        $("#car").css("visibility", "hidden");
        document.getElementById('table_cars_info').textContent = '';
    }
    
}

function closeLights(event){
    var status = true;
    if (status) {
        $("#lights").css("visibility", "hidden");
        document.getElementById('table_lights_info').textContent = '';
    }
    
}

function closeRoads(event){
    var status = true;
    if (status) {
        $("#roads").css("visibility", "hidden");
        document.getElementById('table_roads_info').textContent = '';
    }
    
}

function showLightsEditor(event){
    var status = true;
    if(status){
        $("#lights_editor").css("visibility", "visible");
    }
}
function closeLightsEditor(event){
    var status = true;
    if(status){
        $("#lights_editor").css("visibility", "hidden");
    }
}


function showCarsEditor(event){
    var status = true;
    if(status){
        $("#cars_editor").css("visibility", "visible");
    }
}
function closeCarsEditor(event){
    var status = true;
    if(status){
        $("#cars_editor").css("visibility", "hidden");
    }
}

function hide_all(event){
    var status = true;
    if(status){
        closeLightsEditor();
        closeCarsEditor();
        document.querySelectorAll('.road_highlight').forEach(e => e.remove());
        // todo everything else as well
    }
}

function submit_lights_editor_form(){
    // need to check if user was typing in the right thing, (it should be positive and not blank)
    if(document.getElementById("green_period_input") == "0" ||
     document.getElementById("red_period_input") == "0") return;
    document.getElementById("lights_editor_form").submit();
    hide_all();
}