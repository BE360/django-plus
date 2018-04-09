
class BoolNode:

    AND = 'AND'
    OR = 'OR'

    def __init__(self, data=None):
        self.is_connector = False
        self.data = data
        self.inverted = False

    def new_connector(self, action, left_node: 'BoolNode', right_node: 'BoolNode'):
        self.is_connector = True
        self.action = action
        self.left_node = left_node
        self.right_node = right_node

    def __and__(self, other):
        return type(self)().new_connector(self.AND, self, other)

    def __or__(self, other):
        return type(self)().new_connector(self.OR, self, other)

    def __invert__(self):
        self.inverted = not self.inverted

    def evaluate(self, *args, **kwargs):

        if self.is_connector:
            left_result = self.left_node.evaluate()
            right_result = self.right_node.evaluate()

            if self.action == self.AND:
                connector_result = left_result and right_result
            else:
                connector_result = left_result or right_result

            return connector_result ^ self.inverted

        else:
            return self.evaluate_leaf(*args, **kwargs)

    def evaluate_leaf(self, *args, **kwargs):
        raise NotImplementedError


class M(BoolNode):

    def evaluate_leaf(self, admin, model):

        return getattr(admin, self.data)(model) ^ self.inverted
