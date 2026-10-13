/* England Analytics — site.js
   Three small jobs: the mobile menu, the inquiry form's follow-up questions,
   and reading ?interest= / ?product= from the URL so a visitor lands on a
   form that already knows what they clicked. No dependencies. */

(function () {
  "use strict";

  /* --- Mobile menu ------------------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  /* --- Current year in footer -------------------------------------------- */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  /* --- Dashboard theme preview ------------------------------------------ */
  document.querySelectorAll("[data-theme-gallery]").forEach(function (gallery) {
    var preview = gallery.querySelector("[data-theme-preview]");
    var status = gallery.querySelector("[data-theme-status]");
    var options = gallery.querySelectorAll("[data-theme-option]");

    options.forEach(function (option) {
      option.addEventListener("click", function () {
        var theme = option.dataset.themeName;
        preview.src = option.dataset.themeSrc;
        preview.alt = "KPI Snapshot dashboard in " + theme + " theme";
        options.forEach(function (otherOption) {
          otherOption.setAttribute("aria-pressed", otherOption === option ? "true" : "false");
        });
        status.textContent = "Previewing " + theme + ".";
      });
    });
  });

  /* --- Inquiry form ------------------------------------------------------ */
  var form = document.getElementById("inquiry-form");
  if (!form) return;

  var radios = form.querySelectorAll('input[name="interest"]');
  var branches = form.querySelectorAll(".branch");

  function showBranch(value) {
    branches.forEach(function (b) {
      var match = b.dataset.branch === value;
      b.hidden = !match;
      // Only require fields inside the visible branch.
      b.querySelectorAll("[data-required]").forEach(function (f) {
        if (match) { f.setAttribute("required", ""); } else { f.removeAttribute("required"); }
      });
    });
  }

  radios.forEach(function (r) {
    r.addEventListener("change", function () { showBranch(r.value); });
  });

  var params = new URLSearchParams(window.location.search);
  var interest = params.get("interest");
  var product = params.get("product");

  if (interest) {
    var picked = form.querySelector('input[name="interest"][value="' + CSS.escape(interest) + '"]');
    if (picked) picked.checked = true;
  }

  var checked = form.querySelector('input[name="interest"]:checked');
  showBranch(checked ? checked.value : null);

  if (product) {
    var select = form.querySelector('select[name="dashboard"]');
    if (select) {
      var found = Array.prototype.some.call(select.options, function (o) { return o.value === product; });
      if (found) select.value = product;
    }
  }
})();
