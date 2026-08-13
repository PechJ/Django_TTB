from django.utils import timezone

from devices.models import ImportStatus


def update_import_status(import_type):

    status, created = ImportStatus.objects.get_or_create(
        import_type=import_type,
    )

    status.last_import = timezone.now()

    status.save(
        update_fields=["last_import"]
    )

    return status