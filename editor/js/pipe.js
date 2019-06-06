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

    make_xhr_post_request: function(command, form, callback) {
        var url = `${url_base}/${command}`
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                callback(xhr.response);
            }
        }
        xhr.open('POST', url, true);
        xhr.send(formData);
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

    newTemplate: function(path, args, outs, extension, code, callback) {
        var data = {
            path: path,
            args: args,
            outs: outs,
            extension: extension,
            code: code
        }
        pipe.make_request("new_basic_template", data, function(response) {
            var templateData = JSON.parse(response);
            callback(templateData);
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
            statusbar.displayError(`${edgeId} is not a valid edge identifier`);
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
                statusbar.displayError("execution failed");
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
    },

    upload: function(form, callback) {
        pipe.make_xhr_post_request("upload", form, callback);
    },

    // `download` by user iXs
    // See https://stackoverflow.com/questions/17527713/force-browser-to-download-image-files-on-click
    download: function(filepath) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", `${url_base}/download?filepath=${filepath}`, true);
        xhr.responseType = "blob";
        xhr.onload = function(){
            var urlCreator = window.URL || window.webkitURL;
            var imageUrl = urlCreator.createObjectURL(this.response);
            var tag = document.createElement('a');
            tag.href = imageUrl;
            tag.download = filepath.split("/").slice(-1)[0];
            document.body.appendChild(tag);
            tag.click();
            document.body.removeChild(tag);
        }
        xhr.send();
    },

    timeSinceStart: function(callback) {
        pipe.make_request("time_since_start", {}, function(response) {
            var seconds = JSON.parse(response);
            callback(seconds);
        });
    }
    
}
