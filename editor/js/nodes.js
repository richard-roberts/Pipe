var nodes = {
    
    label: 50,
    innerW: 100,

    createFromData: function(templateData, nodeData) {
        // Calculate metadata
        var parts = nodeData.path.split(".")
        var name = parts[parts.length-1];
        var w = variables.w * 2 + variables.spacing * 2 + nodes.innerW;
        var h = nodes.label + Math.max(
            variables.measureHeight(templateData.args),
            variables.measureHeight(templateData.outs)
        );

        // Group
        var group = svg.newGroup(nodeData.x / svg.scale, nodeData.y / svg.scale, parent=null, id=nodeData.id);

        // Background
        var background = svg.newRect(0, 0, w, h, parent=group);
        svg.setAttr(background, "rx", "15");
        svg.setStyle(background, `fill:${config.node.body};stroke:${config.node.bordercolor};stroke-width:${config.node.borderwidth};border-style:inset;}`);
        svg.setEvent(background, "mousedown", function(e) {
            editor.addSelected(group);
        });
        editProperties.setMouseOverFunction(background, function() {
            editor.lastHovered = `${nodeData.id}`;
            editor.lastHoveredType = 'node';
        })

        // Title
        var text = svg.newCenteringText(w / 2, nodes.label * 0.6, 25, name, parent=group);
        svg.setStyle(text, `fill:${config.node.text};`)
            
        // Variables
        variables.createArgsFromData(group, nodeData.id, nodeData.args, templateData.args, variables.spacing, nodes.label);
        variables.createOutsFromData(group, nodeData.id, nodeData.outs, templateData.outs, w - variables.w - variables.spacing, nodes.label);
    }

}