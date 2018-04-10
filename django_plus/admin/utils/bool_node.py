class BoolNode:
    AND = 'AND'
    OR = 'OR'

    default = AND

    def __init__(self, *contents):
        self.is_connector = False
        self.contents = contents
        self.inverted = False

    def change_to_connector(self, action, left_node: 'BoolNode', right_node: 'BoolNode'):
        self.is_connector = True
        self.action = action
        self.left_node = left_node
        self.right_node = right_node

    def __and__(self, other):
        return type(self)().change_to_connector(self.AND, self, other)

    def __or__(self, other):
        return type(self)().change_to_connector(self.OR, self, other)

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
            return self.__evaluate_leaf__(*args, **kwargs)

    def __evaluate_leaf__(self, *args, **kwargs):
        if not hasattr(self, 'leaf_evaluator'):
            raise Exception("You should use bool_node_class_generator instead of "
                            "directly extending BoolNode class")

        if self.default == self.AND:
            for content in self.contents:
                if not self.leaf_evaluator(*args, **kwargs, content=content):
                    return self.inverted

            return not self.inverted

        else:
            for content in self.contents:
                if self.leaf_evaluator(*args, **kwargs, content=content):
                    return not self.inverted

            return self.inverted


def bool_node_class_generator(leaf_evaluator):
    class NodeWrapper(BoolNode):
        def __init__(self, *contents):
            self.leaf_evaluator = leaf_evaluator

            super(NodeWrapper, self).__init__(*contents)

    return NodeWrapper
