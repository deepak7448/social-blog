from django import forms
from django.forms import ModelForm
from .models import Post,Postcomment,feedback
#from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin

class PostForm(ModelForm):
  #  content = forms.CharField(widget=CKEditorWidget(attrs={'id':'content', 'placeholder': "What's on your Mind",'autocomplete':'off'}))
    class Meta:
         model = Post
         fields = ['title','content', 'image']

         widgets = {
             'title':forms.TextInput(attrs={'id':'title', 'placeholder': 'Title your Post','autocomplete':'off'}),
             'content':forms.Textarea(attrs={'id':'content', 'placeholder': "Write something here",'autocomplete':'off'})
         }

class PostcommentForm(forms.ModelForm):
    class Meta:
        model = Postcomment
        fields =['comment']

class feedbackForm(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['name','feedback']
        widgets = {
             'name':forms.TextInput(attrs={'id':'name', 'placeholder': 'Enter your name','autocomplete':'off'}),
             'feedback':forms.Textarea(attrs={'id':'feedback', 'placeholder': "Feedback...",'autocomplete':'off'})
         }



