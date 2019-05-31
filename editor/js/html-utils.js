
var makeHtml = {

    div: function() {
        var e = document.createElement('div');
        return e;
    },

    ul: function() {
        var e = document.createElement('ul');
        return e;
    },

    li: function() {
        var e = document.createElement('li');
        return e;
    },

    button: function() {
        var e = document.createElement('button');
        return e;
    }
    
}

var editProperties = {

    setClass: function(e, className) {
        e.className = className;
    },

    setClickFunction: function(e, callback) {
        e.onclick = callback;
    },

    setMouseDownFunction: function(e, callback) {
        e.onmousedown = callback;
    },

    setMouseUpFunction: function(e, callback) {
        e.onmouseup = callback;
    },

    setMouseMoveFunction: function(e, callback) {
        e.onmousemove = callback;
    },

    setMouseOverFunction: function(e, callback) {
        e.onmouseover = callback;
    },

    setMouseOutFunction: function(e, callback) {
        e.onmouseout = callback;
    }
}

var editChildren = {

    clear: function(e) {
        // See: https://stackoverflow.com/questions/3955229/remove-all-child-elements-of-a-dom-node-in-javascript
        while (e.firstChild) {
            e.removeChild(e.firstChild);
        }
    },

    append: function(e, toAppend) {
        e.appendChild(toAppend);
    }
}

var editInner = {
    
    set: function(e, content) {
        e.innerHTML = content;
    }

}
