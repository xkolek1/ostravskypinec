# Remake of ostravskypinec.cz website --IN PROGRESS--

This project is a complete remake of the official website for the Ostrava City Table Tennis Association. It's built with simple HTML/CSS/JS and includes a Python-based automation system for content management.

---

## ✨ Key Features & Automation

The core of this project is an automated content pipeline using **GitHub Actions**. Instead of manually editing HTML, this system automatically updates the website's content when new files are added to the repository.

### How it works:
1.  **Add Files:** A user simply adds a new tournament regulations PDF to `/assets/propozice/` or a new photo album folder to `/assets/images/albums/`.
2.  **Trigger Automation:** Pushing the new files to the `main` branch automatically triggers a GitHub Actions workflow.
3.  **Run Python Script:** The workflow executes a Python script (`/scripts/update_json.py`) which:
    * Scans the content directories for new files.
    * For new PDFs, it **extracts the tournament dates** directly from the text, handling formats like `dd. mm. yyyy` and `dd. <month_name> yyyy`.
    * For new photo albums, it identifies the first image to use as a preview.
4.  **Generate `data.json`:** The script updates `data.json`, which serves as a central database for all dynamic content on the site.
5.  **Dynamic Frontend:** JavaScript on the live website fetches this `data.json` file and dynamically generates the HTML to display the latest tournaments and photo galleries.

---

## 📂 Project Structure

-   `index.html` – Home page
-   `components/` – Reusable header, footer, sponsors, sidebar...
-   `assets/` – Images, CSS, JS, and content files.
    -   `js/`
        -   `include.js` - Handles the inclusion of reusable `components/`.
        -   `index-turnaje.js` - Manages the collapsible tournament lists on the index page.
        -   `pagination.js` - Controls the pagination for lists.
    -   `css/` - General styling.
-   `.github/workflows/` - Contains the YAML file for the GitHub Actions automation.
-   `scripts/` - Contains the Python script for generating the JSON.
-   `data.json` - The auto-generated database of website content.

---

## <iframe> Third-Party Integrations

The website uses iframes for two sections in the sidebar:
-   **"Nejbližší akce" (Upcoming Events):** An embedded Google Calendar. Events need to be added there.
-   **"Oddíly" (Clubs):** An embedded Mapy.cz map showing the locations of club halls. This should be checked and updated at least once a year.

---

## 📝 Progress Commentary & To-Do

-   **index:** Structure is done, links need to be added.
-   **turnaje (tournaments):** Pagination is working. The structure needs to be fully implemented to dynamically load from `data.json`. Links are missing.
-   **soutěže (leagues):** Currently just a link to stis.cz. Some improvements may be needed.
-   **foto (photos):** Page is missing. Needs to be implemented to load albums from `data.json`.
-   **zpravodaje (newsletters):** The main idea with pagination is done, links are missing.
-   **svaz (association):** No relevant data yet.

### Automation & Future Plans:
-   **`[IMPLEMENTED]`** **Automatic JSON Generation:** Pushing a document to the repository now generates a `json` file. Info from this JSON is ready to be printed on the "turnaje" page and possibly an "updates" section.
-   **`[TO-DO]`** **Auto-creating Google Calendar events:** The next step is to create a script (e.g., Google Apps Script) that reads `data.json` and automatically creates events in the embedded Google Calendar.

---

## 🐛 Unfixed Errors & Documentation

-   **Unfixed errors:** The header (due to the photo background) and footer have slight visual inconsistencies between the `index.html` and other pages that need to be unified.
-   **Documentation:** Missing/not good. Needs to be improved.

More soon ;)
