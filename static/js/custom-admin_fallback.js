document.addEventListener("DOMContentLoaded", function () {
  const mapWrapper = document.getElementById("visitor-map-wrapper");
  const mapDiv = document.getElementById("visitor-map");

  if (!mapDiv) return;

  let map;
  let marker;

  function ensureGoogleMapsLoaded(cb) {
    if (window.google && window.google.maps) {
      cb();
      return;
    }
    if (window._gt_google_maps_loading) {
      window._gt_google_maps_callbacks.push(cb);
      return;
    }
    window._gt_google_maps_loading = true;
    window._gt_google_maps_callbacks = [cb];
    var script = document.createElement("script");
    var key = window.GOOGLE_MAPS_API_KEY || "";
    if (!key) {
      // No Google key: fall back to Leaflet (open-source) for development so map still shows
      loadLeaflet(function () {
        try {
          initLeafletMap({ lat: 0, lng: 0 });
        } catch (e) {}
      });
      window._gt_google_maps_loading = false;
      window._gt_google_maps_callbacks = [];
      return;
    }
    var src = "https://maps.googleapis.com/maps/api/js?key=" + encodeURIComponent(key) + "&libraries=marker";
    script.src = src;
    script.async = true;
    script.defer = true;
    script.onload = function () {
      window._gt_google_maps_loading = false;
      (window._gt_google_maps_callbacks || []).forEach(function (f) {
        try { f(); } catch (e) {}
      });
      window._gt_google_maps_callbacks = [];
    };
    script.onerror = function () {
      window._gt_google_maps_loading = false;
      window._gt_google_maps_callbacks = [];
      // On Google load failure, fall back to Leaflet so development can continue
      loadLeaflet(function () {
        // callbacks waiting for Google should be called with a noop; callers will detect absence of google.maps
        try { (window._gt_google_maps_callbacks || []).forEach(function(f){ try{ f(); }catch(e){} }); } catch(e){}
      });
    };
    document.head.appendChild(script);
  }

  document.querySelectorAll(".map-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();

      const lat = parseFloat(this.dataset.lat);
      const lng = parseFloat(this.dataset.lng);

      if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

      mapWrapper.style.display = "block";

      const position = { lat: lat, lng: lng };

      ensureGoogleMapsLoaded(function () {
        // If google.maps is available, use it; otherwise Leaflet will have been loaded as fallback
        if (window.google && window.google.maps) {
          if (!map) {
            map = new google.maps.Map(mapDiv, {
              zoom: 13,
              center: position,
            });

            try {
              if (google.maps.marker && google.maps.marker.AdvancedMarkerElement) {
                marker = new google.maps.marker.AdvancedMarkerElement({
                  position: position,
                  map: map,
                });
              } else {
                marker = new google.maps.Marker({
                  position: position,
                  map: map,
                });
              }
            } catch (e) {
              marker = new google.maps.Marker({
                position: position,
                map: map,
              });
            }
          } else {
            map.setCenter(position);
            if (marker) {
              if (typeof marker.setPosition === 'function') {
                marker.setPosition(position);
              } else if ('position' in marker) {
                marker.position = position;
              }
            }
          }
        } else {
          // Leaflet fallback: initialize or move marker
          if (!window._leaflet_map) {
            initLeafletMap(position);
          } else {
            window._leaflet_map.setView([position.lat, position.lng], 13);
            if (window._leaflet_marker) {
              window._leaflet_marker.setLatLng([position.lat, position.lng]);
            }
          }
        }
      });
    });
  });
  
  // --- Leaflet dynamic loader and initializer (fallback) ---
  function loadLeaflet(cb) {
    if (window.L && window.L.map) {
      cb();
      return;
    }
    if (window._gt_leaflet_loading) {
      window._gt_leaflet_callbacks.push(cb);
      return;
    }
    window._gt_leaflet_loading = true;
    window._gt_leaflet_callbacks = [cb];

    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);

    var script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.async = true;
    script.defer = true;
    script.onload = function () {
      window._gt_leaflet_loading = false;
      (window._gt_leaflet_callbacks || []).forEach(function (f) { try { f(); } catch (e) {} });
      window._gt_leaflet_callbacks = [];
    };
    script.onerror = function () {
      window._gt_leaflet_loading = false;
      window._gt_leaflet_callbacks = [];
    };
    document.head.appendChild(script);
  }

  function initLeafletMap(position) {
    // create map container if empty
    mapDiv.innerHTML = '';
    try {
      window._leaflet_map = L.map(mapDiv).setView([position.lat, position.lng], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(window._leaflet_map);
      window._leaflet_marker = L.marker([position.lat, position.lng]).addTo(window._leaflet_map);
    } catch (e) {
      // ignore
    }
  }
});

// document.addEventListener("DOMContentLoaded", function () {
//   const mapWrapper = document.getElementById("visitor-map-wrapper");
//   const mapDiv = document.getElementById("visitor-map");

//   if (!mapDiv) return;

//   let map;
//   let marker;

//   function ensureGoogleMapsLoaded(cb) {
//     if (window.google && window.google.maps) {
//       cb();
//       return;
//     }
//     if (window._gt_google_maps_loading) {
//       window._gt_google_maps_callbacks.push(cb);
//       return;
//     }
//     window._gt_google_maps_loading = true;
//     window._gt_google_maps_callbacks = [cb];
//     var script = document.createElement("script");
//     var key = window.GOOGLE_MAPS_API_KEY || "";
//     script.src = "https://maps.googleapis.com/maps/api/js?key=" + encodeURIComponent(key);
//     script.onload = function () {
//       window._gt_google_maps_loading = false;
//       (window._gt_google_maps_callbacks || []).forEach(function (f) {
//         try { f(); } catch (e) {}
//       });
//       window._gt_google_maps_callbacks = [];
//     };
//     script.onerror = function () {
//       window._gt_google_maps_loading = false;
//       window._gt_google_maps_callbacks = [];
//     };
//     document.head.appendChild(script);
//   }

//   document.querySelectorAll(".map-btn").forEach(btn => {
//     btn.addEventListener("click", function (e) {
//       e.preventDefault();

//       const lat = parseFloat(this.dataset.lat);
//       const lng = parseFloat(this.dataset.lng);

//       if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

//       mapWrapper.style.display = "block";

//       const position = { lat: lat, lng: lng };

//       ensureGoogleMapsLoaded(function () {
//         if (!map) {
//           map = new google.maps.Map(mapDiv, {
//             zoom: 13,
//             center: position,
//           });

//           marker = new google.maps.Marker({
//             position: position,
//             map: map,
//           });
//         } else {
//           map.setCenter(position);
//           if (marker) marker.setPosition(position);
//         }
//       });
//     });
//   });
// });
