var variables = {

    w: 100,
    h: 25,
    r: 5,
    spacing: 10,

    measureHeight(vars) {
        return variables.h * vars.length + variables.spacing * (vars.length + 1);
    },

    createArgFromData: function(parent, data, x, y) {
        var connector = svg.newCircle(
            x + variables.w * 0.125, 
            y + variables.h / 2,
            variables.r,
            parent=parent
        );
        var connectorInner = svg.newCircle(
            x + variables.w * 0.125, 
            y + variables.h / 2,
            variables.r * 0.5,
            parent=parent
        );
        svg.setStyle(connector, `fill:${config.variable.connector};`);
        svg.setStyle(connectorInner, `fill:${config.node.body};`);
        
        var text = svg.newLeftAlignedText(
            x + variables.w * 0.3,
            y + variables.h / 2, 
            20,
            data.name, 
            parent=parent
        );
        svg.setStyle(text, `fill:${config.variable.text};`);
    },

    createOutFromData: function(parent, data, x, y) {
        var connector = svg.newCircle(
            x + variables.w * 0.875, 
            y + variables.h / 2,
            variables.r,
            parent=parent
        )
        var connectorInner = svg.newCircle(
            x + variables.w * 0.875, 
            y + variables.h / 2,
            variables.r * 0.5,
            parent=parent
        );
        svg.setStyle(connector, `fill:${config.variable.connector};`);
        svg.setStyle(connectorInner, `fill:${config.node.body};`);
        
        var text = svg.newRightAlignedText(
            x + variables.w * 0.7,
            y + variables.h / 2, 
            20,
            data.name, 
            parent=parent
        );
        svg.setStyle(text, `fill:${config.variable.text};`);
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