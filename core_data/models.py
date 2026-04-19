from django.db import models


class User_Details(models.Model):
    family_no = models.IntegerField()
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_details'
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
        ordering = ['-id']

# saves the data form the kobo toolbox
class Response_table(models.Model):
    metadata = models.JSONField()

    # def __str__(self):
    #     return self.metadata

    class Meta:
        db_table = 'response_table'
        verbose_name = 'Response Table'
        verbose_name_plural = 'Response Tables'
        ordering = ['-id']

    

