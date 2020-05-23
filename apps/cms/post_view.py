from django.views.generic import View
from .forms import PostForm, PostEditForm
from apps.poster.models import Post, Category, Tag
from apps.peekpauser.models import User
from django.shortcuts import render, redirect, reverse
from utils import restful
import mistune
from django.utils.decorators import method_decorator
from apps.peekpauser.decorators import peekpa_login_required


@method_decorator(peekpa_login_required, name='post')
class PostView(View):
    def post(self, request):
        # 新建提交
        if 'submit' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                author = form.cleaned_data.get('author')
                thumbnail = form.cleaned_data.get('thumbnail')
                status = form.cleaned_data.get('status')
                content = form.cleaned_data.get('content')
                is_md = form.cleaned_data.get('is_md')
                category = form.cleaned_data.get('category')
                priority = form.cleaned_data.get('priority')
                is_hot = form.cleaned_data.get('is_hot')
                is_top = form.cleaned_data.get('is_top')
                is_main_page = form.cleaned_data.get('is_main_page')
                publish_time_show = form.cleaned_data.get('publish_time_show')
                time_id = form.cleaned_data.get('time_id')
                read_num = form.cleaned_data.get('read_num')
                tags = form.cleaned_data.get('tag_id')
                if request.user.is_superuser:
                    instance = Post.objects.create(title=title, description=description, author=author,
                                        thumbnail=thumbnail, status=status, content=content,
                                        is_md=is_md, category=category, priority=priority,
                                        is_hot=is_hot, is_top=is_top, is_main_page=is_main_page,
                                        publish_time_show=publish_time_show, time_id=time_id,read_num=read_num)
                    instance.tag.set(tags)
                return redirect(reverse("cms:post_publish_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改Post
        elif 'modify' in request.POST:
            form = PostEditForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data.get('id')
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                author = form.cleaned_data.get('author')
                thumbnail = form.cleaned_data.get('thumbnail')
                status = form.cleaned_data.get('status')
                content = form.cleaned_data.get('content')
                is_md = form.cleaned_data.get('is_md')
                category = form.cleaned_data.get('category')
                priority = form.cleaned_data.get('priority')
                is_hot = form.cleaned_data.get('is_hot')
                is_top = form.cleaned_data.get('is_top')
                is_main_page = form.cleaned_data.get('is_main_page')
                publish_time_show = form.cleaned_data.get('publish_time_show')
                time_id = form.cleaned_data.get('time_id')
                read_num = form.cleaned_data.get('read_num')
                tags = form.cleaned_data.get('tag_id')
                if request.user.is_superuser:
                    instance = Post.objects.filter(id=id)
                    if is_md:
                        content_html = mistune.markdown(content)
                    instance.update(title=title, description=description, author=author,
                                        thumbnail=thumbnail, status=status, content=content,
                                        is_md=is_md, category=category, priority=priority,
                                        is_hot=is_hot, is_top=is_top, is_main_page=is_main_page,
                                        publish_time_show=publish_time_show, time_id=time_id,read_num=read_num,
                                        content_html=content_html)
                    instance.first().tag.set(tags)
                return redirect(reverse("cms:post_manage_view"))
            else:
                return restful.method_error("Form is error", form.get_errors())
        # 修改状态返回
        elif 'back':
            return redirect(reverse("cms:post_manage_view"))
        # 新建状态的取消
        else:
            return redirect(reverse("cms:post_publish_view"))


@method_decorator(peekpa_login_required, name='get')
class PostEditView(View):
    def get(self, request):
        post_id = request.GET.get('post_id')
        post = Post.objects.get(pk=post_id)
        tag_list = list()
        for item in post.tag.all():
            tag_list.append(item.id)
        context = {
            'item_data': post,
            'list_data_category': Category.objects.all(),
            'list_data_tag': Tag.objects.all(),
            'list_data_user': User.objects.all(),
            'list_data_status': Post.STATUS_ITEMS,
            'item_data_tag_list': tag_list
        }
        return render(request, 'cms/post/publish.html', context=context)


@method_decorator(peekpa_login_required, name='post')
class PostDeleteView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        if request.user.is_superuser:
            Post.objects.filter(id=post_id).update(status=Post.STATUS_DELETE)
        return restful.ok()