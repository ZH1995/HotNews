from django.shortcuts import render
from .models import NewsArticle

def index(request):
    # 先查询出数据库中create_at的最大值
    latest_date = NewsArticle.objects.latest('created_at').created_at

    # 然后按照create_at等于最大值且按hot_rank升序排列，取出所有数据
    latest_news_list = NewsArticle.objects.filter(created_at=latest_date).order_by('hot_rank')
    context = {'latest_news_list': latest_news_list}
    return render(request, 'news/index.html', context)