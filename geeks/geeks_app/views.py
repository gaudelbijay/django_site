from .forms import *
from .models import *
from .mixins import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from geeks_app.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from urllib.parse import quote_plus

# STATE_CHOICES = dict(NEWS_STATE_CHOICES)

'''Admin Section'''


class AdminHomePage(EmployeeRequiredMixin, TemplateView):
    template_name = 'geeks_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        return context


class AdminLogin(TemplateView):
    template_name = 'geeks_app/account/login.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            form = LoginForm()
            print(user)
            print('form valid')
            if user is not None:
                if user.is_active:
                    print('user is active')
                    login(request, user)
                    return HttpResponseRedirect('/admin-panel/')
            else:
                print('else')
                # raise forms.ValidationError("Invalid Username or  Password")

                return HttpResponseRedirect('/admin-login')

    def get_context_data(self):
        context = super(AdminLogin, self).get_context_data()
        form = LoginForm()
        context['form'] = form
        return context


class AdminLogout(AuthMixin, TemplateView):
    template_name = 'geeks_app/account/logout.html'

    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/admin-login/')


'''User Section'''


class ListUser(AuthMixin, ListMixin):
    template_name = 'geeks_app/user/list_user.html'
    model = NewUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'newuser'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class RegisterUser(AuthMixin, CreateMixin):

    template_name = 'geeks_app/user/create_user.html'
    model = NewUser
    form_class = SignUpForm
    success_url = reverse_lazy('geeks_app:user_list')


    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.username = form.cleaned_data.get('email')
        email = obj.username
        obj.first_name = form.cleaned_data.get('first_name')
        obj.last_name = form.cleaned_data.get('last_name')
        password = User.objects.make_random_password()

        message = "Dear, " + obj.first_name + " " + obj.last_name + \
            " your username is: " + obj.username + "\n Password:" + password
        obj.set_password(password)
        obj.save()

        send_mail('Your Account has been created!', message,
                  settings.EMAIL_HOST_USER, [email], fail_silently=False)
        message = str(str(obj.username) + " Created Successfully")
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = NewUser.objects.filter(
            deleted_at__isnull=True).count() < 15
        context['url_name'] = 'newuser'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateUser(AuthMixin, UpdateMixin):
    template_name = 'geeks_app/user/create_user.html'
    model = NewUser
    form_class = SignUpForm
    success_url = reverse_lazy('geeks_app:user_list')

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.username = form.cleaned_data.get('email')
        email = obj.username
        obj.first_name = form.cleaned_data.get('first_name')
        obj.last_name = form.cleaned_data.get('last_name')
        password = User.objects.make_random_password()

        message = "Dear, " + obj.first_name + " " + obj.last_name + \
            " your username is: " + obj.username + "\n Password:" + password
        obj.set_password(password)
        obj.save()
        message = str(str(obj.username) + " Created Successfully")
        send_mail('Your Account has been created!', message,
                  settings.EMAIL_HOST_USER, [email])
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = NewUser.objects.filter(
            deleted_at__isnull=True).count() < 15
        context['url_name'] = 'newuser'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteUser(AuthMixin, DeleteMixin):
    template_name = 'geeks_app/user/delete_user.html'
    model = NewUser
    success_url = reverse_lazy('geeks_app:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'newuser'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UserLogin(TemplateView):
    template_name = 'geeks_app/user/login_user.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(user)
            print('form valid')
            if user is not None:
                if user.is_active:
                    print('user is active')
                    login(request, user)
                    return HttpResponseRedirect('/admin-panel/')
            else:
                print('else')
                # raise forms.ValidationError("Invalid Username or  Password")

                return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self):
        context = super().get_context_data()
        form = LoginForm()
        context['form'] = form
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UserLogout(EmployeeRequiredMixin, TemplateView):
    template_name = 'geeks_app/user/logout_user.html'

    def post(self, request):
        logout(request)
        return HttpResponseRedirect('/login/user/')


class ForgotPasswordFormView(View):
    template_name = 'home/pwdresetform.html'

    # def get(self, request, *args, **kwargs):
    #     form = ForgotPasswordForm()
    #
    # return render(request, 'geeks_app/user/login_user.html', {'form':
    # form})

    def post(self, request, *args, **kwargs):

        form = ForgotPasswordForm(request.POST)
        if form.is_valid():

            to_email = form.cleaned_data['email']
            user = User.objects.get(email=to_email)
            primarykey = user.id
            current_site = get_current_site(request)
            subject = 'Passwor Reset !!'
            message = render_to_string('geeks_app/user/newpasswordlink.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(primarykey)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
        return render(request, 'geeks_app/user/sendmail.html')


class ResetPassword(View):

    def get(self, request, uidb64, token):
        form = NewPassword()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):

            return render(request, 'geeks_app/user/newpasswordcreate.html', {'form': form})
        else:
            return render(request, 'geeks_app/user/account_activation_invalid.html')

    def post(self, request, uidb64, token):

        form = NewPassword(request.POST)
        if form.is_valid():
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']
            if pass1 != pass2:
                return render(request, 'geeks_app/user/passwordnotmatch.html')
            else:
                print(user.id)
                user.set_password(pass1)
                user.save()
                # return HttpResponse('complete password verification!!')
                return render(request, 'geeks_app/user/success.html')


'''Designation Part'''


class ListDesignation(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/designation/list_designation.html'
    model = Designation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'designation'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class CreateDesignation(EmployeeRequiredMixin, CreateMixin):
    template_name = 'geeks_app/designation/create_designation.html'
    model = Designation
    form_class = DesignationForm
    success_url = reverse_lazy('geeks_app:designation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'designation'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateDesignation(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/designation/create_designation.html'
    model = Designation
    form_class = DesignationForm
    success_url = reverse_lazy('geeks_app:designation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'designation'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteDesignation(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/designation/delete_designation.html'
    model = Designation
    success_url = reverse_lazy('geeks_app:designation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'designation'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context



'''Author Part'''


class ListAuthor(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/author/list_author.html'
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'author'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class CreateAuthor(EmployeeRequiredMixin, CreateMixin):
    template_name = 'geeks_app/author/create_author.html'
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('geeks_app:list_author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'author'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateAuthor(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/author/create_author.html'
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('geeks_app:list_author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'author'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteAuthor(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/author/delete_author.html'
    model = Author
    success_url = reverse_lazy('geeks_app:list_author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'author'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailAuthor(EmployeeRequiredMixin, DetailView):
    template_name = 'geeks_app/author/detail_author.html'
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'Post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()

        return context


'''Category'''
class CreateCategory(EmployeeRequiredMixin, CreateMixin):
    model = Category
    template_name = 'geeks_app/category/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('geeks_app:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'category'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()

        return context


class ListCategory(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/category/list_category.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'category'
        # context['subcategories'] = SubCategory.objects.filter(deleted_at__isnull=True)
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateCategory(EmployeeRequiredMixin, UpdateMixin):
    model = Category
    template_name = 'geeks_app/category/create_category.html'
    form_class = CategoryForm

    success_url = reverse_lazy('geeks_app:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'category'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteCategory(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/category/delete_category.html'
    model = Category
    success_url = reverse_lazy('geeks_app:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'category'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context



##############################Menu###############################

class ListMenu(EmployeeRequiredMixin, ListMixin):
    template_name = "geeks_app/menu/list_menu.html"
    model = Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'menu'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailMenu(EmployeeRequiredMixin, DetailView):
    template_name = "geeks_app/menu/detail_menu.html"
    model = Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'menu'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class CreateMenu(EmployeeRequiredMixin, CreateMixin):
    model = Category
    template_name = 'geeks_app/menu/create_menu.html'
    form_class = MenuForm
    success_url = reverse_lazy('geeks_app:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['url_name'] = 'menu'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateMenu(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/menu/create_menu.html'
    model = Menu
    form_class = FormMenu
    success_url = reverse_lazy('geeks_app:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = "menu"
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteMenu(EmployeeRequiredMixin, DeleteMixin):
    template_name = "geeks_app/menu/delete_menu.html"
    model = Menu
    success_url = reverse_lazy('geeks_app:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = "menu"
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context

    ###############################Menu ENd###################################


''' Post part '''


class ListPost(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/post/list_post.html'
    model = Post
    paginate_by = 10

    def get_paginate_by(self, queryset):
        if self.request.GET.get('paginate_by') is not None:
            self.paginate_by = self.request.GET.get('paginate_by')
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        if self.request.GET.get('paginate_by') is not None:
            self.paginate_by = self.request.GET.get('paginate_by')

        context['paginate_by'] = self.paginate_by
        return context


class CreatePost(EmployeeRequiredMixin, CreateMixin):
    template_name = 'geeks_app/post/create_post.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('geeks_app:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdatePost(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/post/create_post.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('geeks_app:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeletePost(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/post/delete_post.html'
    model = Post
    success_url = reverse_lazy('geeks_app:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailPost(EmployeeRequiredMixin, DetailView):
    template_name = 'geeks_app/post/detail_post.html'
    model = Post 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class SearchPost(EmployeeRequiredMixin, TemplateView):

    def post(self, request):
        search_text = request.POST.get('searchtext', None)

        if search_text is not None and search_text != u"":
            search_post = Post.objects.filter(
                title__icontains=search_text, deleted_at__isnull=True).values().order_by('-created_at')
        else:
            search_post = []

        return render_to_response('geeks_app/post/search.html', {'search_post': search_post})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


####################DraftView#############################


class ListPostDraft(EmployeeRequiredMixin, ListMixin):

    template_name = 'geeks_app/postdraft/list_postdraft.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True, publish=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'postdraft'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdatePostDraft(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/postdraft/update_postdraft.html'
    model = Post
    form_class = PostDraftForm
    success_url = reverse_lazy('geeks_app:postdraft_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'postdraft'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeletePostDraft(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/postdraft/delete_postdraft.html'
    model = Post
    success_url = reverse_lazy('geeks_app:postdraft_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'post'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailPostDraft(EmployeeRequiredMixin, DetailView):
    template_name = 'geeks_app/postdraft/detail_postdraft.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'postdraft'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()

        return context


class PublishPost(EmployeeRequiredMixin, TemplateView):
    template_name = 'geeks_app/postdraft/list_postdraft.html'
    model = Post

    def post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['publish_id'])
        post.publish = True
        post.save()
        messages.success = "Successfully Published"
        return redirect('geeks_app:postdraft_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postdraft'] = Post.objects.filter(deleted_at__isnull=True)
        context['url_name'] = 'postdraft'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()

        return context



#############################Published Post################################


class ListPublishedPost(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/publishedpost/list_publishedpost.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(deleted_at__isnull=True, publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'publishedpost'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailPublishedPost(EmployeeRequiredMixin, DetailView):
    template_name = 'geeks_app/publishedPost/detail_publishedpost.html'
    model = Post
    success_url = reverse_lazy('geeks_app:publishedpost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'publishedpost'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdatePublishedPost(EmployeeRequiredMixin, UpdateMixin):

    template_name = 'geeks_app/publishedpost/update_publishedpost.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('geeks_app:publishedPost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Postdraft'] = Post.objects.filter(deleted_at__isnull=True)
        context['url_name'] = 'publishedpost'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeletePublishedPost(EmployeeRequiredMixin, DeleteMixin):

    template_name = 'geeks_app/publishedpost/delete_publishedpost.html'
    model = Post
    success_url = reverse_lazy('geeks_app:publishedpost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'publishedpost'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UnPublishPost(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/Postdraft/list_postdraft.html'
    model = Post

    def post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['publish_id'])
        post.publish = False
        # post.__setattr__(self,publish , True)
        post.save()
        messages.success = 'Post Removed from Published !!'

        return redirect('geeks_app:publishedpost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'publishedpost'
        context['postdraft'] = Post.objects.filter(deleted_at__isnull=True)
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context



################### Advertisment ######################


class ListAdvertisement(EmployeeRequiredMixin, ListMixin):
    template_name = 'geeks_app/advertisement/list_advertisement.html'
    model = Advertisement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'advertisement'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class CreateAdvertisement(EmployeeRequiredMixin, CreateMixin):
    template_name = 'geeks_app/advertisement/update_advertisement.html'
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('geeks_app:list_advertisement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'advertisement'
        context['Post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class UpdateAdvertisement(EmployeeRequiredMixin, UpdateMixin):
    template_name = 'geeks_app/advertisement/update_advertisement.html'
    model = Advertisement
    form_class = AdvertisementForm
    success_url = reverse_lazy('geeks_app:list_advertisement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'advertisement'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DeleteAdvertisement(EmployeeRequiredMixin, DeleteMixin):
    template_name = 'geeks_app/advertisement/delete_advertisement.html'
    model = Advertisement
    success_url = reverse_lazy('geeks_app:list_advertisement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'advertisement'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


class DetailAdvertisement(EmployeeRequiredMixin, DetailView):
    template_name = 'geeks_app/advertisement/detail_advertisement.html'
    model = Advertisement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'advertisement'
        context['post_draft'] = Post.objects.filter(
            deleted_at__isnull=True, publish=False).count()
        context['publish_post'] = Post.objects.filter(
            deleted_at__isnull=True, publish=True).count()
        return context


################### End of Advertisment ######################
