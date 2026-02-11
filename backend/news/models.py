from django.db import models

class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # 数据库中列名就是'title'
    url = models.CharField(max_length=255)  # 之前模型中缺少这个字段
    hot_rank = models.IntegerField(null=True, blank=True)  # 数据库中允许为NULL
    source = models.IntegerField()  # 添加数据源字段
    batch_timestamp = models.DateTimeField(null=True, blank=True)  # 批次时间戳字段
    created_at = models.DateTimeField(auto_now_add=True)  # CURRENT_TIMESTAMP默认值
    
    def __str__(self):
        return f"{self.source} - {self.hot_rank} - {self.title}"
    
    class Meta:
        db_table = 'ranking'
        verbose_name = '新闻文章'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['source', 'batch_timestamp']),
            models.Index(fields=['source', 'hot_rank']),
        ]
        ordering = ['hot_rank']