from django.db import models


# Create your models here.
class django_down_excel(models.Model):
    name = models.CharField(max_length=20, db_column='检测员姓名')
    # 检测日期	检测地点 破损管道编号 破损程度	破损坐标
    date = models.CharField(max_length=20, db_column='检测日期')
    pot = models.CharField(max_length=20, db_column='检测地点')
    num = models.IntegerField(db_column='破损管道编号')
    level = models.IntegerField(db_column='破损程度')
    location = models.CharField(max_length=20, db_column='破损坐标')


class User(models.Model):
    account = models.IntegerField()
    password = models.CharField(max_length=12)
    name = models.CharField(max_length=24)
    # title = models.CharField(max_length=100)
    # content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)