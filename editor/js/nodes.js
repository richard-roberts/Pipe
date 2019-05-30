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
        svg.setStyle(background, `fill:${config.node.body};stroke:${config.node.bordercolor};stroke-width:${config.node.borderwidth};border-style:inset;}`);
        svg.setEvent(background, "mousedown", function(e) {
            editor.addSelected(group);
        });

        // Title
        var text = svg.newCenteringText(w / 2, nodes.label * 0.6, 25, name, parent=group);
        svg.setStyle(text, `fill:${config.node.text};`)
            
        // Variables
        variables.createArgsFromData(group, templateData.args, variables.spacing, nodes.label);
        variables.createOutsFromData(group, templateData.outs, w - variables.w - variables.spacing, nodes.label);
    }

}