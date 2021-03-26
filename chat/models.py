from django.db import models

class ChatApplication(models.Model):
    dtime = models.CharField(max_length=30)
    message = models.CharField(max_length=60)
    names = models.CharField(max_length=60,default='Welcome')
    room = models.CharField(max_length=30)
    fl = models.IntegerField()
    ts = models.CharField(max_length=30)
    chatroom = models.CharField(max_length=30,default='Welcome')
    def __str__(self):
        return self.message
        
