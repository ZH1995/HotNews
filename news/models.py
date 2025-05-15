from django.db import models

class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # 数据库中列名就是'title'
    url = models.CharField(max_length=255)  # 之前模型中缺少这个字段
    hot_rank = models.IntegerField(null=True, blank=True)  # 数据库中允许为NULL
    created_at = models.DateTimeField(auto_now_add=True)  # CURRENT_TIMESTAMP默认值
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'weibo_hot_search'
        managed = False  # 告诉Django不要管理这个表的创建/修改/删除