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
    
}
