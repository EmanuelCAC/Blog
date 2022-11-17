from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from blog.models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from blog.forms import PostModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    # return HttpResponse('Olá Django - index')
    return TemplateResponse(request, 'index.html', {})

def ola(request):
    # return HttpResponse('Olá Django')
    posts = Post.objects.all()
    return TemplateResponse(request, 'posts.html', {'posts_list': posts })

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/detail.html', {'post': post})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/create.html'
    success_url = reverse_lazy('posts_list')
    form_class = PostModelForm

    def form_invalid(self, form):
        messages.warning(
            self.request,
            'O Post não foi salvo. Verifique e tente novamente'
        )
        return super(PostCreateView, self).form_invalid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_form.html'
    success_url = reverse_lazy('posts_list')
    form_class = PostModelForm

    def form_invalid(self, form):
        messages.warning(
            self.request,
            'O Post não foi salvo. Verifique e tente novamente'
        )
        return super(UpdateView, self).form_invalid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('posts_list')
    success_message = 'Post excluído com sucesso.'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)
