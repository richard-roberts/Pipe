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
    },

    queryNode: function(id, callback) {
        var data = {
            id: id
        }
        pipe.make_request("query_node", data, function(response) {
            var node = JSON.parse(response);
            callback(node);
        });
    },

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

    assignArgument: function(id, name, value, callback) {
        var data = {
            id: id,
            name: name,
            value: value
        };
        pipe.make_request("assign_argument", data, function(response) {
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

    deleteEdge: function(edgeId, callback) {
        var parts = edgeId.split(".");
        if (parts.length != 4) {
            console.error(`${edgeId} is not a valid edge identifier`);
            return;
        }
        var data = {
            node_id_from: parts[0],
            arg_from: parts[1],
            node_id_to: parts[2],
            arg_to: parts[3]
        }
        pipe.make_request("delete_edge", data, function(response) {
            var success = JSON.parse(response);
            callback(success);
        });
    },

    deleteNode: function(id, callback) {
        var data = {
            id: id
        }
        pipe.make_request("delete_node", data, function(response) {
            var success = JSON.parse(response);
            callback(success);
        });
    },

    execute: function(id, callback) {
        var data = {
            id: id
        }
        pipe.make_request("execute", data, function(response) {
            if (response == "false") {
                console.error("execution failed");
                return;
            }
            
            var nodeData = JSON.parse(response);
            callback(nodeData);
        });
    },

    listNodes: function(callback) {
        pipe.make_request("list_nodes", {}, function(response) {
            var nodeData = JSON.parse(response);
            callback(nodeData);
        });
    },

    listEdges: function(callback) {
        pipe.make_request("list_edges", {}, function(response) {
            var edgeData = JSON.parse(response);
            callback(edgeData);
        });
    },

    asJson: function(callback) {
        pipe.make_request("as_json", {}, function(response) {
            var json = response;
            callback(json);
        });
    },

    fromJson: function(jsonString, callback) {
        var data = {
            data: jsonString
        } 
        pipe.make_request("from_json", data, function(response) {
            var success = response;
            callback(success);
        });
    }
    
}
