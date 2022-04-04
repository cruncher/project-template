from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe


class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    def label_and_url_for_value(self, v):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.model._default_manager.using(self.db).get(**{key: v})
        except (ValueError, self.rel.model.DoesNotExist):
            return "", ""

        try:
            url = reverse(
                "{}:{}_{}_change".format(
                    self.admin_site.name,
                    obj._meta.app_label,
                    obj._meta.object_name.lower(),
                ),
                args=(obj.pk,),
            )
        except NoReverseMatch:
            url = ""  # Admin not registered for target model.

        return (
            mark_safe(
                '<span class="pill"><strong><a href="{}">{}'
                "</a></strong></span>".format(url, str(obj))
            ),
            "",
        )


class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
    def label_and_url_for_value(self, value):
        result = []
        for v in value:
            key = self.rel.get_related_field().name
            try:
                obj = self.rel.model._default_manager.using(self.db).get(**{key: v})
            except (ValueError, self.rel.model.DoesNotExist):
                return "", ""

            try:
                url = reverse(
                    "{}:{}_{}_change".format(
                        self.admin_site.name,
                        obj._meta.app_label,
                        obj._meta.object_name.lower(),
                    ),
                    args=(obj.pk,),
                )
            except NoReverseMatch:
                url = ""  # Admin not registered for target model.

            result.append(
                '<span class="pill"><strong><a href="{}">{}</a>'
                '</strong>&nbsp;<a class="deletelink rel-delete-link" '
                'data-rel="{}" href="#"></a></span>'.format(url, str(obj), obj.pk)
            )

        return mark_safe(" ".join(result)), ""


class ImprovedModelForm(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.remote_field.__class__.__name__
            if type == "ManyToOneRel":
                kwargs["widget"] = VerboseForeignKeyRawIdWidget(
                    db_field.remote_field, site
                )
            elif type == "ManyToManyRel":
                kwargs["widget"] = VerboseManyToManyRawIdWidget(
                    db_field.remote_field, site
                )
            return db_field.formfield(**kwargs)
        return super(ImprovedModelForm, self).formfield_for_dbfield(db_field, **kwargs)

    class Media:
        js = ("admin/js/improved_admin_rel.js",)
        css = {"all": ("admin/css/admin-pills.css",)}


# def formfield_for_dbfield(self, db_field, **kwargs):
#         if db_field.name in self.raw_id_fields:
#             kwargs.pop("request", None)
#             type = db_field.remote_field.__class__.__name__
#             if type in ("ManyToOneRel", "OneToOneRel"):
#                 kwargs["widget"] = VerboseForeignKeyRawIdWidget(
#                     db_field.remote_field, self.admin_site
#                 )
#             elif type == "ManyToManyRel":
#                 kwargs["widget"] = VerboseManyToManyRawIdWidget(
#                     db_field.remote_field, self.admin_site
#                 )
#             return db_field.formfield(**kwargs)
#         return super().formfield_for_dbfield(
#             db_field, **kwargs
#         )
