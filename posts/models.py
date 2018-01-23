from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class Post(models.Model):
	title = models.CharField(max_length=100)
	# slug = models.SlugField(unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE,)
	image = models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False,auto_now_add=False)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	objects = PostManager()

	def get_absolute_url(self):
	    return "/posts/%s/" %(self.id)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
	
	class Meta:
		ordering = ["-timestamp","-updated"]