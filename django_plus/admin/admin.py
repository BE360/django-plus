from django.contrib.admin import register, ModelAdmin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseRedirect

from django_plus.admin.urls import AdminUrl
from django_plus.admin.utils.array_utils import append, append_list
import copy
from urllib.parse import unquote
from django_plus.admin import M

# this line is for indicating register is used in import lines. (register is used outside of this module)
if register:
    pass


class AdvancedAdmin(ModelAdmin):

    main_page_js = []
    main_page_css = []

    list_display_js = []
    list_display_css = []

    fieldsets_conditions = []  # (field, appear_condition, readonly_condition)

    __fieldsets__ = None

    __readonly_fields__ = [
        'get_list_item_initializer',
        'get_media_files_for_main_page',
        'get_media_files_for_list_page'
    ]

    def __init__(self, model, admin_site):
        self.model = model
        self.request = None
        super(AdvancedAdmin, self).__init__(model, admin_site)

    @property
    def current_list_page_full_path(self):
        if not self.request:
            return AdminUrl(model_class=self.model).get_list_url()

        else:
            return self.request.get_full_path()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.request = request
        return super(AdvancedAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super(AdvancedAdmin, self).changelist_view(request, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.request = request
        return super(AdvancedAdmin, self).add_view(request, form_url, extra_context)

    def get_fieldsets(self, request, obj=None):

        if self.__fieldsets__ is None:
            self.__fieldsets__ = super(AdvancedAdmin, self).get_fieldsets(request, obj)

        fieldset = copy.deepcopy(self.__fieldsets__)

        # removing fields with conditions
        to_remove_fields = self.get_to_remove_fields(obj)

        for fields_data in fieldset:
            fields = fields_data[1]['fields']
            fields_data[1]['fields'] = [f for f in fields if f not in to_remove_fields]

        # inserting 'get_media_fields_for_main_page' to fieldset
        fields = fieldset[0][1]['fields']
        fields = append(fields, 'get_media_files_for_main_page', unique=True)

        fieldset[0][1]['fields'] = fields

        return fieldset

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.__readonly_fields__ + self.get_should_be_readonly_fields(obj)

        readonly = super(AdvancedAdmin, self).get_readonly_fields(request, obj)

        return append_list(readonly, readonly_fields, unique=True)

    def get_list_display(self, request):
        list_display = super(AdvancedAdmin, self).get_list_display(request)

        list_display = append(list_display, 'get_list_item_initializer')
        return append(list_display, 'get_media_files_for_list_page', unique=True)

    def get_to_remove_fields(self, obj):
        to_remove_fields = []

        for condition in self.fieldsets_conditions:
            if len(condition) >= 2:
                field = condition[0]
                appear_condition = condition[1]

                if appear_condition:

                    if isinstance(appear_condition, M):
                        if not appear_condition.evaluate(self, obj):
                            to_remove_fields.append(field)

                    elif isinstance(appear_condition, str):
                        try:
                            if not getattr(self, appear_condition)(obj):
                                to_remove_fields.append(field)

                        except AttributeError:
                            to_remove_fields.append(field)

                else:
                    to_remove_fields.append(field)

        return to_remove_fields

    def get_should_be_readonly_fields(self, obj):
        should_be_readonly_fields = []

        for condition in self.fieldsets_conditions:
            if len(condition) >= 3:
                field = condition[0]
                readonly_condition = condition[2]

                if readonly_condition:

                    if isinstance(readonly_condition, M):
                        if readonly_condition.evaluate(self, obj):
                            should_be_readonly_fields.append(field)

                    elif isinstance(readonly_condition, str):
                        try:
                            if getattr(self, readonly_condition)(obj):
                                should_be_readonly_fields.append(field)

                        except AttributeError:
                            pass

                    else:
                        should_be_readonly_fields.append(field)

        return should_be_readonly_fields

    def get_media_files_for_main_page(self, model):
        return self.generate_media('field-get_media_files_for_main_page', self.main_page_css, self.main_page_js)
    get_media_files_for_main_page.short_description = ""
    get_media_files_for_main_page.allow_tags = True

    def get_media_files_for_list_page(self, model):
        return self.generate_media('field-get_media_files_for_list_page', self.list_display_css,
                                   self.list_display_js)
    get_media_files_for_list_page.short_description = ""
    get_media_files_for_list_page.allow_tags = True

    def generate_media(self, fieldname, css, js):
        body = "<style>.%s{display:None;}</style>" % fieldname

        for c in css:
            if not c.startswith('http'):
                c = unquote(static(c))

            body += '<link rel="stylesheet" type="text/css" href="{0}" />'.format(c)

        for j in js:
            if not j.startswith('http'):
                j = unquote(static(j))

            body += '<script src="{0}"></script>'.format(j)

        return body

    def response_change(self, request, obj):
        _next = request.GET.get('next', None)

        if '_continue' in request.POST or not _next:
            return super(AdvancedAdmin, self).response_change(request, obj)

        return HttpResponseRedirect(_next)

    def response_add(self, request, obj, post_url_continue=None):
        _next = request.GET.get('next', None)

        if '_continue' in request.POST or not _next:
            return super(AdvancedAdmin, self).response_add(request, obj, post_url_continue)

        return HttpResponseRedirect(_next)

    def list_item_init(self, obj):
        pass

    def get_list_item_initializer(self, obj):
        self.list_item_init(obj)
        return ""
    get_list_item_initializer.short_description = ""
