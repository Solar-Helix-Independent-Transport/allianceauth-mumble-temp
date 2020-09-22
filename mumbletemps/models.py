from django.db import models
from allianceauth.eveonline.models import EveCharacter

# Create your models here.

class TempLink(models.Model):

    expires = models.IntegerField()
    link_ref = models.CharField(max_length=20)
    #active = models.BooleanField(default=True)
    creator = models.ForeignKey(EveCharacter, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        permissions = ( 
            ('create_new_links', 'Can Create Temp Links'), 
        )
    
    def __str__(self):
        return "Link {} - {}".format(self.link_ref, self.expires)


class TempUser(models.Model):
    name = models.CharField(max_length=200) # Display name to show
    username = models.CharField(max_length=20, unique=True) # Username used to login to mumble
    password = models.CharField(max_length=20) # Password used to login to mumble
    expires = models.IntegerField() # timestamp of expiry
    templink = models.ForeignKey(TempLink, on_delete=models.CASCADE, null=True, default=None)
    character_id = models.IntegerField(default=0)
    
    def __str__(self):
        return "Temp User: {} - {}".format(self.username, self.name)
