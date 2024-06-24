import React, { useState, useEffect } from 'react';
import './App.css';
import { APIProvider, Map } from '@vis.gl/react-google-maps'
import { Circle } from './components/circle';
import { API_KEY } from './api_key'
import MarkerWithInfoWindow, { Location, INIT_CENTER, seeOtherStoresWithinRadius } from './components/marker'

const App: React.FC = () => {
  // locations to be displayed on map
  const [locations, setLocations] = useState<Location[]>([]);

  // locations to be highlighted
  const [highlightedLocations, setHighlightedLocations] = useState<Location[]>([]);

  // states for circle
  const [center, setCenter] = React.useState(INIT_CENTER);
  const [radius, setRadius] = React.useState(0);

  // states for page statuses
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [apiLoaded, setApiLoaded] = useState(false);

  // retrieve all subway locations once
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
        setError(error as Error);
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
        <APIProvider apiKey={API_KEY} onLoad={() => {console.log('Maps API loaded.'); setApiLoaded(true)}}>
          {apiLoaded && (
            <Map
              style={{width: '100vw', height: '100vh'}}
              defaultCenter={INIT_CENTER}
              defaultZoom={6}
              gestureHandling={'greedy'}
              disableDefaultUI={true}
              mapId={'SUBWAY_MAP'}
              id={'SUBWAY_MAP'}
              onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
            >
              {/* if circle has a radius, display it */}
              {radius>0 && (
                <Circle
                  center={center}
                  radius={radius}
                  strokeColor={'#0c4cb3'}
                  strokeOpacity={1}
                  strokeWeight={3}
                  fillColor={'#3b82f6'}
                  fillOpacity={0.3}
                  editable={false}
                  draggable={false}
                />
              )}
              {/* for each location, display marker */}
              {locations.map((loc, index) => (
                <MarkerWithInfoWindow
                  key={index}
                  loc={loc}
                  highlight={(location, km, map) => seeOtherStoresWithinRadius(location, km, locations, setHighlightedLocations, map, setCenter, setRadius)}
                  highlighted={highlightedLocations.some(highlightedLoc => highlightedLoc.name === loc.name)}
                  setHighlightedLocations={setHighlightedLocations}
                  isCircleOrigin={(loc.pos.lat===center.lat) && (loc.pos.lng===center.lng)}
                />
              ))}
            </Map>
          )}
        </APIProvider>
      </header>
    </div>
  );
}

export default App;