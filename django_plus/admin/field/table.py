from ._generator_ import admin_field_generator
from django.template.loader import render_to_string
import json


def table(verbose_name="", columns=None):

    def function_changer(func, admin, instance):
        table_content = func(admin, instance)

        if columns:
            columns_json = json.dumps(columns)
        else:
            columns_json = ''

        return render_to_string('admin-plus/field/table_field.html', {
            'table_content': table_content,
            'columns': columns_json
        })

    return admin_field_generator(
        verbose_name=verbose_name,
        function_changer=function_changer,
        html=True
    )
