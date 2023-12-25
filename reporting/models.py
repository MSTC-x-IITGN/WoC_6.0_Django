from django.db import models
from management.models import Volunteer
import uuid

# Create your models here.

class Report(models.Model):
    reportID = models.UUIDField(primary_key = True,
         default = uuid.uuid4,
         editable = False)
    name = models.CharField(max_length=256)
    description = models.TextField()
    severity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, editable=False) 
    assignee = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=1,
        choices=[
            ('R', 'Reported'),
            ('I', 'In Progress'),
            ('S', 'Solved')
        ]
    )

    class Meta:
        unique_together = ('name','description',)
        
    def __str__(self):
        return self.name


    

