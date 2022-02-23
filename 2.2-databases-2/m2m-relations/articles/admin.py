from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Tag


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag_count = 0
        tags = []
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_tag_count += 1
            if form.cleaned_data.get('tag'):
                tags.append(form.cleaned_data['tag'].id)
        if len(tags) > len(set(tags)):
            raise ValidationError('Разделы не должны повторяться')
        if main_tag_count > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif main_tag_count == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset
    extra = 3


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
