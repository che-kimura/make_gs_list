from django.db import models

class EstimateInfo(models.Model):
    class Meta:
        db_table = 'estimate'

    cname = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    cls_num = models.CharField(max_length = 2)
    mark = models.CharField(max_length = 50)
    id =  models.IntegerField(primary_key=True)

    def __str__(self):
        return u'%s, %s, %s' %(self.client, self.country, self.cls_num)

class Country(models.Model):
    class Meta:
        db_table = 'country'

    code = models.CharField(max_length = 2)
    name = models.CharField(max_length = 50)
    jname = models.CharField(max_length = 50)
    area = models.CharField(max_length = 2)
    id =  models.IntegerField(primary_key=True)

    def __str__(self):
        return u'%s, %s, %s' %(self.code, self.name, self.area)
