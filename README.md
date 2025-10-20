# Remake of ostravskypinec.cz website --IN PROGRESS--
The website runs on simple HTML/CSS/JS  

**Structure:**  
- `index.html` – home page 
- `components/` – reusable header, footer, sponsors, sidebar...
- `pages/` - had to be removed due to linking difference between local and github -> pages in the root repository for now  
- `assets/` – images, css, js, fonts  
  - `js/`  
      - `include.js` - needs to be linked for using `components/`, accepts id="$component"-placeholder
      - `index-turnaje.js` - deals with opening lists of tournaments in index
      - `pagination.js` - deals with paging of lists 
  -`css` - not fully done yet ---else.css
  
**The website uses iframes for 2 sections in the sidebar:**  
  "Nejbližší akce" - uses "Google Calendar"; actions has to be added there  
  "Oddíly" - uses "Mapy.cz" map of the playing club fields; has to be checked and updated at least yearly

**Progress comentary**  
  "index" - structure done, links have to be added  
  "turnaje" - pagination done, structure not rly, links missing  
  "soutěže" - some improvement may be needed, for now just a link to stis.cz  
  "foto" - missing  
  "zpravodaje" - main idea done with pagination, links missing  
  "svaz" - no relevant data yet  

  !! automatization idea - push of document into the repository generates json, info from json is printed into "turnaje" also possibly --aktualizace-- section, doc of tournament is added automaticaly to index page of its own category - category also takes date of tournament straight from calendar !! -> before 1st tournament will be necesarry to clear the tournament info & before new season to create new season page in "turnaje"
    ---**not implemented yet**  
  !! maybe simple ai for autocreating calendar events from tournament docs? - then also everything else can be fully automated? !!

**unfixed errors** - header (-bcs of the photos - but the diff doesnt look bad) and footer (-just weird) has to be unified between index and other pages
**documentation** - missing/not good  

More soon ;)
