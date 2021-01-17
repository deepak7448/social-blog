from django.contrib import admin
from .models import Post,Postcomment,feedback

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_on','updated_on')
    list_filter = ('title','created_on','updated_on')
    search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}

    class Media:
        js = ("js/tinymce.js",)

class commentAdmin(admin.ModelAdmin):
    list_display = ('id','user','post', 'comment','created_on',)
    list_filter =  ('user', 'comment','created_on',)
    search_fields = ['user']
   
class feedbackAdmin(admin.ModelAdmin):
    list_display = ('id','name','feedback',)
    list_filter =  ('name','feedback',)
    search_fields = ['name']
   
admin.site.register(Postcomment,commentAdmin)
admin.site.register(feedback,feedbackAdmin)