var tooltip = {

    body: null,

    show: function(message) {
        tooltip.body.style.display = 'block';
        editInner.set(tooltip.body, message);
    },

    hide: function() {
        tooltip.body.style.display = 'none';
    },

    moveToMouse(e) {
        tooltip.body.style.left = e.clientX;
        tooltip.body.style.top = e.clientY;
        tooltip.body.style.display = 'none';
    },

    setup: function() {
        tooltip.body = document.getElementById('tooltip');
        window.addEventListener('mousemove', tooltip.moveToMouse);
    }
}