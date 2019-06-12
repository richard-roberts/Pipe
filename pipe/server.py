import os
import json
import time

from flask import send_from_directory
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from pipe.graph import graphs


# ---------------------------------------------------------------------------- #
# Globals

graph = graphs.BasicGraph()
library = graph.lib
start_time = time.time()

file_storage_directory = f"{os.path.dirname(os.path.abspath(__file__))}/uploads"
if not os.path.exists(file_storage_directory):
    os.makedirs(file_storage_directory)

#
# ---------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------- #
# Pipe API Wrapper
  
def call_list_templates():
    return library.list_templates()

def call_query_template(path):
    return library.get(path).as_json()

def call_add_or_update_template(path, args, outs, extension, code):
    if library.is_valid_path(path):
        old_template = library.get(path)
        new_template = library.create_or_update_basic_template(path, args, outs, extension, code)
        graph.replace_template(old_template, new_template)
        return new_template.as_json()
    else:
        template = library.create_or_update_basic_template(path, args, outs, extension, code)
        return template.as_json()

def call_rename_template(old_path, new_path):
    library.rename_template(old_path, new_path)
    graph.rename_template(old_path, new_path)
    return True

def call_remove_template(path):
    library.remove(path)
    graph.remove_template(path)
    return True

def call_new_node(path, x=0, y=0):
    try:
        return graph.new_node(path, x=x, y=y).as_json()
    except KeyError:
        return False

def call_query_node(id):
    return graph.get_node(id).as_json()

def call_set_node_position(id, x, y):
    try:
        graph.set_node_position(id, x, y)
        return True
    except KeyError as e:
        return str(e)
    
def call_assign_argument(id, name, value):
    graph.assign_argument(id, name, value)
    return True
    
def call_new_edge(id_from, arg_from, id_to, node_to):
    return graph.connect_by_id(id_from, arg_from, id_to, node_to).as_json()
    
def call_delete_edge(id_from, arg_from, id_to, arg_to):
    graph.delete_edge_by_match(id_from, arg_from, id_to, arg_to)
    return True

def call_delete_node(id):
    graph.delete_node(id)
    return True

def call_execute(id):
    try:
        return graph.execute_by_id(id).as_json()
    except KeyError:
        return False

def call_list_nodes():
    return graph.list_nodes()

def call_list_edges():
    return graph.list_edges()

def call_as_json():
    return graph.as_json()

def call_from_json(data):
    global graph, library
    graph = graphs.from_json(data)
    library = graph.lib
    return True

def call_upload(path, file):
    filepath = os.path.join(file_storage_directory, file.filename)
    file.save(filepath)
    library.create_or_update_file_template(path, filepath)
    return True

def call_download(filepath):
    file_storage_directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(file_storage_directory, filename, as_attachment=True)

def call_time_since_start():
    return time.time() - start_time

#
# ---------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------- #
# Server

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/list_templates", methods=["GET"])
@cross_origin()
def list_templates():
    return json.dumps(call_list_templates())

@app.route("/query_template", methods=["GET"])
@cross_origin()
def query_template():
    return json.dumps(call_query_template(
        request.args["path"]
    ))

@app.route("/add_or_update_template", methods=["GET"])
@cross_origin()
def add_or_update_template():
    return json.dumps(call_add_or_update_template(
        request.args["path"],
        json.loads(request.args["args"]),
        json.loads(request.args["outs"]),
        request.args["extension"],
        request.args["code"]
    ))

@app.route("/rename_template", methods=["GET"])
@cross_origin()
def rename_template():
    return json.dumps(call_rename_template(
        request.args["old_path"],
        request.args["new_path"]
    ))

@app.route("/remove_template", methods=["GET"])
@cross_origin()
def remove_template():
    return json.dumps(call_remove_template(
        request.args["path"]
    ))

@app.route("/new_node", methods=["GET"])
@cross_origin()
def new_node():
    return json.dumps(call_new_node(
        request.args["path"],
        request.args["x"],
        request.args["y"]
    ))

@app.route("/query_node", methods=["GET"])
@cross_origin()
def query_node():
    return json.dumps(call_query_node(
        json.loads(request.args["id"])
    ))

@app.route("/set_node_position", methods=["GET"])
@cross_origin()
def set_node_position():
    return json.dumps(call_set_node_position(
        json.loads(request.args["id"]),
        request.args["x"],
        request.args["y"]
    ))

@app.route("/assign_argument", methods=["GET"])
@cross_origin()
def assign_argument():
    return json.dumps(call_assign_argument(
        json.loads(request.args["id"]),
        request.args["name"],
        request.args["value"]
    ))

@app.route("/new_edge", methods=["GET"])
@cross_origin()
def new_edge():
    return json.dumps(call_new_edge(
        json.loads(request.args["id_from"]),
        request.args["arg_from"],
        json.loads(request.args["id_to"]),
        request.args["node_to"]
    ))

@app.route("/delete_edge", methods=["GET"])
@cross_origin()
def delete_edge():
    return json.dumps(call_delete_edge(
        json.loads(request.args["node_id_from"]),
        request.args["arg_from"],
        json.loads(request.args["node_id_to"]),
        request.args["arg_to"]
    ))

@app.route("/delete_node", methods=["GET"])
@cross_origin()
def delete_node():
    return json.dumps(call_delete_node(
        json.loads(request.args["id"])
    ))

@app.route("/execute", methods=["GET"])
@cross_origin()
def execute():
    return json.dumps(call_execute(
        json.loads(request.args["id"])
    ))

@app.route("/list_nodes", methods=["GET"])
@cross_origin()
def list_nodes():
    return json.dumps(call_list_nodes())

@app.route("/list_edges", methods=["GET"])
@cross_origin()
def list_edges():
    return json.dumps(call_list_edges())

@app.route("/as_json", methods=["GET"])
@cross_origin()
def as_json():
    return json.dumps(call_as_json(), indent=4, sort_keys=True)

@app.route("/from_json", methods=["GET"])
@cross_origin()
def from_json():
    return json.dumps(call_from_json(
        json.loads(request.args["data"])
    ))

@app.route('/upload', methods=['POST'])
def upload():
    if request.files:
        return json.dumps(call_upload(
            request.form["path"],
            request.files["file"]
        ))
    return json.dumps(False)
    
@app.route('/download', methods=['GET'])
def download():
    return call_download(request.args["filepath"])

@app.route("/time_since_start", methods=["GET"])
@cross_origin()
def time_since_start():
    return json.dumps(call_time_since_start())

#   
# ---------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------- #
# Execution

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8000)

#
# ---------------------------------------------------------------------------- #

