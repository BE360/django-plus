from django.contrib.admin import register, ModelAdmin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseRedirect

from admin_plus.urls import AdminUrl
from admin_plus.utils.array_utils import append, append_list

# this line is for indicating register is used in import lines. (register is used outside of this module)
if register:
    pass


class AdvancedAdmin(ModelAdmin):

    main_page_js = []
    main_page_css = []

    list_display_js = []
    list_display_css = []

    fieldsets_conditions = []  # (field, appear_condition, readonly_condition)

    __latest_list_page_full_path = ""

    def __init__(self, model, admin_site):
        self.model = model
        super(AdvancedAdmin, self).__init__(model, admin_site)

    @property
    def current_list_page_full_path(self):
        if len(self.__latest_list_page_full_path) == 0:
            return AdminUrl(model_class=self.model).get_list_url()

        else:
            return self.__latest_list_page_full_path

    def changelist_view(self, request, extra_context=None):
        self.__latest_list_page_full_path = request.get_full_path()
        return super(AdvancedAdmin, self).changelist_view(request, extra_context)

    def get_fieldsets(self, request, obj=None):

        fieldset = super(AdvancedAdmin, self).get_fieldsets(request, obj)

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
        readonly_fields = ['get_media_files_for_main_page', 'get_media_files_for_list_page'] + \
                          self.get_should_be_readonly_fields(obj)

        readonly = super(AdvancedAdmin, self).get_readonly_fields(request, obj)

        return append_list(readonly, readonly_fields, unique=True)

    def get_list_display(self, request):
        list_display = super(AdvancedAdmin, self).get_list_display(request)

        return append(list_display, 'get_media_files_for_list_page', unique=True)

    def get_to_remove_fields(self, obj):
        to_remove_fields = []

        for condition in self.fieldsets_conditions:
            if len(condition) >= 2:
                field = condition[0]
                appear_condition = condition[1]

                if appear_condition:

                    if isinstance(appear_condition, str):
                        try:
                            if not getattr(self, appear_condition)(self, obj):
                                to_remove_fields.append(field)

                        except AttributeError:
                            pass

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
                    try:
                        if not getattr(self, readonly_condition)(self, obj):
                            continue

                    except AttributeError:
                        pass

                    # If code reached here we should disappear field from fieldset
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
            body += '<link rel="stylesheet" type="text/css" href="{0}" />'.format(static(c))

        for j in js:
            body += '<script src="{0}"></script>'.format(static(j))

        return body

    def response_change(self, request, obj):
        _next = request.GET.get('next', None)

        if not _next:
            return super(AdvancedAdmin, self).response_change(request, obj)

        return HttpResponseRedirect(_next)

    def response_add(self, request, obj, post_url_continue=None):
        _next = request.GET.get('next', None)

        if not _next:
            return super(AdvancedAdmin, self).response_add(request, obj, post_url_continue)

        return HttpResponseRedirect(_next)
