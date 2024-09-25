import ast
from dataclasses import dataclass

from ._base import Visitor

MESSAGE = "EC35: Avoid the use of try-except with a file open() in the try block."


@dataclass(frozen=True)
class EC35(Visitor):
    """
    Flake8 plugin to check for try-except blocks that contain open() calls.
    """

    def visit_Try(self, node):
        """
        Visit try-except blocks and check if open() is called inside.
        """
        for stmt in node.body:
            self.check_for_open_call(stmt)

        # Continue visiting nested nodes
        self.generic_visit(node)

    def check_for_open_call(self, node):
        """
        Check if the given node or its children contains a call to open().
        """
        if isinstance(node, ast.Call):
            if self.is_open_call(node):
                self.report(node, MESSAGE)
        else:
            # Recursively check child nodes for a call to open()
            for child in ast.iter_child_nodes(node):
                self.check_for_open_call(child)

    def is_open_call(self, node):
        """
        Check if a function call is to the built-in open() function.
        """
        return isinstance(node.func, ast.Name) and node.func.id == "open"
