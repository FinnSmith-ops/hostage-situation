
function initializeMap(loc){
    map = L.map('map').setView([loc.coords.latitude, loc.coords.longitude], 13);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', { 
        maxZoom: 19, 
    }).addTo(map); 
    map.on("click", function(e) {
    L.popup()
        .setLatLng(e.latlng)
        .setContent(
            "Lat: " + e.latlng.lat.toFixed(6) +
            "<br>Lng: " + e.latlng.lng.toFixed(6)
        )
        .openOn(map);
});

    
}


async function updateView(){
    function getLocation(){
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject)
        })
    }
    let lat;
    let long;
    const value = await getLocation()
    lat = value.coords.latitude;
    long = value.coords.longitude;

    data = {"lat": lat,
            "long": long,
            "game_id": document.getElementById("gameId").value}
    
    const response = await fetch("/update_location", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
    
    }
)
    const allLocations = await response.json();
    if(typeof markerGroup !== "undefined"){
        map.removeLayer(markerGroup);
    }
    markerGroup = L.layerGroup().addTo(map);
    
    for (const i of allLocations) {
        console.log(i[0])
        if(i[1] !== null && 
            i[1] !== undefined && 
            i[1] !== "null" && 
            i[1] !== "undefined" &&
            i[4] != null &&
            i[5] != null &&
            !isNaN(i[4]) &&
            !isNaN(i[5]) ){
            let marker = L.marker([i[4], i[5]]).addTo(markerGroup);
            marker.bindPopup(`<b>${i[1]}: ${i[3]}, ${i[0]}`)
    }
}
}

setInterval(updateView, 3000)
