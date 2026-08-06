from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import TemplateView

from news.models import NewsCategory, NewsGallery, News



class NewsView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs,):
        category_id = self.request.GET.get('category')
        news = News.objects.all().order_by('-created_at')

        if category_id:
            news = news.filter(category_id=category_id)

        news_categories = NewsCategory.objects.all()
        news_gallery = NewsGallery.objects.all()

        paginator = Paginator(news, 1)
        page = self.request.GET.get('page')
        news = paginator.get_page(page)

        context = {
            'news_category': news_categories,
            'news_gallery': news_gallery,
            'news': news,
        }
        return context

class NewsDetailView(TemplateView):
    template_name = 'detail_news.html'

    def get_context_data(self, **kwargs,):
        try:
            news = News.objects.get(id=kwargs['pk'])
        except News.DoesNotExist:
            raise Http404

        context = {
            'news': news,
        }
        return context
