from unittest import TestCase
import importlib
import json

from pipe.graph import arguments
from pipe.graph import outputs
from pipe.graph import routines
from pipe.graph import templates
from pipe.graph import nodes
from pipe.graph import graphs
from pipe.graph import library


class TestArguments(TestCase):

    def test_basic_argument(self):
        argument = arguments.BasicArgument("x")
        self.assertEqual(argument.get_name(), "x")


class TestOutputs(TestCase):

    def test_basic_outputs(self):
        argument = outputs.BasicOutput("x")
        self.assertEqual(argument.get_name(), "x")


class TestRoutines(TestCase):

    def test_basic_c_routine(self):
        code =                                     \
            "#include <stdio.h>\n"                 \
            "#include <stdlib.h>\n"                \
            "int main(int argc, char *argv[]) {\n" \
            "    int a = atoi(argv[1]);\n"         \
            "    int b = atoi(argv[2]);\n"         \
            "    int c = atoi(argv[3]);\n"         \
            "    int sum = a + b + c;\n"           \
            "    printf(\"%d\", sum);\n"           \
            "    return 0;\n"                      \
            "}\n"
        routine = routines.CRoutine(code)
        result = int(routine.execute(["20", "20", "2"]))
        self.assertEqual(result, 42)

    def test_basic_python_routine(self):
        code =                       \
            "import sys\n"           \
            "a = int(sys.argv[1])\n" \
            "b = int(sys.argv[2])\n" \
            "c = int(sys.argv[3])\n" \
            "print(a + b + c)\n"
        routine = routines.PythonRoutine(code)
        result = int(routine.execute(["20", "20", "2"]))
        self.assertEqual(result, 42)

    def test_basic_ruby_routine(self):
        code = \
            "puts ARGV[0].to_i + ARGV[1].to_i"
        routine = routines.RubyRoutine(code)
        result = int(routine.execute(["3", "5"]))
        self.assertEqual(result, 8)
        

class TestTemplates(TestCase):

    def test_basic_uniform_noise_node(self):
        l = library.load_interal()
        template = l.get("Generate.Noise.Uniform")
        data = template.as_json()
        self.assertEqual(list(data["args"]), [{'name': 'seed'}, {'name': 'n'}, {'name': 'from'}, {'name': 'to'}])
        self.assertEqual(list(data["outs"]), [{'name': 'points'}])
        expected = [
            8.599796663725433,
            7.821589626462722,
            4.7851442274776055,
            3.3302507526366703,
            5.601472492317477
        ]
        result = template.execute({'seed': '0', 'n': '5', 'from': '1', 'to': '10'})
        parsed = json.loads(result["points"])
        self.assertAlmostEqual(parsed, expected)

    def test_basic_sum_template(self):
        l = library.load_interal()
        template = l.get("Math.Sets.Sum")
        data = template.as_json()
        self.assertEqual(list(data["args"]), [{'name': 'points'}])
        self.assertEqual(list(data["outs"]), [{'name': 'summed'}])
        self.assertEqual(template.execute({'points' : '[20.0, 20.0, 2]'}), {"summed": '42.0'})


class TestNodes(TestCase):

    def test_basic_uniform_noise_node(self):
        l = library.load_interal()
        node = nodes.BasicNode(l, "Generate.Noise.Uniform")
        node.set_argument("seed", "0")
        node.set_argument("n", "5")
        node.set_argument("from", "1")
        node.set_argument("to", "10")
        node.evaluate()
        expected = [
            8.599796663725433,
            7.821589626462722,
            4.7851442274776055,
            3.3302507526366703,
            5.601472492317477
        ]
        result = json.loads(node.read_output("points"))
        self.assertAlmostEqual(result, expected)

    def test_basic_sum_node(self):
        l = library.load_interal()
        node = nodes.BasicNode(l, "Math.Sets.Sum")
        node.set_argument("points", "[20.0, 20.0, 2]")
        node.evaluate()
        self.assertEqual(node.read_output("summed"), str(42.0))


class TestLibrary(TestCase):

    def test_add(self):
        l = library.load_interal()
        template = templates.from_data(["in"], ["out"], "py", "import sys; print(sys.argv[1])")
        l.add("a", template)
        self.assertEqual(len(l.list_templates()), 3)
        template = l.get("a")
        data = template.as_json()
        self.assertEqual(list(data["args"]), [{'name': 'in'}])
        self.assertEqual(list(data["outs"]), [{'name': 'out'}])
        self.assertEqual(template.execute({'in' : '"hello world"'}), {'out': '"hello world"'})

    def test_new(self):
        l = library.load_interal()
        l.new("a", ["in"], ["out"], "py", "import sys; print(sys.argv[1])")
        self.assertEqual(len(l.list_templates()), 3)
        template = l.get("a")
        data = template.as_json()
        self.assertEqual(list(data["args"]), [{'name': 'in'}])
        self.assertEqual(list(data["outs"]), [{'name': 'out'}])
        self.assertEqual(template.execute({'in' : '"hello world"'}), {'out': '"hello world"'})

    def test_replace(self):
        l = library.load_interal()
        sum_template = l.get("Math.Sets.Sum")
        l.replace("Generate.Noise.Uniform", sum_template)

        # Check library size
        self.assertEqual(len(l.list_templates()), 2)

        # Check template was indeed replaced
        template = l.get("Generate.Noise.Uniform")
        data = template.as_json()
        self.assertEqual(list(data["args"]), [{'name': 'points'}])
        self.assertEqual(list(data["outs"]), [{'name': 'summed'}])

    def test_remove(self):
        l = library.load_interal()
        sum_template = l.get("Math.Sets.Sum")
        l.remove("Math.Sets.Sum")
        self.assertEqual(len(l.list_templates()), 1)
        self.assertIn('Generate.Noise.Uniform', l.list_templates())
        self.assertNotIn('Math.Sets.Sum', l.list_templates())
        l.add("Math.Sets.Sum", sum_template)
        self.assertEqual(len(l.list_templates()), 2)
        self.assertIn('Generate.Noise.Uniform', l.list_templates())
        self.assertIn('Math.Sets.Sum', l.list_templates())

    def test_move(self):
        l = library.load_interal()
        l.move("Math.Sets.Sum", "a")
        self.assertEqual(len(l.list_templates()), 2)
        self.assertIn('Generate.Noise.Uniform', l.list_templates())
        self.assertIn("a", l.list_templates())
        self.assertNotIn('Math.Sets.Sum', l.list_templates())
        l.move("a", "Math.Sets.Sum")
        self.assertEqual(len(l.list_templates()), 2)
        self.assertIn('Generate.Noise.Uniform', l.list_templates())
        self.assertIn('Math.Sets.Sum', l.list_templates())
        self.assertNotIn("a", l.list_templates())


class TestGraphs(TestCase):

    def test_new_node(self):
        graph = graphs.BasicGraph()
        node = graph.new_node("Math.Sets.Sum", x=500, y=200)
        self.assertEqual(node.x, 500)
        self.assertEqual(node.y, 200)

    def test_query_node(self):
        graph = graphs.BasicGraph()
        node = graph.new_node("Math.Sets.Sum")
        node_copy = graph.get_node(node.node_id)
        self.assertEqual(node, node_copy)

    def test_new_node_failure(self):
        graph = graphs.BasicGraph()
        try:
            graph.new_node("xxx")
            raise Exception("Key error should be thrown")
        except KeyError:
            pass

    def test_assign_variable(self):
        graph = graphs.BasicGraph()
        node = graph.new_node("Math.Sets.Sum")
        graph.assign_argument(node.node_id, "points", "[20.0, 10.0, 2.0]")
        self.assertEqual(node.arguments["points"], "[20.0, 10.0, 2.0]")

    def test_new_edge(self):
        graph = graphs.BasicGraph()
        noise_node = graph.new_node("Generate.Noise.Uniform")
        sum_node = graph.new_node("Math.Sets.Sum")
        graph.connect(
            noise_node, "points",
            sum_node, "points"
        )
        self.assertEqual(len(graph.edges), 1)

    def test_evaluate(self):
        graph = graphs.BasicGraph()
        noise_node = graph.new_node("Generate.Noise.Uniform")
        sum_node = graph.new_node("Math.Sets.Sum")
        graph.connect(noise_node, "points", sum_node, "points")
        graph.assign_argument(noise_node.node_id, "seed", "0")
        graph.assign_argument(noise_node.node_id, "n", "5")
        graph.assign_argument(noise_node.node_id, "from", "1")
        graph.assign_argument(noise_node.node_id, "to", "10")
        graph.execute(sum_node)
        self.assertAlmostEqual(
            float(sum_node.outputs["summed"]),
            30.138253762619907
        )

    def test_list_nodes(self):
        graph = graphs.BasicGraph()
        noise_node = graph.new_node("Generate.Noise.Uniform")
        sum_node = graph.new_node("Math.Sets.Sum")
        graph.connect(noise_node, "points", sum_node, "points")
        result = graph.list_nodes()
        self.assertEqual(len(result), 2)
        self.assertEqual(noise_node, graph.get_node(noise_node.node_id))
        self.assertEqual(sum_node, graph.get_node(sum_node.node_id))

    def test_list_edges(self):
        graph = graphs.BasicGraph()
        noise_node = graph.new_node("Generate.Noise.Uniform")
        sum_node = graph.new_node("Math.Sets.Sum")
        graph.connect(noise_node, "points", sum_node, "points")
        result = graph.list_edges()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["node_id_from"], noise_node.node_id)
        self.assertEqual(result[0]["node_id_to"], sum_node.node_id)
        self.assertEqual(result[0]["arg_from"], "points")
        self.assertEqual(result[0]["arg_to"], "points")

    def test_as_json(self):
        graph = graphs.BasicGraph()
        noise_node = graph.new_node("Generate.Noise.Uniform")
        sum_node = graph.new_node("Math.Sets.Sum")
        graph.connect(noise_node, "points", sum_node, "points")
        result = graph.as_json()

        # Check library
        self.assertEqual(len(result["library"]), 2)
        self.assertIn('Generate.Noise.Uniform', result["library"].keys())
        self.assertIn('Math.Sets.Sum', result["library"].keys())

        # Check nodes
        ids = [n["id"] for n in result["nodes"]]
        self.assertEqual(len(ids), 2)
        self.assertIn(noise_node.node_id, ids)
        self.assertIn(sum_node.node_id, ids)

        # Check edges
        self.assertEqual(len(result["edges"]), 1)
        self.assertEqual(result["edges"][0]["node_id_from"], noise_node.node_id)
        self.assertEqual(result["edges"][0]["node_id_to"], sum_node.node_id)
        self.assertEqual(result["edges"][0]["arg_from"], "points")
        self.assertEqual(result["edges"][0]["arg_to"], "points")
        
    def test_from_json(self):
        json_data = {
            'library': 
                {
                    'Generate.Noise.Uniform': {
                        'args': [{'name': 'seed'}, {'name': 'n'}, {'name': 'from'}, {'name': 'to'}], 
                        'outs': [{'name': 'points'}],
                        'routine': {
                            'extension': 'py',
                            'code': 'import sys\nimport random\nseed = int(sys.argv[1])\nn    = int(sys.argv[2])\ns    = float(sys.argv[3])\ne    = float(sys.argv[4])\nrandom.seed(seed)\ndelta = e - s\npoints = [\n   s + random.random() * delta   for i in range(n)\n]\nprint(points)\n'
                        }
                    },
                    'Math.Sets.Sum': {
                        'args': [{'name': 'points'}],
                        'outs': [{'name': 'summed'}],
                        'routine': {
                            'extension': 'py',
                            'code': 'import sys\nimport json\npoints = json.loads(sys.argv[1])\nsummed = sum(points)\nprint(summed)\n'
                        }
                    }
            },            
            'nodes': [
                {'path': 'Generate.Noise.Uniform', 'id': 4417478384, 'args': {}, 'outs': {}, 'x': 100, 'y': 200},
                {'path': 'Math.Sets.Sum', 'id': 4417562888, 'args': {}, 'outs': {}, 'x': 200, 'y': 300}
            ], 
            'edges': [
                {'node_id_from': 4417478384, 'arg_from': 'points', 'node_id_to': 4417562888, 'arg_to': 'points'}
            ]
        }

        graph = graphs.from_json(json_data)
        result = graph.as_json()
        self.assertTrue(result)
        self.assertEqual(len(result["library"]), 2)
        self.assertEqual(len(result["nodes"]), 2)
        self.assertEqual(len(result["edges"]), 1)
