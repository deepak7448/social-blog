from django.db import models
#from.utils import unique_slug_generator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save
from profiles.models import Profiles
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify


# Create your models here.
def custom_slugify(value):
    return default_slugify(value).replace('-', '_')

class Post(models.Model):
    author = models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=50,unique=False)
    #slug = models.SlugField(max_length=50,unique=True)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['title',],
                         slugify=custom_slugify,
                         always_update=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='image/post_image/',blank=True,validators=[FileExtensionValidator(['png','jpg','jpeg','svg'])]) 
    liked = models.ManyToManyField(User,blank=True,related_name="likes")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 

    def get_absolute_url(self):
        return reverse("posts:post_details", kwargs={"slug": self.slug})
    
    def get_like_url(self):
        return reverse("posts:like-toggle", kwargs={"slug": self.slug})

   
    class Meta:
        ordering = ['-created_on','-updated_on',]
        verbose_name = 'Social Post'
        verbose_name_plural = 'Social Post'   

    def comment_count(self):
        return self.postcomment_set.all().count()

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

class Postcomment(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="comment_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField( max_length=50)
    reply = models.ForeignKey('Postcomment',blank=True, null=True, on_delete=models.CASCADE,related_name="replies")
    created_on = models.DateTimeField(auto_now_add=True)
    #updated_on = models.DateTimeField(auto_now=True) 

    class Meta:
        #ordering = ['-id',]
        verbose_name = "Post comment"
        verbose_name_plural = "Post comments"

    def __str__(self):
        return self.comment
        
class feedback(models.Model):
    name = models.CharField(max_length=100,unique=False)
    feedback = models.TextField(max_length=500)

    class Meta:
        verbose_name = ("feedback")
        verbose_name_plural = ("feedbacks")

    def __str__(self):
        return self.feedback

# def post_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
# pre_save.connect(post_pre_save, sender=Post)