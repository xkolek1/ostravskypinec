# Remake of ostravskypinec.cz website  
The website runs on simple HTML/CSS/JS  

**Structure:**  
- `index.html` – home page  
- `` – other pages  
- `components/` – reusable header, footer, sponsors, sidebar...  
- `assets/` – images, css, js, fonts  
  - `js/`  
      - `indent.js` - needs to be linked for using `components/`, accepts id="$component"-placeholder  
  
**The website uses iframes for 2 sections in the sidebar:**  
  "Nejbližší akce" - uses "Google Calendar"; actions has to be added there  
  "Oddíly" - uses "Mapy.cz" map of the playing club fields; has to be checked and updated at least yearly  
  
More soon ;)
