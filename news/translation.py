from news.models import NewsCategory, News
from modeltranslation.translator import register, TranslationOptions

@register(NewsCategory)
class NewsCategory(TranslationOptions):
    fields = ('title',)


@register(News)
class News(TranslationOptions):
    fields = ('title','text')