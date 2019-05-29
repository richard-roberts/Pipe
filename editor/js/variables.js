var variables = {

    w: 100,
    h: 25,
    r: 5,
    spacing: 10,

    measureHeight(vars) {
        return variables.h * vars.length + variables.spacing * (vars.length + 1);
    },

    createArgFromData: function(parent, data, x, y) {
        var background = svg.newCircle(
            x + variables.w * 0.125, 
            y + variables.h / 2,
            variables.r,
            parent=parent
        )
        svg.setStyle(background, "fill:blue;");
        svg.newLeftAlignedText(x + variables.w / 4, y + variables.h / 2, 20, data.name);
    },

    createOutFromData: function(parent, data, x, y) {
        var background = svg.newCircle(
            x + variables.w * 0.875, 
            y + variables.h / 2,
            variables.r,
            parent=parent
        )
        svg.setStyle(background, "fill:blue;");
        svg.newRightAlignedText(x - variables.w * 0.4, y + variables.h / 2, 20, data.name);
    },

    createArgsFromData: function(parent, data, x, y) {
        var group = svg.newGroup(x, y, parent=parent, id=data.id);

        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createArgFromData(group, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },
    
    createOutsFromData: function(parent, data, x, y) {
        var group = svg.newGroup(x, y, parent=parent, id=data.id);

        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createOutFromData(group, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },

}