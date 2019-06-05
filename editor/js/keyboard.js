var keyboard = {

    press: function(e) {
        editor.handleKeyPress(e.key);
    },

    setup: function() {
        $(document).keydown(keyboard.press);
    }
}

