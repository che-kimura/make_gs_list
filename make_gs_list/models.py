from django.db import models

class GoodsService(models.Model):
    class Meta:
        db_table = 'make_gs_list_goodsservice'

    cls = models.CharField(max_length = 2)
    eng = models.CharField(max_length = 100)
    jpn = models.CharField(max_length = 100)
    ruijigun = models.CharField(max_length = 6)
    nice = models.CharField(max_length = 6)

    def __str__(self):
        return u'%s, %s, %s' %(self.cls, self.jpn, self.eng)
