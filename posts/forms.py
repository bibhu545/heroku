from django import forms
# from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):
	# content = forms.DateField(widget=PagedownWidget(show_preview=False))
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta():
		model = Post
		fields = [
			"title",
			"image",
			"content",
			"draft",
			"publish",
		]
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args,**kwargs)
		self.fields['title'].widget.attrs.update({'class':'form-control'})
		self.fields['title'].widget.attrs.update({'placeholder':'Enter Title'})
		self.fields['image'].widget.attrs.update({'class':'form-control'})
		self.fields['image'].widget.attrs.update({'placeholder':'Choose Image'})
		self.fields['content'].widget.attrs.update({'class':'form-control'})
		self.fields['content'].widget.attrs.update({'placeholder':'Enter Content Here'})
# from django.forms import ModelForm
# from posts.models import Post
# class PostForm(ModelForm):
# 	class Meta:
# 		model = Post
# 		fields = ['title','content']