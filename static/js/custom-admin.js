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

//       // AUTO NAVIGATE CURSOR TO MAP
//       mapWrapper.scrollIntoView({
//         behavior: "smooth",
//         block: "start"
//       });

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
    script.src = "https://maps.googleapis.com/maps/api/js?key=" + encodeURIComponent(key);
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

      // AUTO NAVIGATE CURSOR TO MAP
      mapWrapper.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });

      const position = { lat: lat, lng: lng };

      ensureGoogleMapsLoaded(function () {
        if (!map) {
          map = new google.maps.Map(mapDiv, {
            zoom: 13,
            center: position,
          });

          marker = new google.maps.Marker({
            position: position,
            map: map,
          });
        } else {
          map.setCenter(position);
          if (marker) marker.setPosition(position);
        }
      });
    });
  });
});

// Spectra sidebar label tweak: replace long auth app label if present
document.addEventListener("DOMContentLoaded", function () {
  try {
    var nodes = document.querySelectorAll('.nav-text');
    nodes.forEach(function (n) {
      if (n.textContent && n.textContent.trim() === 'Authentication and Authorization') {
        n.textContent = 'Auth and Authorization';
      }
    });
  } catch (e) {
    // safe noop
  }
});
