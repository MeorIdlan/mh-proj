import React, { useCallback, useState, useEffect } from 'react';
import './App.css';
import { APIProvider, AdvancedMarker, InfoWindow, Map, useAdvancedMarkerRef, useMap } from '@vis.gl/react-google-maps'
import { Easing, Tween, update } from '@tweenjs/tween.js'

function MarkerWithInfoWindow({loc}) {
  const map = useMap('SUBWAY_MAP');

  const [markerRef, marker] = useAdvancedMarkerRef();
  const [infoWindowShown, setInfoWindowShown] = useState(false);

  const handleMarkerClick = useCallback(
    () => {
      if (!map) return;

      let cameraOptions = {
        center: map.getCenter().toJSON(),
        zoom: map.getZoom()
      };
      if (!infoWindowShown) {
        // if far, animate. otherwise just pan
        if (
          map.getCenter().lat() > loc.pos.lat+0.01 || 
          map.getCenter().lat() < loc.pos.lat-0.01 ||  
          map.getCenter().lng() > loc.pos.lng+0.01 || 
          map.getCenter().lng() < loc.pos.lng-0.01 || 
          map.getZoom() < 13) {
          new Tween(cameraOptions)
            .to({center: loc.pos, zoom: 15}, 3000)
            .easing(Easing.Quadratic.Out)
            .onUpdate(() => {
              map.moveCamera(cameraOptions);
            })
            .start();

          function animate(time) {
            requestAnimationFrame(animate);
            update(time);
          }

          requestAnimationFrame(animate)
        } else {
          map.panTo(loc.pos)
          if (map.getZoom() < 15) map.setZoom(15);
        }
      }
      
      return setInfoWindowShown(isShown => !isShown)
    },
    [map, loc, infoWindowShown]
  );
  const handleClose = useCallback(() => setInfoWindowShown(false), []);

  return (
    <>
      <AdvancedMarker position={loc.pos} ref={markerRef} onClick={handleMarkerClick}/>
      {infoWindowShown && (
        <InfoWindow anchor={marker} onClose={handleClose} style={{color:'black'}}>
          <h2>{loc.name}</h2>
          <p>{loc.address}</p>
        </InfoWindow>
      )}
    </>
  )
}

function App() {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch('http://localhost:5000/dev-api/subway-locations');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setLocations(data.locations);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
      }
    };

    fetchLocations();
  }, []);

  // if loading, display this
  if (loading) {
    return (
      <div id="app" className="App">
        <header className="App-header">
          <h1>Subway Surfer (get it?)</h1>
          <div>Loading...</div>
        </header>
      </div>
    )
  }

  // if error on fetch, display this
  if (error) {
    return (
      <div id="app" className="App">
        <header className="App-header">
          <h1>Subway Surfer (get it?)</h1>
          <div>Error: {error.message}</div>
        </header>
      </div>
    )
  }

  return (
    <div id="app" className="App">
      <header className="App-header">
        <h1>Subway Surfer (get it?)</h1>
        <APIProvider apiKey='API_KEY_HERE' onLoad={() => console.log('Maps API loaded.')}>
          <Map
            style={{width: '100vw', height: '100vh'}}
            defaultCenter={{lat: 1.86865, lng: 107.43795}}
            defaultZoom={6}
            gestureHandling={'greedy'}
            disableDefaultUI={true}
            mapId={'SUBWAY_MAP'}
            id={'SUBWAY_MAP'}
            onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
          >
            {locations.map((loc, index) => (
              <MarkerWithInfoWindow loc={loc} />
            ))}
          </Map>
        </APIProvider>
      </header>
    </div>
  );
}

export default App;