var svg = {
    
    type: "http://www.w3.org/2000/svg",
    w: 1600,
    h: 900,
    x: -800,
    y: -450,

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
        var e = svg.newElement(parent, 'g', id=id);
        svg.setAttr(e, "x", x);
        svg.setAttr(e, "y", y);
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

    newText: function (x, y, text, parent=null, id=null) {
        var e = svg.newElement(parent, 'text', id=id);
        e.appendChild(document.createTextNode(text));
        svg.setAttr(e, "x", x - e.getBBox().width / 2);
        svg.setAttr(e, "y", y + e.getBBox().height / 4);
        return e;
    },

    setup: function() {
        svg.body = document.getElementById("editor-body");
        svg.updateView();
    },
}
