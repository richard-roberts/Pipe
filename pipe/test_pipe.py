import unittest

from pipe_backend import PipeBackend
from graph.graph_manager import GraphManager
from templates.template_collection_manager import TemplateCollectionManager


def create_simple_templates():
    template_manager = TemplateCollectionManager()

    # Create a node that gives the literal numeral 42
    template_manager.new_template("Literals", "FortyTwo", "", "o")
    template_manager.get_template("Literals", "FortyTwo").code = \
        "class FortyTwo:\n" \
        "    def __init__(self):\n" \
        "        self.o = 42\n" \
        "\n"

    # Create a node that prints its input
    template_manager.new_template("Utils", "Log", "o", "")
    template_manager.get_template("Utils", "Log").code = \
        "class Log\n:" \
        "    def __init__(self, o):\n" \
        "        print(o)\n" \
        "\n"
    return template_manager


def create_simple_graph():
    template_manager = create_simple_templates()
    graph_manager = GraphManager()
    graph = graph_manager.new_graph('test')
    node_forty_two = graph.create_node(template_manager.get_template('Literals', 'FortyTwo'), (0, 0))
    node_log = graph.create_node(template_manager.get_template('Utils', 'Log'), (0, 0))
    graph.create_edge(
        node_forty_two.get_output_argument_by_name('o'),
        node_log.get_input_argument_by_name('o')
    )
    return template_manager, graph_manager, graph


class TestTemplates(unittest.TestCase):

    def test_template_creation(self):
        template_manager = create_simple_templates()
        expected = ['GraphExecution', 'Utils', 'Literals']
        found = template_manager.get_collection_names()

        self.assertEqual(
            len(expected),
            len(found),
            msg="The template manager did not have the expected collections"
        )

        for item in expected:
            self.assertIn(
                item,
                found,
                msg="The expected collection %s was not found" % item
            )


class TestGraphs(unittest.TestCase):

    def test_new_graph(self):
        template_manager, graph_manager, graph = create_simple_graph()

        # Check correct name, number of nodes, and number of edges
        self.assertEqual(graph.name, "test")
        self.assertEqual(graph.number_of_nodes(), 2)
        self.assertEqual(graph.number_of_edges(), 1)


class TestPipe(unittest.TestCase):

    def test_open_project(self):

        pipe = PipeBackend()
        pipe.open_project("../examples/testing")

        # Make sure all expected graphs and collections are available after loading
        self.assertListEqual(
            pipe.graphs.get_names(),
            ['Main']
        )
        self.assertListEqual(
            pipe.templates.get_collection_names(),
            ['GraphExecution', 'Math', 'Utils']
        )


if __name__ == '__main__':
    unittest.main()
