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
        
        svg.newLeftAlignedText(
            x + variables.w * 0.2,
            y + variables.h / 2, 
            20,
            data.name, 
            parent=parent
        );
    },

    createOutFromData: function(parent, data, x, y) {
        var background = svg.newCircle(
            x + variables.w * 0.875, 
            y + variables.h / 2,
            variables.r,
            parent=parent
        )
        svg.setStyle(background, "fill:blue;");
        
        svg.newRightAlignedText(
            x + variables.w * 0.8,
            y + variables.h / 2, 
            20,
            data.name, 
            parent=parent
        );
    },

    createArgsFromData: function(parent, data, x, y) {
        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createArgFromData(parent, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },
    
    createOutsFromData: function(parent, data, x, y) {
        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createOutFromData(parent, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },

}