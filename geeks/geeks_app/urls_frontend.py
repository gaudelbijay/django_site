from django.conf.urls import url

from .views_frontend import *

app_name = 'geeks_frontend'

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^home/python/$', PythonHome.as_view(), name='python_home'),
    url(r'^home/machinelearning/$', MachineLearningHome.as_view(), name='machinelearning_home'),
    url(r'^home/challenges/$', ChallengeHome.as_view(), name='challenge_home'),
    url(r'^post/detail/(?P<pk>\d+)/$',
        FrontendPostDetail.as_view(), name='post_detail'),
    # url(r'^news/category/(?P<slug>[\w-]+)/$',
    #     NewsCategory.as_view(), name='news_category'),
    # url(r'^publishpost/search$',SearchPost.as_view(), name='post_search'),
    # url(r'^publish/search/(?P<searchQuery>.*S+)/$',SearchPost.as_view(), name='post_search'),
    # url(r'^publish/search/(?P<searchQuery>.+)/$',SearchPost.as_view(), name='post_search'),
    # url(r'^publish/search/(?P<searchQuery>\w\s]+)/$',SearchPost.as_view(), name='post_search'),
]
