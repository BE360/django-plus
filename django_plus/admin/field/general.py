from ._generator_ import admin_field_generator


def general(verbose_name="", html=False, boolean=False, path_to_field=None):

    return admin_field_generator(
        verbose_name=verbose_name,
        html=html,
        boolean=boolean,
        path_to_field=path_to_field
    )
