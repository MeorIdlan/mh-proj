import React, { useState, useEffect } from 'react';
import './App.css';
import { APIProvider, Map } from '@vis.gl/react-google-maps'
import { Circle } from './components/circle';
import { API_KEY } from './api_key'
import MarkerWithInfoWindow, { Location, INIT_CENTER, seeOtherStoresWithinRadius } from './components/marker'
import { allPostcodes } from 'malaysia-postcodes';

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

  // filtered locations based on search query
  const [filteredLocations, setFilteredLocations] = useState<Location[]>([]);

  // state for search query
  const [searchQuery, setSearchQuery] = useState('');

  // retrieve all subway locations once
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch('http://localhost:5000/dev-api/subway-locations');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        // error handling
        if (data.locations && Array.isArray(data.locations) && typeof data.locations === 'object') {
          setLocations(data.locations);
          setFilteredLocations(data.locations);
          setLoading(false);
        } else {
          if (data.locations) {
            throw Error(`Error message: ${data.locations.message}\nError code: ${data.locations.code}`);
          } else {
            throw Error('Something went wrong during retrieving locations.')
          }
        }
      } catch (error) {
        setError(error as Error);
        setLoading(false);
      }
    };

    fetchLocations();
  }, []);

  // filter locations on pressing Enter in query box
  const handleSearchEnter = async (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      const query = (event.target as HTMLInputElement).value;
      if (query === '') {
        setFilteredLocations(locations);
      } else {
        
        const response = await fetch('http://localhost:5000/api/complex-query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query, locations: locations, allPostcodes })
        });
        const result = await response.json();
        if (result.locations.length > 0) {
          setFilteredLocations(result.locations);
        } else {
          setFilteredLocations(locations.filter(
            loc => loc.name.toLowerCase().includes(query.toLowerCase()) || loc.address.toLowerCase().includes(query.toLowerCase())
          ))
        }
      }
    }
  };

  // for updating query box with text
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const query = event.target.value;
    setSearchQuery(query);
  };

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
        <div style={{ paddingBottom: '15px', width: '50%' }}>
          <input
            type="text"
            className="query"
            placeholder="Search for a location"
            value={searchQuery}
            onChange={handleSearchChange}
            onKeyDown={handleSearchEnter}
          />
        </div>
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
              {filteredLocations.map((loc, index) => (
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