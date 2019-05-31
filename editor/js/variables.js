var variables = {

    w: 100,
    h: 25,
    r: 10,
    spacing: 10,

    measureHeight(vars) {
        return variables.h * vars.length + variables.spacing * (vars.length + 1);
    },

    createArgFromData: function(parent, node_id, data, x, y) {
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
            parent=parent,
            id=`${node_id}.${data.name}`
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

        var argCallback = function(e) {
            editor.setInputToBeConnected(node_id, data.name);
        }
        editProperties.setMouseUpFunction(connector, argCallback);
        editProperties.setMouseUpFunction(connectorInner, argCallback);
    },

    createOutFromData: function(parent, node_id, data, x, y) {
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
            parent=parent,
            id=`${node_id}.${data.name}`
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
        
        var outCallback = function(e) {
            editor.setOutputToBeConnected(connectorInner, node_id, data.name);
        }
        editProperties.setMouseDownFunction(connector, outCallback);
        editProperties.setMouseDownFunction(connectorInner, outCallback);
    },

    createArgsFromData: function(parent, node_id, data, x, y) {
        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createArgFromData(parent, node_id, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },
    
    createOutsFromData: function(parent, node_id, data, x, y) {
        var y = y + variables.spacing;
        data.forEach(datum => {
            variables.createOutFromData(parent, node_id, datum, x, y);
            y += variables.h + variables.spacing;
        });
    },

}