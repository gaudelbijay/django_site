from django.conf.urls import url,include
from django.contrib import admin
from .views import *
# from .views_frontend import CategoricalNewsDetail

app_name='geeks_app'

urlpatterns = [
    url(r'^',include('geeks_app.urls_frontend')),
    url(r'^admin-login/$', AdminLogin.as_view(), name='admin_login'),
    url(r'^admin-logout/$', AdminLogout.as_view(), name='admin_logout'),
    url(r'^admin-panel/$', AdminHomePage.as_view(), name='admin_homepage'),



    ######################### User Section ##########################

    url(r'^user/list/$', ListUser.as_view(), name='user_list'),
    url(r'^create/user/$', RegisterUser.as_view(), name='user_create'),
    url(r'^update/user/(?P<pk>\d+)/$', UpdateUser.as_view(), name='user_update'),
    url(r'^delete/user/(?P<pk>\d+)/$', DeleteUser.as_view(), name='user_delete'),

    url(r'^login/user/$', UserLogin.as_view(), name='user_login'),
    url(r'^logout/user/$', UserLogout.as_view(), name='user_logout'),
    url(r'^password/change/$', ForgotPasswordFormView.as_view(), name='password_change'),
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',ResetPassword.as_view(), name='reset_password'),





    ######################### Designation Part ##########################

    url(r'^designation/list/$', ListDesignation.as_view(), name='designation_list'),
    url(r'^create/designation/$', CreateDesignation.as_view(), name='designation_create'),
    url(r'^update/designation/(?P<pk>\d+)/$', UpdateDesignation.as_view(), name='designation_update'),
    url(r'^delete/designation/(?P<pk>\d+)/$', DeleteDesignation.as_view(), name='designation_delete'),


    #category
    url(r'^category/list/$', ListCategory.as_view(), name='category_list'),
    url(r'^create/category/$', CreateCategory.as_view(), name='category_create'),
    url(r'^update/category/(?P<pk>\d+)/$', UpdateCategory.as_view(), name='category_update'),
    url(r'^delete/category/(?P<pk>\d+)/$', DeleteCategory.as_view(), name='category_delete'),


    ############################  Post ######################################

    url(r'^post/list/$', ListPost.as_view(), name='post_list'),
    url(r'^create/post/$', CreatePost.as_view(), name='post_create'),
    url(r'^update/post/(?P<pk>\d+)/$', UpdatePost.as_view(), name='post_update'),
    url(r'^delete/post/(?P<pk>\d+)/$', DeletePost.as_view(), name='post_delete'),
    url(r'^detail/post/(?P<pk>\d+)/$', DetailPost.as_view(), name='post_detail'),
    url(r'^post/search$',SearchPost.as_view(), name='post_search'),
    url(r'^post/search/(?P<searchQuery>.*S+)/$',SearchPost.as_view(), name='post_search'),
    url(r'^post/search/(?P<searchQuery>.+)/$',SearchPost.as_view(), name='post_search'),
    url(r'^post/search/(?P<searchQuery>\w\s]+)/$',SearchPost.as_view(), name='post_search'),


    ######################### Author ##########################
    url(r'^list/author/$', ListAuthor.as_view(), name='list_author'),
    url(r'^create/author/$', CreateAuthor.as_view(), name='create_author'),
    url(r'^update/author/(?P<pk>\d+)/$', UpdateAuthor.as_view(), name='update_author'),
    url(r'^delete/author/(?P<pk>\d+)/$', DeleteAuthor.as_view(), name='delete_author'),
    url(r'^detail/author/(?P<pk>\d+)/$', DetailAuthor.as_view(), name='detail_author'),


    #######################MENU#######################################
    url(r'^menu/list/$', ListMenu.as_view(), name='menu_list'),
    url(r'^create/menu/$', CreateMenu.as_view(), name='menu_create'),
    url(r'^update/menu/(?P<pk>\d+)/$', UpdateMenu.as_view(), name='menu_update'),
    url(r'^delete/menu/(?P<pk>\d+)/$', DeleteMenu.as_view(), name='menu_delete'),
    url(r'^detail/menu/(?P<pk>\d+)/$', DetailMenu.as_view(), name='menu_detail'),

    ######################################## DRAFT ###############
    url(r'^draft/list/$', ListPostDraft.as_view(), name='postdraft_list'),
    url(r'^delete/postdraft/(?P<pk>\d+)/$', DeletePostDraft.as_view(), name='postdraft_delete'),
    url(r'^detail/postdraft/(?P<pk>\d+)/$', DetailPostDraft.as_view(), name='postdraft_detail'),
    url(r'^update/postdraft/(?P<pk>\d+)/$', UpdatePostDraft.as_view(), name='postdraft_update'),
    # url(r'^create/menu/$', CreatePostDraft.as_view(), name='Postdraft_create'),
    
    
    ######################################## Published Post ###############
    url(r'^publishedpost/list/$', ListPublishedPost.as_view(), name='publishedpost_list'),
    url(r'^delete/publishedpost/(?P<pk>\d+)/$', DeletePublishedPost.as_view(), name='publishedpost_delete'),
    url(r'^detail/publishedpost/(?P<pk>\d+)/$', DetailPublishedPost.as_view(), name='publishedpost_detail'),
    url(r'^update/publishedpost/(?P<pk>\d+)/$', UpdatePublishedPost.as_view(), name='publishedpost_update'),
    url(r'^publish/(?P<publish_id>\d+)/$', PublishPost.as_view(), name='publish_post'),

    url(r'^publish/(?P<publish_id>\d+)/$', PublishPost.as_view(), name='publish_post'),
    url(r'^unpublish/(?P<publish_id>\d+)/$', UnPublishPost.as_view(), name='unpublish_post'),

    #############################Advertisement###############################

    url(r'^list/advertisement/$', ListAdvertisement.as_view(), name='list_advertisement'),
    url(r'^create/advertisement/$', CreateAdvertisement.as_view(), name='create_advertisement'),
    url(r'^update/advertisement/(?P<pk>\d+)/$', UpdateAdvertisement.as_view(), name='update_advertisement'),
    url(r'^delete/advertisement/(?P<pk>\d+)/$', DeleteAdvertisement.as_view(), name='delete_advertisement'),
    url(r'^detail/advertisement/(?P<pk>\d+)/$', DetailAdvertisement.as_view(), name='detail_advertisement'),

    #url(r'^post/(?P<slug>[\w-]+)/$', CategoricalPostDetail.as_view(), name='list_categoricalPost'),


]
