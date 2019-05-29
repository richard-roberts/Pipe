var editor = {
    
    selected: [],

    deselectAll: function() {
        editor.selected = [];
    },

    addSelected: function(element) {
        editor.selected.push(element);
    },

    newNode: function(path) {
        pipe.query_template(path, function(templateData) {
            pipe.new_node(path, 0, 0, function(nodeData) {
                nodes.createFromData(templateData, nodeData);
            });
        });
    },

    setup: function() {
        
        var background = svg.newRect(-svg.w / 2, -svg.h / 2, svg.w, svg.h, parent=svg.body);
        svg.setAttr(background, "following", false);
        svg.setAttr(background, "style", "fill:#aaaaaa;");
        
        svg.setEvent(background, "mousedown", function(e) {
            svg.setAttr(background, "following", true);
        });

        svg.setEvent(svg.body, "mouseup", function(e) {
            svg.setAttr(background, "following", false);
            editor.deselectAll();
        });

        svg.setEvent(svg.body, "mousemove", function(e) {
            if (editor.selected.length == 0) {
                var following = svg.getAttr(background, "following");
                if (following == "true") {
                    svg.shiftView(e.movementX, e.movementY);
                }
            } else {
                editor.selected.forEach(o => {
                    svg.translateXY(o, e.movementX, e.movementY);
                });    
            }
        });

        svg.setEvent(svg.body, "wheel", function(e) {
            e.preventDefault();
            svg.zoomView(e.deltaY);
        });

    }
    
}