from django.contrib import admin
from tabbed_admin import TabbedModelAdmin

from medicine.filters import CompletionFilter
from medicine.models import Image, Instruction, Medicine


class ImageInlineAdmin(admin.StackedInline):
    model = Image
    exclude = ["id"]
    ordering = ["order", "id"]
    extra = 0


class InstructionInlineAdmin(admin.StackedInline):
    model = Instruction
    exclude = ["id"]
    ordering = ["order", "id"]
    extra = 0


class MedicineAdmin(TabbedModelAdmin):
    list_filter = [CompletionFilter]
    ordering = ["id"]
    model = Medicine
    list_display = (
        'id', "name", 'spec', 'dosage_unit', 'preparation', 'approval_number', 'barcode', 'brand', 'manufacture')
    readonly_fields = ("id", "update_time", "data_completion", "data_source")
    search_fields = (
        'id', 'name', 'barcode', 'approval_number', 'abbreviation', 'pinyin',
        'brand_abbreviation', 'brand_pinyin', 'manufacture', 'tag')
    tab_base_info = (
        ("基本信息", {
            'fields': (
                "name", "prod_name", 'spec', 'dosage_unit',
                'preparation', "pack_unit", 'approval_number', 'barcode',
                "brand", 'manufacture', "ro", "storage", "origin", "tag", "expiration", "dosage", "function")
        }),
    )
    tab_instruction = (InstructionInlineAdmin,)
    tab_image = (ImageInlineAdmin,)
    tab_meta = (
        ("元数据", {
            'fields': readonly_fields
        }),
    )
    tabs = [
        ("基本信息", tab_base_info),
        ("说明书", tab_instruction),
        ("图片", tab_image),
        ("元数据", tab_meta)
    ]


admin.site.register(Medicine, MedicineAdmin)
