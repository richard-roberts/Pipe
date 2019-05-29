var nodes = {
    
    label: 50,
    innerW: 100,

    createFromData: function(templateData, nodeData) {
        // Calculate metadata
        var name = nodeData.path;
        var w = variables.w * 2 + variables.spacing * 2 + nodes.innerW;
        var h = nodes.label + Math.max(
            variables.measureHeight(templateData.args),
            variables.measureHeight(templateData.outs)
        );

        // Group
        var group = svg.newGroup(nodeData.x, nodeData.y, parent=null, id=nodeData.id);

        // Background
        var background = svg.newRect(0, 0, w, h, parent=group);
        svg.setAttr(background, "rx", "15");
        svg.setStyle(background, "fill:red");
        svg.setAttr(group, "selected", false);

        svg.setEvent(background, "click", function(e) {
            var selected = svg.getAttr(group, "selected");
            if (selected == "true") {
                svg.setAttr(group, "selected", false);
            } else {
                svg.setAttr(group, "selected", true);
            }
        })

        svg.setEvent(background, "mousemove", function(e) {
            var t = svg.getTranslateXY(group);
            var selected = svg.getAttr(group, "selected");
            if (selected == "true") {
                svg.setAttr(
                    group,
                    "transform", 
                    `translate(${t.x + e.movementX}, ${t.y + e.movementY})`
                );
            }
        })

        // Title
        var text = svg.newCenteringText(w / 2, nodes.label * 0.6, 25, name, parent=group);
            
        // Variables
        variables.createArgsFromData(group, templateData.args, variables.spacing, nodes.label);
        variables.createOutsFromData(group, templateData.outs, w - variables.w - variables.spacing, nodes.label);
    }

}