var nodes = {

    w: 160,
    h: 90,
    
    createFromData: function(templateData, nodeData) {
        var group = svg.newGroup(nodeData.x, nodeData.y, parent=null, id=nodeData.id);
        var background = svg.newRect(0, 0, nodes.w, nodes.h, parent=group);
        svg.setStyle(background, "fill:red");
    }

}