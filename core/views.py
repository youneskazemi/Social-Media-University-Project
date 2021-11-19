from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import AddPostForm, EditPostForm, AddCommentReplyForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(View):
    form_class = None
    template_name = 'core/home.html'

    def get(self, request):
        return render(request, self.template_name, {'posts': Post.objects.all()})


class UserPost(LoginRequiredMixin, View):
    form_class = AddCommentReplyForm
    template_name = 'core/post.html'

    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, id=post_id, slug=post_slug)
        comments = Comment.objects.filter(post=post, is_reply=False)
        return render(request, self.template_name,
                      {'post': post, 'comments': comments, 'form': self.form_class})

    def post(self, request, post_id, post_slug):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=post_id, slug=post_slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment submitted successfully!", 'success')
            return redirect('core:post', post_id, post_slug)


class AddPost(LoginRequiredMixin, View):
    form_class = AddPostForm
    template_name = 'core/add_post.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Your post added successfully', 'success')
            return redirect("accounts:user_profile", request.user.username)


class DeletePost(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'Your post deleted successfully', 'danger')
        return redirect("accounts:user_profile", request.user.username)


class EditPost(LoginRequiredMixin, View):
    form_class = EditPostForm
    template_name = 'core/edit_post.html'

    def get(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        return render(request, self.template_name,
                      {'form': self.form_class(instance=obj), 'post': obj})

    def post(self, request, post_id):
        obj = get_object_or_404(Post, id=post_id)
        form = self.form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post edited successfully', 'info')
            return redirect("accounts:user_profile", request.user.username)


class Reply(LoginRequiredMixin, View):
    form_class = AddCommentReplyForm

    def post(self, request, post_id, post_slug, comment_id):
        post = get_object_or_404(Post, id=post_id, slug=post_slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.reply = comment
            reply.user = request.user
            reply.post = post
            reply.is_reply = True
            reply.save()
            messages.success(request, "Your reply submitted successfully!", 'success')
            return redirect('core:post', post_id, post_slug)
