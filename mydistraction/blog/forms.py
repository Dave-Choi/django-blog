from django.forms import ModelForm
from models import Post, Author

class PostForm(ModelForm):
    class Meta:
        model = Post
