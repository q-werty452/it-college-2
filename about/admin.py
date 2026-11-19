from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    AboutPage, AboutFeature, AboutCardStat, AboutCounter, AboutValue,
    AboutMilestone, AboutAdvantage, AboutLinkCard, GalleryImage,
)


class BaseInline(admin.TabularInline):
    extra = 0
    ordering = ("order",)


class FeatureInline(BaseInline):
    model = AboutFeature
    verbose_name_plural = "Пункты блока «О колледже»"


class CardStatInline(BaseInline):
    model = AboutCardStat
    verbose_name_plural = "Цифры в карточке справа"


class CounterInline(BaseInline):
    model = AboutCounter
    verbose_name_plural = "Счётчики статистики"


class ValueInline(BaseInline):
    model = AboutValue
    verbose_name_plural = "Миссия и ценности"


class MilestoneInline(BaseInline):
    model = AboutMilestone
    verbose_name_plural = "История (этапы)"


class AdvantageInline(BaseInline):
    model = AboutAdvantage
    verbose_name_plural = "Преимущества"


class LinkCardInline(BaseInline):
    model = AboutLinkCard
    verbose_name_plural = "Карточки-ссылки (Команда)"


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Одна страница редактирования: тексты + все списки через inline."""

    fieldsets = (
        ("Шапка страницы", {"fields": ("hero_title", "hero_subtitle")}),
        ("Блок «О колледже»", {"fields": ("about_tag", "about_title", "about_text")}),
        ("Карточка справа", {"fields": ("badge_text", "card_title", "card_text")}),
        ("Миссия и ценности (заголовки)", {"classes": ("collapse",), "fields": ("values_tag", "values_title", "values_subtitle")}),
        ("История (заголовки)", {"classes": ("collapse",), "fields": ("history_tag", "history_title", "history_subtitle")}),
        ("Преимущества (заголовки)", {"classes": ("collapse",), "fields": ("adv_tag", "adv_title")}),
        ("Галерея (заголовки и лимит)", {"classes": ("collapse",), "fields": ("gallery_tag", "gallery_title", "gallery_subtitle", "gallery_limit")}),
        ("Команда (заголовки)", {"classes": ("collapse",), "fields": ("team_tag", "team_title", "team_subtitle")}),
        ("Призыв к действию", {"classes": ("collapse",), "fields": ("cta_title", "cta_text")}),
    )
    inlines = [
        FeatureInline, CardStatInline, CounterInline, ValueInline,
        MilestoneInline, AdvantageInline, LinkCardInline,
    ]

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = AboutPage.load()
        return redirect(reverse("admin:about_aboutpage_change", args=[obj.pk]))


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "size", "order", "is_active", "created_at")
    list_display_links = ("preview", "title")
    list_editable = ("size", "order", "is_active")
    list_filter = ("is_active", "size")
    search_fields = ("title",)
    readonly_fields = ("preview_large",)
    fields = ("image", "preview_large", "title", "size", "order", "is_active")

    @admin.display(description="Фото")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:56px;width:80px;object-fit:cover;border-radius:6px">',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Предпросмотр")
    def preview_large(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="max-height:240px;border-radius:10px">', obj.image.url)
        return "—"
