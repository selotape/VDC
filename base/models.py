from django.db import models

class Desktop(models.Model):

    AMI_CHOICES = (
        ('Trusty Tahr', 'Trusty Tahr'),
        ('Saucy Salamander', 'Saucy Salamander'),
        ('Windows 8', 'Windows 8'),
    )

    def __unicode__(self):
        return self.name
    name = models.CharField( max_length=50 , primary_key=True)
    owner = models.CharField( max_length=50 )
    ami = models.CharField( max_length=50 , choices=AMI_CHOICES, default='TT')
    state = models.CharField( max_length=50 , default='Running')
    dns = models.CharField( max_length=50 , default='54.84.192.8')
    creation_date = models.DateTimeField(auto_now=True)
