from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import NewsArticle
from collections import defaultdict
from django.db.models import Max
from django.core.cache import cache

# 数据源配置
SOURCE_CONFIG = {
    1: {'title': '微博', 'logo': '/images/weibo_logo.png', 'limit': 50},
    3: {'title': '百度', 'logo': '/images/baidu_logo.png', 'limit': 50},
    4: {'title': '36氪', 'logo': '/images/kr36_logo.png', 'limit': 50},
    5: {'title': '抖音', 'logo': '/images/douyin_logo.png', 'limit': 50},
    6: {'title': '华尔街见闻', 'logo': '/images/wallstreetcn_logo.png', 'limit': 10},
    7: {'title': '澎湃新闻', 'logo': '/images/thepaper_logo.png', 'limit': 10},
}

SCHOOL_SOURCES_CONFIG = {
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
    show_school_sources = request.GET.get('show_school_sources', '0')
    if show_school_sources == '1':
        sources.extend([
            {
                'id': source_id,
                'title': config['title'],
                'logo': config['logo'],
                'limit': config['limit']
            }
            for source_id, config in SCHOOL_SOURCES_CONFIG.items()
        ])
    return Response({'sources': sources})

@api_view(['GET'])
def get_ranking_data(request, source_id):
    """获取单个榜单数据的API（缓存优化版）"""
    try:
        source_id = int(source_id)
    except ValueError:
        return Response({'error': 'Invalid source ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 确定数据源配置
    if source_id in SOURCE_CONFIG:
        source_config = SOURCE_CONFIG[source_id]
    elif source_id in SCHOOL_SOURCES_CONFIG:
        source_config = SCHOOL_SOURCES_CONFIG[source_id]
    else:
        return Response({'error': 'Source not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # 缓存键
    cache_key = f'latest_batch_{source_id}'
    latest_batch = cache.get(cache_key)
    
    # 如果缓存不存在，查询并缓存（60秒）
    if latest_batch is None:
        latest_batch = NewsArticle.objects.filter(
            source=source_id
        ).aggregate(latest_timestamp=Max('batch_timestamp'))['latest_timestamp']
        
        if latest_batch:
            cache.set(cache_key, latest_batch, timeout=60)  # 缓存60秒
    
    if not latest_batch:
        return Response({
            'id': source_id,
            'title': source_config['title'],
            'logo': source_config['logo'],
            'articles': []
        })
    
    # 只查询需要的字段（减少数据传输）
    articles = NewsArticle.objects.filter(
        source=source_id, 
        batch_timestamp=latest_batch
    ).only('id', 'title', 'url', 'hot_rank').order_by('hot_rank')[:source_config['limit']]
    
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
        'title': source_config['title'],
        'logo': source_config['logo'],
        'articles': articles_data
    })