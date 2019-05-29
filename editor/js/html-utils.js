
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
    
}

var editProperties = {

    setClass: function(e, className) {
        e.className = className;
    },

    setClickFunction: function(e, callback) {
        e.onclick = callback;
    }
}

var editChildren = {

    append: function(e, toAppend) {
        e.appendChild(toAppend);
    }
}

var editInner = {
    
    set: function(e, content) {
        e.innerHTML = content;
    }

}
