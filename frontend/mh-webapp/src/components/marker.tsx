import React, { useCallback, useState } from 'react';
import { AdvancedMarker, InfoWindow, Pin, useAdvancedMarkerRef, useMap } from '@vis.gl/react-google-maps'
import { Easing, Tween, update } from '@tweenjs/tween.js'
import { FaLocationDot, FaWaze } from 'react-icons/fa6'
import '../App.css';

// initial center upon loading the page
export const INIT_CENTER = {lat: 1.86865, lng: 107.43795};

// data structure for a location
export interface Location {
  name: string;
  address: string;
  pos: { lat: number; lng: number };
  google: string;
  waze: string;
}

// for display marker function props
interface MarkerWithInfoWindowProps {
  loc: Location; // the store location
  highlight: (location: Location, km: number, map: google.maps.Map | null) => void; // function to attach to infowindow button
  highlighted: boolean; // should this marker be highlighted or not
  setHighlightedLocations: React.Dispatch<React.SetStateAction<Location[]>>; // function to set highlighted markers
  isCircleOrigin: boolean; // is this marker the origin of the circle
}

// function to display markers
function MarkerWithInfoWindow({loc,highlight,highlighted,setHighlightedLocations,isCircleOrigin}: MarkerWithInfoWindowProps) {
  const map = useMap('SUBWAY_MAP');

  const [markerRef, marker] = useAdvancedMarkerRef();
  const [infoWindowShown, setInfoWindowShown] = useState(false);

  // callback function when a marker is clicked
  const handleMarkerClick = useCallback(
    () => {
      // if map not found, exit
      if (!map) return;

      // ensure variables are not undefined
      let currCenter = map.getCenter();
      if (currCenter === undefined) {
        currCenter = new google.maps.LatLng(INIT_CENTER);
      }

      let currZoom = map.getZoom();
      if (currZoom === undefined) {
        currZoom = 6;
      }

      // camera for animation
      // this will be constantly changed throughout animation
      let cameraOptions = {
        center: currCenter.toJSON(),
        zoom: map.getZoom()
      };

      // only animate/pan when marker not clicked yet
      if (!infoWindowShown) {
        // if far, animate. otherwise just pan
        if (
          currCenter.lat() > loc.pos.lat+0.01 || 
          currCenter.lat() < loc.pos.lat-0.01 ||  
          currCenter.lng() > loc.pos.lng+0.01 || 
          currCenter.lng() < loc.pos.lng-0.01 || 
          currZoom < 13) {
          new Tween(cameraOptions)
            .to({center: loc.pos, zoom: 15}, 3000)
            .easing(Easing.Quadratic.Out)
            .onUpdate(() => {
              map.moveCamera(cameraOptions);
            })
            .start();

          function animate(time: number) {
            requestAnimationFrame(animate);
            update(time);
          }

          requestAnimationFrame(animate)
        } else {
          map.panTo(loc.pos)
          if (currZoom < 15) map.setZoom(15);
        }
      }
      
      // toggle infowindow
      return setInfoWindowShown(isShown => !isShown);
    },
    [map, loc, infoWindowShown]
  );

  // callback function when infowindow is closed
  const handleClose = useCallback(() => {
    setInfoWindowShown(false);
    // if marker is the origin of circle, remove circle and unhighlight markers
    if (isCircleOrigin) {
      highlight(loc,0,map);
      setHighlightedLocations([]);
    }
  }, [isCircleOrigin, highlight, loc, map, setHighlightedLocations]);

  return (
    <>
      <AdvancedMarker position={loc.pos} ref={markerRef} onClick={handleMarkerClick}>
        <Pin background={highlighted ? '#FBBC04' : undefined} />
      </AdvancedMarker>
      {infoWindowShown && (
        <InfoWindow anchor={marker} onClose={handleClose} style={{color:'black'}} headerContent={<h3 style={{color:'black'}}>{loc.name}</h3>}>
          <p className='address'>{loc.address}</p>
          <p></p>
          <p>
            <a href={loc.google} target='noreferrer noopener'>
              <FaLocationDot size={25}/>
            </a>
            <a href={loc.waze} target='noreferrer noopener'>
              <FaWaze size={25}/>
            </a>
          </p>
          <button className='btn-highlight' onClick={() => highlight(loc, 5, map)}>See other stores within 5 km</button>
        </InfoWindow>
      )}
    </>
  )
}

// function called when see other stores button in any infowindow is clicked
// calculates distance to closest stores within radius and highlights them
// generates a circle around selected store
export function seeOtherStoresWithinRadius(
  loc: Location, // location of selected store
  km: number, // radius in KM
  locations: Location[], // locations of all stores
  setHighlightedLocations: React.Dispatch<React.SetStateAction<Location[]>>, // state function to highlight stores
  map: google.maps.Map | null, // the map
  setCenter: React.Dispatch<React.SetStateAction<{ lat: number; lng: number; }>>, // state function for circle center
  setRadius: React.Dispatch<React.SetStateAction<number>>) /* state function for circle radius */ { 
  // haversine distance function, used to calculate distance between two points on earth given lat and lng.
  // more info: https://www.movable-type.co.uk/scripts/latlong.html
  const haversineDistance = (pos1: { lat: number; lng: number }, pos2: { lat: number; lng: number }) => {
    const toRad = (x: number) => (x * Math.PI) / 180;
    const R = 6371; // Earth's radius in kilometers

    const dLat = toRad(pos2.lat - pos1.lat);
    const dLon = toRad(pos2.lng - pos1.lng);
    const lat1 = toRad(pos1.lat);
    const lat2 = toRad(pos2.lat);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
  };

  // filter locations if <= km
  const filteredLocations = locations.filter(
    (location) => haversineDistance(loc.pos, location.pos) <= km
  );
  setHighlightedLocations(filteredLocations);

  // zoom out to see full circle
  if (map) {
    map.setZoom(13);
    map.panTo(loc.pos);
  }

  // adjust circle
  setCenter(loc.pos);
  setRadius(km * 1000);
}

export default MarkerWithInfoWindow;