from django_plus.admin.field import admin_field_generator


def image(verbose_name="", width_px=200):

    def function_changer(func, admin_inst, model_inst):
        """
        :param func: returns an AdminFormAjaxData object
        :param admin_inst:
        :param model_inst:
        :return: html string
        """

        image_link = func(admin_inst, model_inst)

        return "<img style='width:%spx' src='%s'/>" % (width_px, image_link)

    return admin_field_generator(verbose_name=verbose_name, function_changer=function_changer, html=True)
