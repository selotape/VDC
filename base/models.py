from django.db import models

class Desktop(models.Model):

    AMI_CHOICES = (
        ('TT', 'Trusty Tahr'),
        ('SS', 'Saucy Salamander'),
        ('WIN8', 'Windows 8'),
        ('SR', 'Senior'),
    )

    def __unicode__(self):
        return self.name
    name = models.CharField( max_length=50 , primary_key=True)
    owner = models.CharField( max_length=50 , null=True)
    ami = models.CharField( max_length=50 , null=True, choices=AMI_CHOICES, default='TT')
    state = models.CharField( max_length=50 , null=True)
    dns = models.CharField( max_length=50 , null=True)
    creation_date = models.DateTimeField(null=True)
