var editor = {
    
    selected: [],
    pendingConnectionOutput: null,
    pendingCurve: null,
    pendingConnectionNode: null,
    pendingConnectionOutputNodeId: null,
    pendingConnectionOutputName: null,

    addSelected: function(element) {
        editor.selected.push(element);
    },

    setOutputToBeConnected: function(element, nodeId, name) {
        editor.pendingConnectionOutput = element;
        editor.pendingConnectionNode = document.getElementById(nodeId);
        editor.pendingConnectionOutputNodeId = nodeId;
        editor.pendingConnectionOutputName = name;
        editor.startDrawingPendingCurve();
    },

    setInputToBeConnected: function(nodeId, name) {
        if (editor.pendingConnectionOutput != null) {
            pipe.newEdge(
                editor.pendingConnectionOutputNodeId,
                editor.pendingConnectionOutputName,
                nodeId,
                name,
                function(edgeDatum) {
                    edges.createFromData(edgeDatum);
                }
            );
        }

        if (editor.pendingCurve != null) {
            editor.stopDrawingPendingCurve();   
        }
    },

    newNode: function(path) {
        pipe.query_template(path, function(templateData) {
            pipe.new_node(path, 0, 0, function(nodeData) {
                nodes.createFromData(templateData, nodeData);
            });
        });
    },

    sendNodePositionUpdate: function(node) {
        var pos = svg.getTranslateXY(node);
        pipe.setNodePosition(node.id, pos.x, pos.y, function(success) {
            if (success != true) {
                console.error(`failed to move node (id=${node.id}) to (x=${pos.x} y=${pos.y})`);
            }
        })
    },

    startDrawingPendingCurve: function(e) {
        editor.pendingCurve = svg.newCurve();
        svg.setAttr(editor.pendingCurve, "stroke", `${config.edge.color}`);
        svg.setAttr(editor.pendingCurve, "stroke-width", `${config.edge.width}`);
        svg.setAttr(editor.pendingCurve, "fill", "transparent");
    },

    stopDrawingPendingCurve: function(e) {
        svg.removeElement(svg.body, editor.pendingCurve);
        editor.pendingCurve = null;
        editor.pendingConnectionOutput = null;
    },

    drawPendingCurveEndAtMouse: function(e) {
        var nodeXY = svg.getTranslateXY(editor.pendingConnectionNode);
        var connectorRelativeXY = svg.getCxCy(editor.pendingConnectionOutput);
        var connectorAbsoluteXY = {
            x: nodeXY.x + connectorRelativeXY.x,
            y: nodeXY.y + connectorRelativeXY.y,
        }
        var mouseXY = svg.getMouseXY(e);
        
        var a = connectorAbsoluteXY;
        var b = mouseXY;
        b.x -= 10;
        svg.setCurveCoordinates(
            editor.pendingCurve,
            a.x, a.y,
            b.x, a.y,
            a.x, b.y,
            b.x, b.y
        );
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
            if (editor.pendingCurve != null) {
                editor.stopDrawingPendingCurve(e);
            }
            editor.selected.forEach(node => {
                editor.sendNodePositionUpdate(node);
            });
            editor.selected = [];
        });

        svg.setEvent(svg.body, "mousemove", function(e) {

            if (editor.pendingConnectionOutput != null) {
                editor.drawPendingCurveEndAtMouse(e);    
                return;
            }

            if (editor.selected.length == 0) {
                var following = svg.getAttr(background, "following");
                if (following == "true") {
                    svg.shiftView(e.movementX, e.movementY);
                }
            } else {
                editor.selected.forEach(node => {
                    svg.moveXY(node, e.movementX, e.movementY);
                });
                edges.updateAll();
            }
        });

        svg.setEvent(svg.body, "wheel", function(e) {
            e.preventDefault();
            svg.zoomView(e.deltaY);
        });

    }
    
}