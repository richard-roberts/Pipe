var url_base = 'http://127.0.0.1:5000';

var pipe = {

    make_request: function(command, data, callback) {
        var url = `${url_base}/${command}`;
        $.ajax({
            url: url, 
            type: 'GET', 
            crossDomain: true,
            data: data, 
            success: callback
        });
    },

    list_templates: function(callback) {
        pipe.make_request("list_templates", {}, function(response) {
            var templates = JSON.parse(response);
            callback(templates);
        });
    },

    query_template: function(path, callback) {
        var data = {
            path: path
        };
        pipe.make_request("query_template", data, function(response) {
            var template = JSON.parse(response);
            callback(template);
        });
    },

    new_node: function(path, x, y, callback) {
        var data = {
            path: path,
            x: x,
            y: y
        }
        pipe.make_request("new_node", data, function(response) {
            var node = JSON.parse(response);
            callback(node);
        });
    setNodePosition: function(id, x, y, callback) {
        var data = {
            id: id,
            x: x,
            y: y
        }
        pipe.make_request("set_node_position", data, function(response) {
            var success = JSON.parse(response);
            callback(success);
        });
    },

    newEdge: function(nodeIdFrom, argFrom, nodeIdTo, argTo, callback) {
        var data = {
            id_from: nodeIdFrom,
            arg_from: argFrom,
            id_to: nodeIdTo,
            node_to: argTo
        }
        pipe.make_request("new_edge", data, function(response) {
            var edgeDatum = JSON.parse(response);
            callback(edgeDatum);
        });
    },

    }
    
}
