from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "geraetename",
        "tei",
        "landkreis",
        "kommune",
        "funkrufname",
        "status",
    )

    search_fields = (
        "geraetename",
        "tei",
        "seriennummer",
        "issi",
        "funkrufname",
        "kommune",
        "organisationsname",
    )

    list_filter = (
        "landkreis",
        "status",
    )

    ordering = (
        "geraetename",
    )