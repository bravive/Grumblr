from django.db import models
# Create your models here.
from django.contrib.auth.models import User
# Register your models here.


class Grumbls(models.Model):
    text = models.CharField(max_length=400)
    user = models.ForeignKey(User)
    dislike_user = models.ManyToManyField(User,related_name='dislike_map')
    entry_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.text
        
class Comment(models.Model):
    text = models.CharField(max_length=400)
    item = models.ForeignKey(Grumbls)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

class UserRelationship(models.Model):
    user = models.OneToOneField(User,related_name='username_map', primary_key=True)
    followings = models.ManyToManyField(User,related_name='follow_map')
    blockings = models.ManyToManyField(User,related_name='block_map')
    def __unicode__(self):
        return self.user.username

class Entry(models.Model):
    owner = models.OneToOneField(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address_1 = models.CharField(max_length=200, default="", blank=True)
    address_2 = models.CharField(max_length=200, default="", blank=True)
    city = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(max_length=200, default="", blank=True)
    zip = models.CharField(max_length=200, default="", blank=True)
    country = models.CharField(max_length=200, default="", blank=True)
    phone = models.CharField(max_length=200, default="", blank=True)
    picture = models.ImageField(upload_to="addr-book-photos", blank=True)
    
    def __unicode__(self):
	return self.first_name + " " + self.last_name

    @staticmethod
    def get_entries(owner):
        return Entry.objects.filter(owner=owner).order_by('last_name', 'first_name')
    


    




