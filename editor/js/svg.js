var svg = {
    
    type: "http://www.w3.org/2000/svg",
    ow: window.innerWidth,
    oh: window.innerHeight,
    w: window.innerWidth,
    h: window.innerHeight,
    x: -window.innerWidth / 2,
    y: -(window.innerHeight) / 2,
    scale: 1.0,

    body: null,

    clear: function(element) {
        editChildren.clear(element);
    },

    getById: function(id) {
        return document.getElementById(id);
    },

    getAttr: function (element, attr) {
        return element.getAttributeNS(null, attr);
    },

    getCxCy: function(element) {
        var bbox = element.getBBox();
        var x = bbox.x + (bbox.width / 2);
        var y = bbox.y + (bbox.height / 2);
        return {
            x: x,
            y: y
        };
    },

    getMouseXY: function(e) {
        return {
            x: e.clientX * svg.scale + svg.x,
            y: e.clientY * svg.scale + svg.y
        }
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
        var sx = x * svg.scale;
        var sy = y * svg.scale;
        svg.setAttr(element, "transform", `translate(${sx},${sy})`);
    },
    
    moveXY: function(element, x, y) {
        var xy = svg.getTranslateXY(element);
        var sx = xy.x + x * svg.scale;
        var sy = xy.y + y * svg.scale;
        svg.setAttr(element, "transform", `translate(${sx},${sy})`);
    },

    resetView: function(x, y) {
        svg.ow = window.innerWidth;
        svg.oh = window.innerHeight;
        svg.w = window.innerWidth;
        svg.h = window.innerHeight;
        svg.x = -window.innerWidth / 2;
        svg.y = -(window.innerHeight) / 2;
        svg.scale = 1.0;
        svg.updateView();
    },

    shiftView: function(x, y) {
        svg.x -= x * svg.scale;
        svg.y -= y * svg.scale;
        svg.updateView();
    },

    zoomView: function(delta) {
        svg.scale += delta * 0.0001;
        var offsetX = svg.x + svg.w / 2;
        var offsetY = svg.y + svg.h / 2;
        svg.w = svg.ow * svg.scale;
        svg.h = svg.oh * svg.scale;
        svg.x = -svg.w / 2 + offsetX;
        svg.y = -svg.h / 2 + offsetY;
        svg.updateView();
    },

    updateView: function () {
        svg.setAttr(svg.body, "viewBox", `${svg.x} ${svg.y} ${svg.w} ${svg.h}`);
    },

    removeElement: function(parent, element) {
        parent.removeChild(element);
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
        svg.setAttr(e, "x", x - e.getBBox().width);
        svg.setAttr(e, "y", y + e.getBBox().height / 4);
        return e;
    },

    newCurve: function(parent=null, id=null) {
        var e = svg.newElement(parent, 'path', id=id);
        return e;
    },

    setCurveCoordinates: function(e, x1, y1, x2, y2, x3, y3, x4, y4) {
        // See https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
        svg.setAttr(e, "d", `M ${x1} ${y1} C ${x2} ${y2}, ${x3} ${y3}, ${x4} ${y4}`);
    },

    setup: function() {
        svg.body = document.getElementById("editor-body");
        svg.updateView();
    },
}
