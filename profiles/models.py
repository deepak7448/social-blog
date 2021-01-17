from django.db import models
import datetime 
#from.utils import unique_slug_generator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save
from django_countries.fields import CountryField
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from PIL import Image
#from social.models import Post


def custom_slugify(value):
    return default_slugify(value).replace('-', '_')
# Create your models here.
class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    slug = AutoSlugField(populate_from='user',
                         unique_with=['user',],
                         slugify=custom_slugify,
                         always_update=True)
    profile_pic = models.ImageField(default="profile/male.svg",upload_to='profile/',blank=False,) 
    #cover_pic = models.ImageField(default="cover/background.svg",upload_to='cover/',blank=True,validators=[FileExtensionValidator(['png','jpg','jpeg','svg'])]) 
    bio = models.TextField(max_length = "200",blank=True, null=True)
    country = CountryField(default='IN')
    facebook_url = models.URLField(blank=True,max_length=200)
    instagram_url = models.URLField(blank=True,max_length=200)
    date_of_birth = models.DateField(blank=True, null=True,auto_now=False, auto_now_add=False, default=datetime.date(1997,10,19) )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # def save(self,*args,**kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.profile_pic.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)


    def get_profile_url(self):
        return reverse("profile:Profiles_detail", kwargs={"slug": self.slug})
   
    def all_post(self):
        return self.posts.all().count()

    def __str__(self):
        return str(self.user)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        ordering = ['-created_on',]
        verbose_name = 'Profiles'
        verbose_name_plural = 'Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)

# def post_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
# pre_save.connect(post_pre_save, sender=Profiles)