    
async function updateMap(){    
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


let count = 0;
let map;
let markerGroup
navigator.geolocation.getCurrentPosition(initializeMap)