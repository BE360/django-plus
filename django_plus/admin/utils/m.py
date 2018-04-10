from .bool_node import bool_node_class_generator


def leaf_evaluator(admin, model, content):
    return getattr(admin, content)(model)

M = bool_node_class_generator(leaf_evaluator)
