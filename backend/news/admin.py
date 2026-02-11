from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'hot_rank', 'title', 'batch_timestamp', 'created_at']
    list_filter = ['source', 'batch_timestamp']
    search_fields = ['title', 'url']
    ordering = ['source', 'hot_rank']
    date_hierarchy = 'batch_timestamp'
    list_per_page = 50
