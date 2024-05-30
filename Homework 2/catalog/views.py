from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product, BlogPost
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from catalog.forms import ProductForm


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'{name} ({phone}) написал: {message}')
        return HttpResponseRedirect(self.request.path)


class PostListView(ListView):
    model = BlogPost

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'preview', 'created_at', 'is_published')
    success_url = reverse_lazy('catalog:posts_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'preview', 'created_at', 'is_published')
    success_url = reverse_lazy('catalog:posts_list')

    def get_success_url(self):
        return reverse('catalog:post_detail', args=[self.kwargs.get('pk')])


class PostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:posts_list')
