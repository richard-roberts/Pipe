var editor = {

    selected: [],
    following: false,
    pendingConnectionOutput: null,
    pendingCurve: null,
    pendingConnectionNode: null,
    pendingConnectionOutputNodeId: null,
    pendingConnectionOutputName: null,
    lastHovered: null,
    lastHoveredType: null,

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

    addOrUpdateTemplate: function(path, args, outs, extension, code) {
        pipe.addOrUpdateTemplate(
            path, args, outs, extension, code,
            function(templateData) {
                statusbar.displayMessage(templateData)
            }
        );
    },

    newNode: function(path) {
        pipe.query_template(path, function(templateData) {
            pipe.new_node(path, 0, 0, function(nodeData) {
                nodes.createFromData(templateData, nodeData);
            });
        });
    },

    assignArgument: function() {
        if (editor.lastHoveredType == 'arg') {
            var parts = editor.lastHovered.split(".");
            var id = parts[0];
            var name = parts[1];
            
            pipe.queryNode(id, function(nodeData) {
                var previousValue = "";
                if (name in nodeData.args) {
                    previousValue = nodeData.args[name];
                }
                var value = prompt(`Enter value for ${name}:`,  previousValue); 
                if (value != null) { 
                    pipe.assignArgument(id, name, value, function(success) {
                        if (success) {
                            if (value == "") {
                                svg.setStyle(svg.getById(editor.lastHovered), `fill:${config.variable.connectorUnassigned};`);
                            } else {
                                svg.setStyle(svg.getById(editor.lastHovered), `fill:${config.variable.connectorAssigned};`);
                            }
                        }
                    });
                }       
            });
        } else {
            statusbar.displayError(`You can only assign to arguments.`);
        }  
    },

    deleteLastHovered: function() {
        if (editor.lastHovered == null) {
            statusbar.displayError("Nothing selected to delete (hover over it)");
            return;
        }

        if (editor.lastHoveredType == 'edge') {
            pipe.deleteEdge(editor.lastHovered, function(success) {
                if (success) {
                    svg.removeElement(svg.body, svg.getById(editor.lastHovered));
                    editor.lastHovered = null;
                } else {
                    statusbar.displayError(`Failed to delete edge (id=${editor.lastHovered})`);
                }
            });
        }
        if (editor.lastHoveredType == 'node') {
            pipe.deleteNode(editor.lastHovered, function(success) {
                if (success) {
                    // TODO: remove just the node in questions and any connected edges
                    editor.refresh(); 
                    editor.lastHovered = null;
                } else {
                    statusbar.displayError(`Failed to delete node (id=${editor.lastHovered})`);
                }
            })
        }
    },

    evaluate: function() {
        if (editor.lastHoveredType != 'node') {
            statusbar.displayError(`You can only evalaute nodes.`);
            return;
        }

        var nodeid = editor.lastHovered;

        pipe.execute(nodeid, function(nodeData) {
            statusbar.displayMessage("Execution successful");
            Object.keys(nodeData.outs).forEach(key => {
                var name = key;
                var value = nodeData.outs[key];
                if (value == "") {
                    svg.setStyle(svg.getById(`${nodeid}.${name}`), `fill:${config.variable.connectorUnassigned};`);
                } else {
                    svg.setStyle(svg.getById(`${nodeid}.${name}`), `fill:${config.variable.connectorAssigned};`);
                }
            });
        });

    },

    editNodeTemplate: function() {
        if (editor.lastHoveredType != "node") {
            statusbar.displayWarning("hover over a node to edit it's template");
            return;
        }

        var id = editor.lastHovered;
        pipe.queryNode(id, function(nodeData) {
            menu.editTemplate(nodeData.path);
        });

    },

    showTooltip: function()  {
        function showVariable() {
            var parts = editor.lastHovered.split(".");
            var id = parts[0];
            var name = parts[1];
            pipe.queryNode(id, function(nodeData) {
                var key = `${editor.lastHoveredType}s`;
                var varMap = nodeData[key];
                if (name in varMap) {
                    var message = `${name}=${varMap[name]}`;
                    tooltip.show(message);
                } else {
                    statusbar.displayError(`${name} not found in node data (id=${nodeData.id}).`);
                }
            });
        }

        switch(editor.lastHoveredType) {
            case 'arg': showVariable(); break;
            case 'out': showVariable(); break;
            default: statusbar.displayWarning("hover over something to display value");
        }
    },

    handleMouseDown: function(e) {
        editor.following = true;
    },

    handleMouseUp: function(e) {
        editor.following = false;
        
        if (editor.pendingCurve != null) {
            editor.stopDrawingPendingCurve(e);
        }
        editor.selected.forEach(node => {
            editor.sendNodePositionUpdate(node);
        });
        editor.selected = [];
    },

    handleMouseMove: function(e) {
        if (editor.pendingConnectionOutput != null) {
            editor.drawPendingCurveEndAtMouse(e);    
            return;
        }

        if (editor.selected.length == 0) {
            if (editor.following) {
                svg.shiftView(e.movementX, e.movementY);
            }
        } else {
            editor.selected.forEach(node => {
                svg.moveXY(node, e.movementX, e.movementY);
            });
            edges.updateAll();
        }
    },

    handleMouseWheel: function(e) {
        e.preventDefault();
        svg.zoomView(e.deltaY);
    },

    handleKeyPress: function(key) {

        if (document.activeElement == document.getElementsByTagName('body')[0]) {
            switch(key) {
                case '.': editor.refresh(); break;
                case 'm': menu.showMenu(); break;
                case 'e': editor.exportToFile(); break;
                case 's': editor.downloadFilepathViaArgument(); break;
                case 'n': menu.showMenu(); menu.newOrUpdateTemplateMenu(); break;
                case 'p': menu.showMenu(); menu.newNodeMenu(); break;
                case 'u': menu.showMenu(); menu.uploadMenu(); break;
                case 'l': menu.showMenu(); menu.openLogger(); break;
                case 'a': editor.assignArgument(); break;
                case 'd': editor.deleteLastHovered(); break;
                case ' ': editor.showTooltip(); break;
                case 'x': editor.evaluate(); break;
                case 't': editor.editNodeTemplate(); break;
            }
        } 
        
        if (menu.open) {
            switch(key) {
                case 'Escape': menu.hideMenu(); break;
            }
            return;
        }

        switch(key) {
            case 'Escape': menu.toggleMenu(); break;
        }
    },

    refresh: function() {

        function renderGrid(nextFunctions) {
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
                svg.setAttr(hori, "style", `fill:${config.editor.highlight};opacity:0.5;`);
            }
    
            // Vertical
            var x = -(spacing * (n + 1) + thickness * n) / 2;
            for (var i = 0; i < n; i++) {
                x += thickness + spacing;
                var hori = svg.newRect(x, -h / 2, thickness, h, parent=svg.body);
                svg.setAttr(hori, "style", `fill:${config.editor.highlight};opacity:0.5;`);
            }
            
            var centerHori = svg.newRect(-w / 2, -thickness, w, thickness * 2, parent=svg.body);
            var centerVert = svg.newRect(-thickness, -h / 2, thickness * 2, h, parent=svg.body);
            svg.setAttr(centerHori, "style", `fill:${config.editor.highlight};opacity:0.5`);
            svg.setAttr(centerVert, "style", `fill:${config.editor.highlight};opacity:0.5`);
            nextFunctions.shift()(nextFunctions);
        }

        function renderNodes(nextFunctions) {
            pipe.listNodes(function(nodeData) {
                if (nodeData.length == 0) {
                    nextFunctions.shift()(nextFunctions);
                    return;
                }
                var nodesFinished = 0;
                nodeData.forEach(nodeDatum => {
                    pipe.query_template(nodeDatum.path, function(templateDatum) {
                        nodes.createFromData(templateDatum, nodeDatum);
                        nodesFinished ++;
    
                        if (nodesFinished == nodeData.length) {
                            nextFunctions.shift()(nextFunctions);
                        }
                    });
                });
            });
        }

        function renderEdges(nextFunctions) {   
            edges.reset();
            
            pipe.listEdges(function(edgeData) {
                if (edgeData.length == 0) {
                    nextFunctions.shift()(nextFunctions);
                    return;
                }
                var edgesFinished = 0;
                edgeData.forEach(edgeDatum => {
                    edges.createFromData(edgeDatum);
                    edgesFinished ++;

                    if (edgesFinished == edgeData.length) {
                        nextFunctions.shift()(nextFunctions);
                    }
                });
            });   
        }

        function setEvents(nextFunctions) {
            svg.setEvent(svg.body, "mousedown", editor.handleMouseDown);
            svg.setEvent(svg.body, "mouseup", editor.handleMouseUp);
            svg.setEvent(svg.body, "mousemove", editor.handleMouseMove);
            svg.setEvent(svg.body, "wheel", editor.handleMouseWheel);
            svg.setEvent(svg.body, "dragover", files.showLinkIconOnDrag);
            svg.setEvent(svg.body, "drop", editor.importFromFile);
            nextFunctions.shift()(nextFunctions);
        }

        function renderComplete() {
            statusbar.displayMessage("Graph render complete");
        }

        svg.clear(svg.body);
        svg.resetView();
        var actions = [renderGrid, renderNodes, renderEdges, setEvents, renderComplete];
        actions.shift()(actions);
    },

    sendNodePositionUpdate: function(node) {
        var pos = svg.getTranslateXY(node);
        pipe.setNodePosition(node.id, pos.x, pos.y, function(success) {
            if (success != true) {
                statusbar.displayError(`failed to move node (id=${node.id}) to (x=${pos.x} y=${pos.y})`);
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
        b.y -= 10;
        svg.setCurveCoordinates(
            editor.pendingCurve,
            a.x, a.y,
            b.x, a.y,
            a.x, b.y,
            b.x, b.y
        );
    },

    importFromFile: function(e) {
        files.loadDroppedFileCotentAsString(e, function(str) {
            pipe.fromJson(str, function(success) {
                if (success) {
                    editor.refresh();
                }
            });
        });
    },

    exportToFile: function() {
        pipe.asJson(function(json) {
            var name = prompt("Name:",  "graph"); 
            if (name != null) { 
                files.downloadContent(`${name}.json`, json);
            }
        });
    },

    downloadFilepathViaArgument: function() {
        if (editor.lastHoveredType != 'arg' && editor.lastHoveredType != 'out') {
            statusbar.displayWarning(`You can only download from "filepath" variables.`);
            return;
        }
        var parts = editor.lastHovered.split(".");
        var id = parts[0];
        var name = parts[1];
        if (name != "filepath") {
            statusbar.displayWarning(`You can only download from "filepath" variables.`);
            return;
        }
        
        pipe.queryNode(id, function(nodeData) {
            var key = `${editor.lastHoveredType}s`;
            if ("filepath" in nodeData[key]) {
                pipe.download(nodeData[key]["filepath"]);
            } else {
                statusbar.displayError(`filepath not found in node data (id=${nodeData.id})?`);
            }
        }); 
    },

    setup: function() {
        editor.refresh();
    }
    
}