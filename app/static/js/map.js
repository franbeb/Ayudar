let map;
let marker;

const mapClickHandler = (e) =>{
    addMarker(e.latlng);


};
const addMarker  =({lat,lng}) => {

    if (marker) marker.remove();
    marker= L.marker([lat,lng]).addTo(map);
    //latlng= marker.getLatLng();
    //document.getElementById('probando').setAttribute('value',latlng.lng + '-'+ latlng.lat);

};
 const addSearchControl= () =>{
    L.control.scale().addTo(map);
    
    let searchControl = new L.esri.Controls.Geosearch().addTo(map);
    let results = new L.LayerGroup().addTo(map);
    searchControl.on('results',(data) =>{

    results.clearLayers();
    if (data.results.length > 0){
        addMarker(data.results[0].latlng)

    }
});


}; 
const initializeMap =(selector) =>{
    var longitud = document.getElementById('longitud').getAttribute('value');
    var latitud =document.getElementById('latitud').getAttribute('value');
    if (longitud & latitud){
        map = L.map(selector).setView([latitud,longitud],13);
        marker= L.marker([latitud,longitud]).addTo(map);
    }
    else{
        map = L.map(selector).setView([-34.9187,-57.956],13);

    }
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    //addSearchControl();
    map.on('click',mapClickHandler);



};

const submitHandler = (event) =>{
    if (!marker){
        event.preventDefault();

        alert('Debes seleccionar una ubicacion en el mapa');


    }
    else{
        latlng= marker.getLatLng();
        
        document.getElementById('longitud').setAttribute('value',latlng.lng);
        document.getElementById('latitud').setAttribute('value',latlng.lat);


    }


};
window.onload = () =>{
    initializeMap('mapid');

};
