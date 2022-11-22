const canvas = document.getElementById('map');
const mapView = new harp.MapView({
   canvas,
   theme: "https://unpkg.com/@here/harp-map-theme@latest/resources/berlin_tilezen_night_reduced.json"
});

let car_speed = 2000;
let paused_3d = false;
let started_3d = false;
let eventCars_3d = null;

// center the camera to New York
mapView.lookAt({
  target: new harp.GeoCoordinates(48.92312, 24.71248),
  zoomLevel: 17,
  tilt: 40,
});

const mapControls = new harp.MapControls(mapView);
const ui = new harp.MapControlsUI(mapControls);
canvas.parentElement.appendChild(ui.domElement);

mapView.resize(window.innerWidth, window.innerHeight);
window.onresize = () => mapView.resize(window.innerWidth, window.innerHeight);

const vectorTileDataSource = new harp.VectorTileDataSource({
   authenticationCode: 'vcbAYK2YRECdifbEDVkAtVmWlwlS7kYVoZ8PeYKGYVw',
});
mapView.addDataSource(vectorTileDataSource);

//window.addEventListener("click", (evt) => {
//   //Create the three.js cube
//   const geometry = new THREE.BoxGeometry(100, 100, 100);
//   const material = new THREE.MeshStandardMaterial({ color: 0x00ff00fe });
//   const cube = new THREE.Mesh(geometry, material);
//   cube.renderOrder = 100000;
//
//   //Get the position of the click
//   const geoPosition = mapView.getGeoCoordinatesAt(48.92312, 24.71248);
//   cube.anchor = geoPosition;
//
//   //Add object to the map
//   mapView.mapAnchors.add(cube);
//   mapView.update();
//});

function addCar(){
        //Create the three.js cube
        const geometry = new THREE.BoxGeometry(100, 100, 100);
        const material = new THREE.MeshStandardMaterial({ color: 0x00ff00fe });
        const cube = new THREE.Mesh(geometry, material);
        cube.renderOrder = 100000;

        //Get the position of the click
        const geoPosition = mapView.getGeoCoordinatesAt(48.92312, 24.71248);
        cube.anchor = geoPosition;

        //Add object to the map
        mapView.mapAnchors.add(cube);
        mapView.update();

}

const Speed = (value) => {
    $("#speed_display").text("Speed in ms: " + value.toString());
    car_speed = parseInt(value);
    clearIntervals_3d();
    setIntervals_3d();
}

function createCar(x, y){
        //Create the three.js cylinder
        const geometry = new THREE.CylinderGeometry( 5, 5, 20, 32 );
        const material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
        const cylinder = new THREE.Mesh(geometry, material);
        cylinder.renderOrder = 100000;

        //Get the position of the click
        const geoPosition = mapView.getGeoCoordinatesAt(y, x);
        cylinder.anchor = geoPosition;

        //Add object to the map
        mapView.mapAnchors.add(cylinder);
        mapView.update();

        //setTimeout(() => {
        //    mapView.mapAnchors.remove(cylinder)
        //}, car_speed);

        console.log('car was created')
        console.log(x, y)

}

function setCars3d() {
    if(!map_ajax_state_sending){
        map_ajax_state_sending = true
        $.ajax({
        url: "/car_3d",
        type: "GET",
        cache: false,
        success: function(response) {
            //$('#cars').html(response);
            map_ajax_state_sending = false; 
            console.log(response);
            eval(response);
            console.log('one new request')
            },

        });
        return false;
    }
}; 

const onStart_3d = () => {
    started_3d = !started_3d;

    if (started_3d)
    {
        setIntervals_3d();
        $("#button_pause").text("Pause");
        $("#button_start").text("Stop");
        $("#button_pause").css("visibility", "visible");
        $("#speed_menu").css("visibility", "visible");
    }
    else
    {
        $("#button_pause").css("visibility", "hidden");
        $("#button_pause").text("Pause");
        $("#button_start").text("Start");
        $("#speed_menu").css("visibility", "hidden");
        $("#map").html("");
        $("#cars").html("");        
        clearIntervals_3d();
        paused_3d = false;
    }
}

const onPause_3d = () => {
    paused_3d = !paused_3d;

    if (started_3d && !paused_3d)
    {
        setIntervals_3d();
        $("#button_pause").text("Pause");
        $("#navigator").css("visibility", "hidden");  
        $("#button_start").text("Stop");
        
    }
        
    if (paused_3d)
    {
        clearIntervals_3d();
        $("#button_start").text("Start");
        $("#button_pause").text("Resume");
        $("#navigator").css("visibility", "visible");  
    }
    
}

function setIntervals_3d(){
    eventCars_3d = setInterval(setCars3d, car_speed);
}

function clearIntervals_3d(){
    clearInterval(eventCars_3d);
}

createCar(48.93312, 24.81248);
createCar(48.92104292204861, 24.708878438194443)