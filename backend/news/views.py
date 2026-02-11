from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import NewsArticle
from collections import defaultdict
from django.db.models import Max

# 数据源配置
SOURCE_CONFIG = {
    1: {'title': '微博', 'logo': '/images/weibo_logo.png', 'limit': 50},
    3: {'title': '百度', 'logo': '/images/baidu_logo.png', 'limit': 50},
    4: {'title': '36氪', 'logo': '/images/kr36_logo.png', 'limit': 50},
    5: {'title': '抖音', 'logo': '/images/douyin_logo.png', 'limit': 50},
    6: {'title': '华尔街见闻', 'logo': '/images/wallstreetcn_logo.png', 'limit': 10},
    7: {'title': '澎湃新闻', 'logo': '/images/thepaper_logo.png', 'limit': 10},
    231: {'title': '23级人工1班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    232: {'title': '23级人工2班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    241: {'title': '24级人工1班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    242: {'title': '24级人工2班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    243: {'title': '24级人工3班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    244: {'title': '24级物联网1班', 'logo': '/images/wczy_logo.png', 'limit': 100},
    245: {'title': '24级物联网2班', 'logo': '/images/wczy_logo.png', 'limit': 100},
}

@api_view(['GET'])
def get_sources(request):
    """获取所有数据源配置"""
    sources = [
        {
            'id': source_id,
            'title': config['title'],
            'logo': config['logo'],
            'limit': config['limit']
        }
        for source_id, config in SOURCE_CONFIG.items()
    ]
    return Response({'sources': sources})

@api_view(['GET'])
def get_ranking_data(request, source_id):
    """获取单个榜单数据的API"""
    try:
        source_id = int(source_id)
    except ValueError:
        return Response({'error': 'Invalid source ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    if source_id not in SOURCE_CONFIG:
        return Response({'error': 'Source not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # 获取最新批次时间戳
    latest_batch = NewsArticle.objects.filter(source=source_id).aggregate(
        latest_timestamp=Max('batch_timestamp')
    )['latest_timestamp']
    
    if not latest_batch:
        return Response({
            'id': source_id,
            'title': SOURCE_CONFIG[source_id]['title'],
            'logo': SOURCE_CONFIG[source_id]['logo'],
            'articles': []
        })
    
    # 查询文章数据
    limit = SOURCE_CONFIG[source_id]['limit']
    articles = NewsArticle.objects.filter(
        source=source_id, 
        batch_timestamp=latest_batch
    ).order_by('hot_rank')[:limit]
    
    # 准备返回数据
    articles_data = [
        {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'hot_rank': article.hot_rank
        }
        for article in articles
    ]
    
    return Response({
        'id': source_id,
        'title': SOURCE_CONFIG[source_id]['title'],
        'logo': SOURCE_CONFIG[source_id]['logo'],
        'articles': articles_data
    })