import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
# Create your views here.
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from newsportal.filters import PostFilter
from newsportal.forms import NewsForm
from newsportal.models import Post, Category, Subscriber, Author
from .permissions import ReadOnly
from .serializers import PostSerializer
from .tasks import hello
from django.utils.translation import gettext as _

class NewsListView(ListView):
    model = Post
    template_name = 'news_all.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
class NewsDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news_single.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class NewsSearchView(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


# дженерик для удаления товара
class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required = ('newsportal.add_post', 'newsportal.change_post')

    def post(self, request, *args, **kwargs):
        new_post = Post(
            type_of_post=request.POST.get('type_of_post'),
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            author=Author.objects.get(pk=request.POST['author']),
        )
        new_post.save()

        categories_selected = request.POST.getlist('category')
        print(categories_selected, 'categories_selected')

        for category in categories_selected:
            print(category, 'category')

            category_get = Category.objects.get(pk=category)

            new_post.category.add(category_get)

        return redirect('/')


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = NewsForm
    permission_required = ('newsportal.add_post', 'newsportal.change_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe_me_category(request, slug):
    category_find = get_object_or_404(Category, category=slug)
    user = request.user
    Subscriber.objects.create(user=user, category=category_find)
    return redirect('/')


class Hello_view(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


class Index(View):
    def get(self, request):
        string = _('Hello world')
        return HttpResponse(string)



class NewsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Post.objects.filter(type_of_post='NW')
    serializer_class = PostSerializer



class ArticlesViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Post.objects.filter(type_of_post='AL')
    serializer_class = PostSerializer


