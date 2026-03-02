document.addEventListener('DOMContentLoaded', function () {
    var widget = document.querySelector('.spectra-widget.recent-actions-widget');
    if (widget) {
        // add loaded class to trigger CSS animation
        setTimeout(function () { widget.classList.add('loaded'); }, 80);
    }
});
