from unittest import TestCase
import json
import tempfile

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

    def test_default_argument(self):
        argument = arguments.DefaultArgument("x", 42)
        self.assertEqual(argument.get_name(), "x")
        self.assertEqual(argument.get_default_value(), 42)


class TestResults(TestCase):

    def test_basic_result(self):
        argument = outputs.BasicOutput("x")
        self.assertEqual(argument.get_name(), "x")


class TestRoutines(TestCase):

    def test_basic_routine(self):

        def add_3_and_4():
            routine = routines.BasicRoutine("x = a + b")
            routine.execute_and_get_standard_output_and_error(
                [arguments.DefaultArgument("a", 3), arguments.DefaultArgument("b", 4)],
                [outputs.BasicOutput("x")]
            )
            result = routine.read_results_file()
            self.assertEqual(result["x"], 7)

        def dot_product():
            routine = routines.BasicRoutine(
                "a0b0 = a[0] + b[0]",
                "a1b1 = a[1] + b[1]",
                "x = a0b0 + a1b1"
            )
            routine.execute_and_get_standard_output_and_error(
                [arguments.DefaultArgument("a", [2,4]), arguments.DefaultArgument("b", [3,1])],
                [outputs.BasicOutput("x")]
            )
            result = routine.read_results_file()
            self.assertEqual(result["x"], 10)

        def read_field():
            routine = routines.BasicRoutine(
                "class A:",
                "  def __init__(self):"
                "    self.x = 42",
                "read = A().x"
            )
            routine.execute_and_get_standard_output_and_error(
                [],
                [outputs.BasicOutput("read")]
            )
            result = routine.read_results_file()
            self.assertEqual(result["read"], 42)

        add_3_and_4()
        dot_product()
        read_field()


class TestTemplates(TestCase):

    def test_basic_template(self):
        args = [arguments.DefaultArgument("x", 100), arguments.DefaultArgument("y", 10)]
        outs = [outputs.BasicOutput("ratio")]
        routine = routines.BasicRoutine("ratio = x / y")
        template = templates.BasicTemplate("test", args, outs, routine)

        def test_template_name():
            self.assertEqual(template.get_name(), "test")

        def test_argument_names():
            names = template.list_arguments()
            self.assertListEqual(names, ["x", "y"])

        def test_execution():
            _, result = template.execute_to_get_log_and_results()
            self.assertEqual(result["ratio"], 10)

        test_template_name()
        test_argument_names()
        test_execution()


class TestNodes(TestCase):

    def test_basic_node(self):
        args = [arguments.DefaultArgument("x", 100), arguments.DefaultArgument("y", 10)]
        outs = [outputs.BasicOutput("ratio")]
        routine = routines.BasicRoutine("ratio = x / y")
        template = templates.BasicTemplate("test", args, outs, routine)
        node = nodes.BasicNode(template)
        node.evaluate()
        self.assertEqual(node.read_output("ratio"), 10)


class TestGraph(TestCase):

    def test_basic_graph(self):
        def make_sum_node():
            args = [arguments.DefaultArgument("x", 1), arguments.DefaultArgument("y", 2)]
            outs = [outputs.BasicOutput("z")]
            routine = routines.BasicRoutine("z = x + y")
            template = templates.BasicTemplate("sum", args, outs, routine)
            return nodes.BasicNode(template)

        def make_square_node():
            args = [arguments.BasicArgument("x")]
            outs = [outputs.BasicOutput("xx")]
            routine = routines.BasicRoutine("xx = x * x")
            template = templates.BasicTemplate("square", args, outs, routine)
            return nodes.BasicNode(template)

        sum_node = make_sum_node()
        square_node = make_square_node()
        graph = graphs.BasicGraph()
        graph.connect(sum_node, "z", square_node, "x")
        graph.execute_to_root(square_node)
        self.assertEqual(sum_node.read_output("z"), 3)
        self.assertEqual(square_node.read_output("xx"), 9)


class TestLibrary(TestCase):

    def test_export_and_import_to_json(self):
        lib = library.Library()
        graph = graphs.BasicGraph()

        expected = {
            "name": "Dumbledore",
            "age": 400
        }

        file = tempfile.NamedTemporaryFile()

        exporter = nodes.BasicNode(lib.get("FileSystem", "Exports", "Export JSON"))
        exporter.set_argument("filepath", "'%s'" % file.name)
        exporter.set_argument("data", expected)
        graph.execute_to_root(exporter)

        exporter = nodes.BasicNode(lib.get("FileSystem", "Imports", "Import JSON"))
        exporter.set_argument("filepath", "'%s'" % file.name)
        exporter.set_argument("data", expected)

        logger = nodes.BasicNode(lib.get("Utils", "Logging", "Log"))
        graph.connect(exporter, "output", logger, "x")
        graph.execute_to_root(logger)

        output = json.loads(logger.log.replace("'", "\""))
        self.assertEqual(output["name"], expected["name"])
        self.assertEqual(output["age"], expected["age"])

    def test_export_and_import_to_csv(self):
        lib = library.Library()
        graph = graphs.BasicGraph()

        expected = {
            "x": [1.0, 2.0, 3.0, 4.0, 5.0],
            "y": [0.5, 0.4, 0.3, 0.4, 0.5]
        }

        file = tempfile.NamedTemporaryFile()

        exporter = nodes.BasicNode(lib.get("FileSystem", "Exports", "Export CSV"))
        exporter.set_argument("filepath", "'%s'" % file.name)
        exporter.set_argument("data", expected)
        graph.execute_to_root(exporter)

        exporter = nodes.BasicNode(lib.get("FileSystem", "Imports", "Import CSV"))
        exporter.set_argument("filepath", "'%s'" % file.name)
        exporter.set_argument("data", expected)

        logger = nodes.BasicNode(lib.get("Utils", "Logging", "Log"))
        graph.connect(exporter, "output", logger, "x")
        graph.execute_to_root(logger)

        output = json.loads(logger.log.replace("'", "\""))
        self.assertListEqual(output["x"], expected["x"])
        self.assertListEqual(output["y"], expected["y"])

    def test_noise_sampling_and_formatting(self):
        lib = library.Library()
        graph = graphs.BasicGraph()

        generate = nodes.BasicNode(lib.get("Generators", "Noise", "Gaussian Random"))
        generate.set_argument("seed", 42)
        generate.set_argument("mean", 0.0)
        generate.set_argument("deviation", 10.0)
        generate.set_argument("n", 5)

        add_time = nodes.BasicNode(lib.get("Generators", "Sampling", "Insert Time Axis"))
        add_time.set_argument("start", 1.0)
        add_time.set_argument("inc", 1.0)
        graph.connect(generate, "samples", add_time, "data")

        formatter = nodes.BasicNode(lib.get("Formatting", "DataToMap", "N Dimensional"))
        formatter.set_argument("dimensions", "['t', 'x']")
        graph.connect(add_time, "samples", formatter, "data")

        logger = nodes.BasicNode(lib.get("Utils", "Logging", "Log"))
        graph.connect(formatter, "output", logger, "x")
        graph.execute_to_root(logger)

        expected = {
            "t": [1.0, 2.0, 3.0, 4.0, 5.0],
            "x": [-1.4409032957792836, -1.729036003315193, -1.1131586156766247, 7.019837250988631, -1.275882837828871]
        }

        output = json.loads(logger.log.replace("'", "\""))

        # Check names are the same
        self.assertListEqual(list(output.keys()), list(expected.keys()))

        # Check lengths of each entry are the same
        for key in expected.keys():
            self.assertEqual(len(output[key]), len(expected[key]))

        # Check all data is nearly the same (allow for some rounding error)
        for key in expected.keys():
            for i in range(len(expected[key])):
                self.assertAlmostEqual(output[key][i], expected[key][i])
