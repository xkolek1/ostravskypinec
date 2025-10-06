async function loadComponent(id, file) {
  const el = document.getElementById(id);
  const response = await fetch(file);
  const html = await response.text();
  el.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  loadComponent("header-placeholder", "/components/header.html");
  loadComponent("footer-placeholder", "/components/footer.html");
  loadComponent("sponsors-placeholder", "/components/sponsors.html");
  loadComponent("sidebar-placeholder", "/components/sidebar.html");
});