from django.db import models

class Desktop(models.Model):

    def __unicode__(self):
        return self.name
#   student_id = models.IntegerField( primary_key=True )
#   country = models.CharField( max_length=50 )
#   city = models.CharField( max_length=50 )
#   name = models.CharField( max_length=50 )
#   age = models.IntegerField( max_length=2 )
#   faculty = models.CharField( max_length=50 )
#   photo_url = models.CharField( max_length=200 )
    name = models.CharField( max_length=50 , primary_key=True)
    owner = models.CharField( max_length=50 , null=True)
    ami = models.CharField( max_length=50 , null=True)
    state = models.CharField( max_length=50 , null=True)
    dns = models.CharField( max_length=50 , null=True)
    creation_date = models.DateTimeField(null=True)
