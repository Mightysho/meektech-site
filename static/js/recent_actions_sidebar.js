document.addEventListener('click', function (e) {
    var toggle = e.target.closest('[data-toggle="recent-actions"]');
    if (toggle) {
        e.preventDefault();
        var li = toggle.closest('.nav-item-recent-actions');
        var submenu = li.querySelector('.recent-actions-dropdown');
        if (!submenu) return;
        var expanded = submenu.classList.toggle('open');
        submenu.setAttribute('aria-hidden', expanded ? 'false' : 'true');
        toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    } else {
        // click outside closes the dropdown
        var open = document.querySelectorAll('.recent-actions-dropdown.open');
        open.forEach(function (el) {
            if (!el.contains(e.target)) {
                el.classList.remove('open');
                el.setAttribute('aria-hidden', 'true');
                var parentToggle = el.closest('.nav-item-recent-actions').querySelector('[data-toggle="recent-actions"]');
                if (parentToggle) parentToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
});
