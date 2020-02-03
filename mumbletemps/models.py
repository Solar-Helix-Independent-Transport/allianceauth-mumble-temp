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
