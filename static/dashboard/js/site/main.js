
  document.addEventListener('DOMContentLoaded', async function() {
    function setBodyAttributes(options = {}) {
      const body = document.body;
      const defaults = {
        pcDirection: 'ltr',
        pcPreset: 'preset-6',
        pcTheme: 'dark',
        fontFamily: "'Public Sans', sans-serif"
      };
      const settings = { ...defaults, ...options };

      body.className = settings.bodyClass;
      body.setAttribute('data-pc-direction', settings.pcDirection);
      body.setAttribute('data-pc-preset', settings.pcPreset);
      body.setAttribute('data-pc-theme', settings.pcTheme);
      body.style.fontFamily = settings.fontFamily;
    }

    setBodyAttributes({
      pcPreset: 'preset-6',
    });

    if(document.getElementById("player")){

      const Player = (await import("../libs/plyr")).default;

      const player = new Player('#player', {
        controls: ['play', 'progress', 'current-time', 'duration', 'mute', 'volume', 'captions', 'settings', 'fullscreen'],
        settings: ['quality', 'speed'],
        autoplay: false,
        speed: { selected: 1, options: [0.5, 1, 1.5, 2] }
      });

      // Initialize Plyr for video modals
      if(document.getElementById("videoModal")){
        // Event when modal closes
        document.getElementById("videoModal").addEventListener("hidden.bs.modal", () => {
          player.pause();
        });
      }
    }

  });
