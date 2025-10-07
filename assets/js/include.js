async function loadComponent(id, file) {
  const el = document.getElementById(id);
  const response = await fetch(file);
  const html = await response.text();
  el.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  loadComponent("header-placeholder", "/ostravskypinec/components/header.html");
  loadComponent("footer-placeholder", "/ostravskypinec/components/footer.html");
  loadComponent("sponsors-placeholder", "/ostravskypinec/components/sponsors.html");
  loadComponent("sidebar-placeholder", "/ostravskypinec/components/sidebar.html");
});