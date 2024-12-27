from django import forms
from posts.models import Category, Post

class Post_Form(forms.Form):
    image =forms.ImageField()
    title = forms.CharField()
    content = forms.CharField()
    rate = forms.CharField()
    
    def clean(self):
        data = super().clean()
        title = data.get("title")
        content = data.get("content")
        if title.lower() == content.lower():
            raise forms.ValidationError("Title and content must be different")
        return data
    
class SearchForm(forms.Form):
    search = forms.CharField(
    required = False,
    max_length = 100,

    widget=forms.TextInput(attrs={"placeholder":"Поиск", "class": "form-control"}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
       required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    orderings =  (
        ("title", "По названию"),
        ("content", "По контенту"),
        ("create_at", "По дате создания"),
        ("update_at", "По дате обновления"),
        ("rate", "По рейтингу"),
        
        ("-title", "По названию (убыв.)"),
        ("-content", "По контенту (убыв.)"),
        ("-create_at", "По дате создания (убыв.)"),
        ("-update_at", "По дате обновления (убыв.)"),
        ("-rate", "По рейтингу (убыв.)"),
    )
    ordering = forms.ChoiceField(
        choices=orderings, required=False,
        widget=forms.Select(attrs={"class": "form-control"}))

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]