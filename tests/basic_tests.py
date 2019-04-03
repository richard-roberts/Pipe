from unittest import TestCase

from pipe.graph import arguments
from pipe.graph import outputs
from pipe.graph import routines
from pipe.graph import templates
from pipe.graph import nodes
from pipe.graph import graphs


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
            result = template.execute()
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
