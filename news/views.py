from django.shortcuts import render
from django.http import JsonResponse
from .models import NewsArticle
from collections import defaultdict
from django.db.models import Max

def index(request):
    # 获取所有数据源
    sources = [1, 3, 4, 5, 6, 7, 231, 232, 241, 242, 243, 244, 245]
    
    # 创建数据源配置，包括标题、logo和每个数据源要展示的条目数
    source_config = {
        1: {
            'title': '微博',
            'logo': '/static/images/weibo_logo.png',
            'limit': 50
        },
        3: {
            'title': '百度',
            'logo': '/static/images/baidu_logo.png',
            'limit': 50
        },
        4: {
            'title': '36氪',
            'logo': '/static/images/kr36_logo.png',
            'limit': 50
        },
        5: {
            'title': '抖音',
            'logo': '/static/images/douyin_logo.png',
            'limit': 50
        },
        6: {
            'title': '华尔街见闻',
            'logo': '/static/images/wallstreetcn_logo.png',
            'limit': 10
        },
        7: {
            'title': '澎湃新闻',
            'logo': '/static/images/thepaper_logo.png',
            'limit': 10
        },
        231: {
            'title': '23级人工1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        232: {
            'title': '23级人工2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        241: {
            'title': '24级人工1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        242: {
            'title': '24级人工2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        243: {
            'title': '24级人工3班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        244: {
            'title': '24级物联网1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        245: {
            'title': '24级物联网2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
    }
    
    # 首页只传递数据源配置，不加载具体数据
    context = {'sources': sources, 'source_config': source_config}
    return render(request, 'news/index.html', context)

def get_ranking_data(request, source_id):
    """异步获取单个榜单数据的API"""
    source_id = int(source_id)
    
    # 数据源配置
    source_config = {
        1: {
            'title': '微博',
            'logo': '/static/images/weibo_logo.png',
            'limit': 50
        },
        3: {
            'title': '百度',
            'logo': '/static/images/baidu_logo.png',
            'limit': 50
        },
        4: {
            'title': '36氪',
            'logo': '/static/images/kr36_logo.png',
            'limit': 50
        },
        5: {
            'title': '抖音',
            'logo': '/static/images/douyin_logo.png',
            'limit': 50
        },
        6: {
            'title': '华尔街见闻',
            'logo': '/static/images/wallstreetcn_logo.png',
            'limit': 10
        },
        7: {
            'title': '澎湃新闻',
            'logo': '/static/images/thepaper_logo.png',
            'limit': 10
        },
          231: {
            'title': '23级人工1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        232: {
            'title': '23级人工2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        241: {
            'title': '24级人工1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        242: {
            'title': '24级人工2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        243: {
            'title': '24级人工3班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        244: {
            'title': '24级物联网1班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
        245: {
            'title': '24级物联网2班',
            'logo': '/static/images/wczy_logo.png',
            'limit': 100
        },
    }
    
    if source_id not in source_config:
        return JsonResponse({'error': 'Invalid source ID'}, status=400)
    
    # 先获取该数据源最新的batch_timestamp
    latest_batch = NewsArticle.objects.filter(source=source_id).aggregate(
        latest_timestamp=Max('batch_timestamp')
    )['latest_timestamp']
    
    if not latest_batch:
        return JsonResponse({
            'title': source_config[source_id]['title'],
            'logo': source_config[source_id]['logo'],
            'articles': []
        })
    
    # 根据source、batch_timestamp筛选，hot_rank升序取limit条数据
    limit = source_config[source_id]['limit']
    articles = NewsArticle.objects.filter(
        source=source_id, 
        batch_timestamp=latest_batch
    ).order_by('hot_rank')[:limit]
    
    # 准备文章数据
    articles_data = []
    for article in articles:
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'hot_rank': article.hot_rank
        })
    
    return JsonResponse({
        'title': source_config[source_id]['title'],
        'logo': source_config[source_id]['logo'],
        'articles': articles_data
    })