var edges = {

    records: [],

    reset: function() {
        edges.records = [];
    },

    updateEdge: function(record) {
        var datum = record.datum;
        var curve = record.curve;

        var nodeXY;
        var connectorXY;
        nodeXY = svg.getTranslateXY(svg.getById(`${datum.node_id_from}`));
        connectorXY = svg.getCxCy(svg.getById(`${datum.node_id_from}.${datum.arg_from}`));
        var a = {
            x: nodeXY.x + connectorXY.x + 8,
            y: nodeXY.y + connectorXY.y,
        }

        var nodeXY;
        var connectorXY;
        nodeXY = svg.getTranslateXY(svg.getById(`${datum.node_id_to}`));
        connectorXY = svg.getCxCy(svg.getById(`${datum.node_id_to}.${datum.arg_to}`));
        var b = {
            x: nodeXY.x + connectorXY.x - 8,
            y: nodeXY.y + connectorXY.y,
        }

        svg.setCurveCoordinates(
            curve,
            a.x, a.y,
            b.x, a.y,
            a.x, b.y,
            b.x, b.y
        );
    },

    updateAll: function() {
        edges.records.forEach(record => {
            edges.updateEdge(record);
        });
    },

    createFromData: function(datum) {
        var curve = svg.newCurve(
            parent=null,
            id=`${datum.node_id_from}.${datum.arg_from}.${datum.node_id_to}.${datum.arg_to}`
        );
        svg.setAttr(curve, "stroke", `${config.edge.color}`);
        svg.setAttr(curve, "stroke-width", `${config.edge.width}`);
        svg.setAttr(curve, "fill", "transparent");
        var record = {
            datum: datum,
            curve: curve
        };
        edges.updateEdge(record);
        edges.records.push(record);

        editProperties.setMouseOverFunction(curve, function(e) {  
            editor.lastHovered = curve.id;
            editor.lastHoveredType = 'edge';
        });
    }

}