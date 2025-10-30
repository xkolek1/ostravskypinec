# Remake of ostravskypinec.cz website --IN PROGRESS--  

This project is a complete remake of the official website for the Ostrava City Table Tennis Association. It's built with simple HTML/CSS/JS and includes a Python-based automation system for content management.

---

## ✨ Key Features & Automation

The core of this project is an automated content pipeline using **GitHub Actions**. Instead of manually editing HTML, this system automatically updates the website's content when new files are added to the repository.

### How it works:
1.  **Add Files:** A user simply adds a new tournament regulations PDF to `/assets/propozice/nnnn/` or a new photo album folder to `/assets/images/albums/`.
2.  **Trigger Automation:** Pushing the new files to the `main` branch automatically triggers a GitHub Actions workflow.
3.  **Run Python Script:** The workflow executes a Python script (`/scripts/update_json.py`) which:
    * Scans all content directories (`propozice`, `vysledky`, `foto`, etc.).
    * For new PDFs, it **extracts the tournament dates** directly from the text.
    * For new photo albums, it finds the first image for a preview and **generates a complete list of all filenames** within that album (e.g., `["0.jpg", "0(2).jpg", ...]`).
4.  **Generate `data.json`:** The script updates `data.json`, which serves as a central database for all dynamic content on the site.
5.  **Dynamic Frontend:** JavaScript on the live website fetches this `data.json` file and dynamically generates the HTML to display the latest tournaments and photo galleries.

---

## 📂 Project Structure

-   `index.html` – Home page
-   `turnaje.html`, `zpravodaje.html` – Paginated content pages.
-   `foto.html` – Paginated photo album grid.
-   `album.html` – Dynamic page for displaying photos from a single album.
-   `svaz.html` – Static content page.
-   `components/` – Reusable HTML snippets (header, footer, sponsors, sidebar).
-   `assets/` – All static assets.
    -   `js/`
        -   `include.js` - Handles the inclusion of reusable `components/`.
        -   `index-turnaje.js` - Manages the collapsible tournament accordion on `index.html`.
        -   `pagination.js` - Controls all pagination logic for `foto.html`, `turnaje.html`, and `zpravodaje.html`.
        -   `album-loader.js` - Dynamically loads photos into `album.html` based on URL parameters.
    -   `css/`
        -   `general.css` – Global styles (header, footer, layout, variables).
        -   `sidebar.css` – Styles for the sidebar.
        -   `index.css` – Styles only for `index.html` (slider, accordion, buttons).
        -   `list-item.css` – Shared styles for list items (used on index, turnaje, zpravodaje).
        -   `pagination.css` – Shared pagination styles for all paginated pages.
        -   `foto.css` – Grid styles for the album overview on `foto.html`.
        -   `album.css` – Grid styles for the individual photos on `album.html`.
-   `.github/workflows/` – Contains the YAML file for the GitHub Actions automation.
-   `scripts/` – Contains the Python script for generating the JSON.
-   `data.json` – The auto-generated database of website content.

---

## <iframe> Third-Party Integrations

The website uses iframes for two sections in the sidebar:
-   **"Nejbližší akce" (Upcoming Events):** An embedded Google Calendar. Events need to be added there.
-   **"Oddíly" (Clubs):** An embedded Mapy.cz map showing the locations of club halls. This should be checked and updated at least once a year.

---

## 📝 Progress Commentary & To-Do

-   **index:** `[IMPLEMENTED]` Structure is done. Collapsible accordion works. 
-   **turnaje (tournaments):** `[IMPLEMENTED]` Fully functional. Dynamically loads all seasons from `data.json` into a paginated view.
-   **soutěže (leagues):** `[IMPLEMENTED]` Currently just a link to stis.cz.
-   **foto (photos):** `[IMPLEMENTED]` Fully functional. 
    -   `foto.html` displays a paginated grid of all albums loaded from `data.json`.
    -   Page state is preserved in the URL (`?page=N`).
    -   Clicking an album navigates to a dynamic `album.html?album=...&returnPage=N` page.
    -   `album.html` dynamically loads *all* photos for that specific album, based on the `photos` array in `data.json`.
    -   The system correctly handles both Cloudflare and local image paths based on the `previewImage` URL.
-   **zpravodaje (newsletters):** `[IMPLEMENTED]` Fully functional. Dynamically loads all seasons from `data.json` into a paginated view.
-   **svaz (association):** `[IMPLEMENTED]` Static content page is complete.

### Automation & Future Plans:
-   **`[IMPLEMENTED]`** **Automatic JSON Generation:** The Python script (`scripts/update_json.py`) now handles all content aggregation. It scans all asset folders (`propozice`, `vysledky`, `zpravodaje`, `foto`, `zebricky`) and:
    -   Finds new PDF documents and adds them to `data.json` with the correct season.
    -   Extracts tournament dates directly from PDF text.
    -   Finds new photo album folders.
    -   **Generates a complete list of all photo filenames** (`photos: [...]`) for each album, allowing for non-sequential or messy filenames.
    -   Assigns a preview image and display name.
-   **`[TO-DO]`** **Auto-creating Google Calendar events and printing them into index tournament info:** The next step is to create a script (e.g., Google Apps Script) that reads `data.json` and automatically creates events in the embedded Google Calendar. Index should be fully automatical.

---

## 🐛 Unfixed Errors & Documentation
-   **Not known**  
-   **Documentation:** Missing/not good/AI yapping. Needs to be improved.  

More soon ;)
