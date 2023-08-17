from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

class Base(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    modify = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        

class Machine(Base):
    name = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'Machine'
        verbose_name_plural = 'Machines'
        
    def __str__(self) -> str:
        return self.name
    
    
class Color(Base):
    name = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
        
    def __str__(self) -> str:
        return self.name
    
    
class Order(Base):
    requester = models.ForeignKey(User, on_delete=models.SET('unknown'))
    machine = models.ForeignKey(Machine, on_delete=models.SET('unknown'))
    personalization = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.SET('unknown'))
    STAGE_CHOICE = (('required','Required'), ('production','Production'), ('finished','Finished'))
    stage = models.CharField(max_length=15, choices=STAGE_CHOICE, default=STAGE_CHOICE[0])
    finished = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
    def __str__(self) -> str:
        return f'{self.id} {self.requester}'
    
    def save(self, *args, **kwargs):
        if not self.active and not self.finished:
            self.finished = timezone.now()
            self.stage = 'finished'

        if self.stage == 'finished':
            self.active = False
            self.finished = timezone.now()
        else:
            self.active = True
            self.finished = None

        super(Order, self).save(*args, **kwargs) 