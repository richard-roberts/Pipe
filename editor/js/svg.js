var svg = {
    
    type: "http://www.w3.org/2000/svg",
    w: window.innerWidth,
    h: window.innerHeight * 0.8,
    x: -window.innerWidth / 2,
    y: -(window.innerHeight * 0.8) / 2,

    body: null,

    getAttr: function (element, attr) {
        return element.getAttributeNS(null, attr);
    },
    
    setAttr: function (element, attr, value) {
        element.setAttributeNS(null, attr, value);
    },

    setStyle: function(element, style) {
        svg.setAttr(element, "style", style);
    },

    setEvent: function(element, eventType, callback) {
        element.addEventListener(eventType, callback);
    },

    getTranslateXY: function(element) {
        var str = svg.getAttr(element, "transform");
        str = str.split("(")[1];
        str = str.split(")")[0];
        var parts = str.split(",");
        var x = parseInt(parts[0].replace( /^\s+|\s+$/g, ''), 10);
        var y = parseInt(parts[1].replace( /^\s+|\s+$/g, ''), 10); 
        return {x: x, y: y};
    },
    
    setTranslateXY: function(element, x, y) {
        svg.setAttr(element, "transform", `translate(${x},${y})`);
    },

    updateView: function () {
        svg.setAttr(svg.body, "viewBox", `${svg.x} ${svg.y} ${svg.w} ${svg.h}`);
    },

    newElement: function (parent, elementType, id=null) {
        var e = document.createElementNS(svg.type, elementType);
        if (id != null) {
            e.id = id;
        }
        if (parent != null) {
            parent.appendChild(e);
        } else {
            svg.body.appendChild(e);
        }
        return e;
    },
    
    newGroup: function (x, y, parent=null, id=null) {
        var e = svg.newElement(parent, 'svg', id=id);
        svg.setTranslateXY(e, x, y);
        return e;
    },

    newRect: function (x, y, w, h, parent=null, id=null) {
        var e = svg.newElement(parent, 'rect', id=id);
        svg.setAttr(e, "x", x);
        svg.setAttr(e, "y", y);
        svg.setAttr(e, "width", w);
        svg.setAttr(e, "height", h);
        return e;
    },

    newCircle: function(x, y, r, parent=null, id=null) {
        var e = svg.newElement(parent, 'circle', id=id);
        svg.setAttr(e, "cx", x);
        svg.setAttr(e, "cy", y);
        svg.setAttr(e, "r", r);
        return e;
    },

    newCenteringText: function (x, y, size, text, parent=null, id=null) {
        var e = svg.newElement(parent, 'text', id=id);
        e.appendChild(document.createTextNode(text));
        svg.setAttr(e, "font-size", size);
        svg.setAttr(e, "x", x - e.getBBox().width / 2);
        svg.setAttr(e, "y", y + e.getBBox().height / 4);
        return e;
    },

    newLeftAlignedText: function (x, y, size, text, parent=null, id=null) {
        var e = svg.newElement(parent, 'text', id=id);
        e.appendChild(document.createTextNode(text));
        svg.setAttr(e, "font-size", size);
        svg.setAttr(e, "x", x);
        svg.setAttr(e, "y", y + e.getBBox().height / 4);
        return e;
    },

    newRightAlignedText: function (x, y, size, text, parent=null, id=null) {
        var e = svg.newElement(parent, 'text', id=id);
        e.appendChild(document.createTextNode(text));
        svg.setAttr(e, "font-size", size);
        svg.setAttr(e, "x", x + e.getBBox().width);
        svg.setAttr(e, "y", y + e.getBBox().height / 4);
        return e;
    },

    setup: function() {
        svg.body = document.getElementById("editor-body");
        svg.updateView();
    },
}
