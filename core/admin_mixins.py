class SingletonAdminMixin:
    """Для разделов, где сайт показывает только одну запись (.first())."""

    def has_add_permission(self, request):
        return not self.model.objects.exists() and super().has_add_permission(request)


class ReadOnlySubmissionAdminMixin:
    """Заявки с сайта: смотреть и менять статус можно, править данные — нет."""

    editable_fields = ('status',)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name not in self.editable_fields]
