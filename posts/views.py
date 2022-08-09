from django.views.generic import ListView
from posts import models


class PostList(ListView):
    model = models.Post
    context_object_name = "posts"
