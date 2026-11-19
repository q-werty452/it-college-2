from django.views.generic import TemplateView

from .models import AboutPage, GalleryImage

# Если размер "auto" — плитки чередуются по этому шаблону,
# чтобы сетка выглядела живой без ручной настройки.
AUTO_PATTERN = ["big", "normal", "normal", "tall", "wide", "normal", "normal", "wide"]


def decorate(images):
    """Добавляет каждому фото css_class: normal / wide / tall / big."""
    result = []
    for i, img in enumerate(images):
        img.css_class = AUTO_PATTERN[i % len(AUTO_PATTERN)] if img.size == "auto" else img.size
        result.append(img)
    return result


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = AboutPage.load()

        gallery_qs = GalleryImage.objects.filter(is_active=True)
        total = gallery_qs.count()
        limit = page.gallery_limit or 6

        ctx.update({
            "page": page,
            "features": page.features.all(),
            "card_stats": page.card_stats.all(),
            "counters": page.counters.all(),
            "values": page.values.all(),
            "milestones": page.milestones.all(),
            "advantages": page.advantages.all(),
            "link_cards": page.link_cards.all(),
            "gallery_images": decorate(list(gallery_qs[:limit])),
            "gallery_has_more": total > limit,
            "gallery_total": total,
        })
        return ctx


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page"] = AboutPage.load()
        ctx["gallery_images"] = decorate(list(GalleryImage.objects.filter(is_active=True)))
        return ctx
