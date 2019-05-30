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
        svg.setAttr(background, "style", `fill:${config.background};`);

        function grid() {
            var w = 20000;
            var h = 20000;
            var thickness = 0.5;
            var spacing = 100;
            var n = 51;

            // Horizontal
            var y = -(spacing * (n + 1) + thickness * n) / 2;
            for (var i = 0; i < n; i++) {
                y += thickness + spacing;
                var hori = svg.newRect(-w / 2, y, w, thickness, parent=svg.body);
                svg.setAttr(hori, "style", `fill:${config.highlight};opacity:0.5;`);
            }

            // Vwrtical
            var x = -(spacing * (n + 1) + thickness * n) / 2;
            for (var i = 0; i < n; i++) {
                x += thickness + spacing;
                var hori = svg.newRect(x, -h / 2, thickness, h, parent=svg.body);
                svg.setAttr(hori, "style", `fill:${config.highlight};opacity:0.5;`);
            }
            
            var centerHori = svg.newRect(-w / 2, -thickness, w, thickness * 2, parent=svg.body);
            var centerVert = svg.newRect(-thickness, -h / 2, thickness * 2, h, parent=svg.body);
            svg.setAttr(centerHori, "style", `fill:${config.highlight};opacity:0.5`);
            svg.setAttr(centerVert, "style", `fill:${config.highlight};opacity:0.5`);
        }
        grid();

        
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