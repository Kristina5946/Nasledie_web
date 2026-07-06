"""Admin for editable landing content."""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from image_cropping import ImageCroppingMixin

from apps.landing.models import (
    Director,
    DirectorHighlight,
    FaqItem,
    GalleryItem,
    PricingPlan,
    PricingTier,
    SiteContact,
    SiteLink,
    Teacher,
)


class SingletonAdmin(admin.ModelAdmin):
    """Redirect list view to the single record edit form."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            url = reverse(
                f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
                args=[obj.pk],
            )
            return redirect(url)
        return super().changelist_view(request, extra_context)


class DirectorHighlightInline(admin.TabularInline):
    model = DirectorHighlight
    extra = 0
    fields = ('text', 'sort_order')
    ordering = ('sort_order',)


@admin.register(SiteContact)
class SiteContactAdmin(SingletonAdmin):
    fieldsets = (
        ('Контакты', {
            'fields': ('phone', 'email', 'address', 'vk_url', 'vk_label', 'legacy_url'),
        }),
        ('Карта и футер', {
            'fields': ('yandex_map_script', 'map_status', 'footer_tagline'),
        }),
    )
    search_fields = ('phone', 'email', 'address')


@admin.register(Director)
class DirectorAdmin(ImageCroppingMixin, SingletonAdmin):
    inlines = [DirectorHighlightInline]
    list_display = ('name', 'role')
    search_fields = ('name', 'role', 'quote', 'message')
    fields = ('name', 'role', 'quote', 'message', 'education', 'photo', 'photo_cropping')


@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('question', 'answer')
    ordering = ('sort_order', 'pk')
    fieldsets = (
        (None, {'fields': ('question', 'answer', 'sort_order', 'is_published')}),
    )


@admin.register(Teacher)
class TeacherAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'role', 'color', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published', 'color')
    search_fields = ('name', 'role', 'description')
    ordering = ('sort_order', 'pk')
    fields = (
        'name', 'role', 'description', 'color',
        'photo', 'avatar_cropping',
        'sort_order', 'is_published',
    )


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 0
    fields = ('title', 'price', 'original_price', 'icon', 'sort_order', 'is_published')
    ordering = ('sort_order',)
    show_change_link = True


@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('label', 'slug', 'note')
    inlines = [PricingPlanInline]
    fieldsets = (
        (None, {'fields': ('slug', 'label', 'note', 'sort_order', 'is_published')}),
    )


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'price', 'original_price', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published', 'tier')
    search_fields = ('title', 'price', 'original_price')
    autocomplete_fields = ('tier',)
    ordering = ('tier__sort_order', 'sort_order', 'pk')


@admin.register(GalleryItem)
class GalleryItemAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'grid_class', 'title_size', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published', 'grid_class', 'title_size')
    search_fields = ('title', 'alt_text')
    ordering = ('sort_order', 'pk')
    fields = (
        'title', 'alt_text',
        'image', 'image_cropping',
        'grid_class', 'title_size',
        'sort_order', 'is_published',
    )


@admin.register(SiteLink)
class SiteLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'group', 'href', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('group', 'is_published')
    search_fields = ('label', 'href')
    ordering = ('group', 'sort_order', 'pk')


admin.site.site_header = 'Образовательный центр «Наследие»'
admin.site.site_title = 'Наследие — админка'
admin.site.index_title = 'Управление контентом сайта'
