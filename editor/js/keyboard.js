var keyboard = {

    press: function(e) {
        editor.handleKeyPress(e.key);
    },

    setup: function() {
        window.onkeypress = keyboard.press;
    }
}

