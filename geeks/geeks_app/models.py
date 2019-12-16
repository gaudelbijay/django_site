from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield import JSONField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils.text import slugify


AUDIT_TYPE_CHOICES = (
    (1, 'LOGIN'),
    (2, 'LOGOUT'),
    (3, 'CREATE'),
    (4, 'UPDATE'),
    (5, 'DELETE'),
)

AD_CHOICES = (
    (1, 'BANNER_TOP_FULL'),
    (2, 'BANNER_TOP_HALF'),
    (3, 'HOMEPAGE_BELOW_MENU_FULL'),
    (4, 'HOMEPAGE_BELOW_MENU_HALF'),
    (5, 'HOMEPAGE_ABOVE_BREAKING_FULL'),
    (6, 'HOMEPAGE_ABOVE_BREAKING_HALF'),
    (7, 'HOMEPAGE_BELOW_BREAKING_FULL'),
    (8, 'HOMEPAGE_BELOW_BREAKING_HALF'),
    (9, 'HOMEPAGE_BELOW_HEADLINES_FULL'),
    (10, 'HOMEPAGE_BELOW_HEADLINES_HALF'),
    (11, 'BELOW_CATEGORY_HALF'),
    (12, 'ABOVE_FOOTER_FULL'),
    (13, 'ABOVE_FOOTER_HALF'),

)


FEATURED_TYPE_CHOICES = (
    (1, 'GROUPED'),
    (2, 'FULL WIDTH'),
    (3, 'TITLE'),
)


PHOTO_TYPE_CHOICES = ['jpg', 'png', 'jpeg']


class AuditTrial(models.Model):
    modelType = models.CharField('Model Type', max_length=255)
    objectId = models.IntegerField('Model Obj Id')
    action = models.IntegerField(
        choices=AUDIT_TYPE_CHOICES, default=0, null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(null=True)
    fromObj = JSONField(null=True)
    toObj = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.modelType) + ' ' + str(dict(AUDIT_TYPE_CHOICES)[self.action]) + ' by : ' + str(
            self.user.username)


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, )
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        super().save()


class UserModel(DateTimeModel):
    created_by = models.ForeignKey(User)


class Designation(DateTimeModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# geeks Models


class Category(DateTimeModel):

    name = models.CharField(max_length=40)
    parent = models.ForeignKey(
        'self', related_name="children", null=True, blank=True)
    slug = models.CharField(blank=True, null=True, max_length=150, unique=True)

    def save(self, force_insert=False, using=None):
        if self.slug == None:
            self.slug = slugify(self.name, allow_unicode=True)
        else:
            self.slug = slugify(self.slug, allow_unicode=True)

        super().save()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)


class Author(DateTimeModel):
    name = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = (
            '-priority',
        )

    def __str__(self):
        return str(self.name)


class Post(DateTimeModel):
    '''Need to set default values in fk'''
    category = models.ForeignKey(
        Category, blank=True, null=True, related_name="Category")
    subcategory = models.ManyToManyField(
        Category, blank=True, related_name="Sub_Category")
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    photo = ProcessedImageField(upload_to='gallery_folder/', processors=[ResizeToFit(1000, 500)],
                                format='JPEG', options={'quality': 80}, null=True, blank=True)
    photo_caption = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, blank=True, null=True)

    # rating = models.IntegerField(blank=True, null=True, default=0)
    publish = models.BooleanField(default=False)
    slug = models.CharField(blank=True, null=True, max_length=150, unique=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.title, allow_unicode=True)
        else:
            self.slug = slugify(self.slug, allow_unicode=True)
        super().save()

    def __str__(self):
        return str(self.category) + str(":") + str(self.title)


class Menu(UserModel):
    title = models.CharField(max_length=100)
    position = models.IntegerField(unique=True, null=True, blank=True)
    urls = models.CharField(max_length=100)
    slug = models.CharField(blank=True, null=True, max_length=150, unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='menus')

    class Meta:
        ordering = ["position"]

    def save(self):
        if self.slug == None:
            self.slug = slugify(self.title, allow_unicode=True)
            super().save()
        else:
            self.slug = slugify(self.title, allow_unicode=True)
            super().save()

    def __str__(self):
        return str(self.title)


class NewUser(User, DateTimeModel):

    class Meta:
        verbose_name = "New User"
        verbose_name_plural = "New Users"

    def __str__(self):
        return str(self.username)


'''Advertisement'''

class Advertisement(DateTimeModel):
    title = models.CharField('Title', max_length=50, blank=True, null=True)
    place1 = models.ImageField(null=True, blank=True)
    place2 = models.ImageField(null=True, blank=True)
    ad_type = models.IntegerField(choices=AD_CHOICES, blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    expired_at = models.DateTimeField(blank=True, null=True)
    embedded_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.ad_type) + ":" + str(self.title)
