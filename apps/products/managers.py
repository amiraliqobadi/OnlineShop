from apps.core.managers import LogicalManager


class CommentManager(LogicalManager):
    def get_queryset(self):
        return super().get_queryset().filter(reply__isnull=True)


class ProductManager(LogicalManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
