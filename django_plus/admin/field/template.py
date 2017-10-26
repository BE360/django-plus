from django.template.loader import render_to_string

from ._generator_ import admin_field_generator


def template(template_name, verbose_name=""):

    def function_changer(func, admin_inst, model_inst):
        """
        :param func: returns a context
        :param admin_inst:
        :param model_inst:
        :return:
        """
        ctx = func(admin_inst, model_inst)
        return render_to_string(template_name, ctx)

    return admin_field_generator(
        verbose_name=verbose_name,
        function_changer=function_changer,
        html=True
    )
