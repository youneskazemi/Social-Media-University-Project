from django.shortcuts import render, redirect
from django.views import View
from .forms import AddPostForm
from django.utils.text import slugify
from django.contrib import messages


class Home(View):
    form_class = None
    template_name = 'core/home.html'

    def get(self, request):
        return render(request, self.template_name)


class AddPost(View):
    form_class = AddPostForm
    template_name = 'core/add_post.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Your post added successfully', 'success')
            return redirect('core:home')
