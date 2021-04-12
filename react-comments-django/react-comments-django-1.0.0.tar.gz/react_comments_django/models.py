# Core django imports
from django.conf import settings
from django import VERSION as DJANGO_VERSION
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models

# Third party imports
from mptt.models import MPTTModel, TreeForeignKey
# we can use following for this
from django.utils.text import slugify
from ipware.ip import get_ip

# Our app imports
from .utils.utility_funcs import gen_uuid, wsi_confidence


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class NamedModel(models.Model):
    class Meta:
        abstract = True

    def get_name(self):
        return self.__class__.__name__


@python_2_unicode_compatible
class Topic(NamedModel):
    # it can be ungiue by titles, but not with urlTitle, example:
    # urlTitle("About page") -> "about-page" and urlTitle("About-page") -> "about-page"
    slug = models.SlugField(unique=True, null=True, max_length=200)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=120, blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.gen_slug(self.title)
        super(Topic, self).save(*args, **kwargs)

    @staticmethod
    def gen_slug(title, try_count=0, unique=True):

        if try_count != 0:
            slug = slugify("{} {}".format(title, try_count))[:180]
        else:
            slug = slugify(title)[:180]

        if not unique:
            return slug

        # try fo find existing Thread
        try:
            Topic.objects.get(slug=slug)
        except Topic.DoesNotExist:
            return slug
        # if topic is exist
        try_count += 1
        return Topic.gen_slug(title, try_count)

    @property
    def url_title(self):
        return self.slug

    @staticmethod
    def get_topic(title):
        return Topic.objects.get(slug=title)


@python_2_unicode_compatible
class Thread(NamedModel):
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(unique=False, max_length=200)
    url = models.URLField(max_length=120, blank=True, default='')
    views = models.IntegerField(blank=True, default=0)
    topic = models.ForeignKey(Topic, related_name='thread', on_delete=models.CASCADE)
    # op - first Post in thread
    op = models.ForeignKey('Post', related_name='+', on_delete=models.CASCADE)
    locked = models.BooleanField(blank=True, default=False)
    is_stickied = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.gen_slug(self.title)
        super(Thread, self).save(*args, **kwargs)

    @staticmethod
    def gen_slug(title):
        return slugify(title)[:180]

    def delete(self, *args, **kwargs):
        try:
            self.op.delete()
        except Post.DoesNotExist:
            pass
        super(Thread, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class Post(MPTTModel, NamedModel):
    uid = models.UUIDField(max_length=8, primary_key=True, default=gen_uuid, editable=False)
    content = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    _upvotes = models.IntegerField(blank=True, default=0)
    _downvotes = models.IntegerField(blank=True, default=0)
    wsi = models.FloatField(blank=True, default=0)  # Wilson score interval
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=150, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        # TODO not so good code / check that wsi saved
        Post.upvotes = property(lambda self: self._upvotes, Post.vote_setter_wrapper('_upvotes'))
        Post.downvotes = property(lambda self: self._downvotes, Post.vote_setter_wrapper('_downvotes'))

    class MPTTMetta:
        order_insertion_by = ['created_on']

    @staticmethod
    def vote_setter_wrapper(attr):
        def vote_setter(self, value):
            setattr(self, attr, max(0, value))
            self.wsi = wsi_confidence(self._upvotes, self._downvotes)
        return vote_setter

    def __str__(self):
        return self.content[:70]

    @property
    def thread(self):  # TODO: thread should be stored in Post
        post = self
        while post.parent:
            post = post.parent
            try:
                return Thread.objects.get(op=post)
            except Thread.DoesNotExist:
                return None

    @property
    def score(self):
        return self.upvotes - self.downvotes

    # add to views
    def set_meta(self, request):
        """update post ip_address & user_agent attributes"""
        ip = get_ip(request)
        if ip is not None:
            self.ip_address = ip
        ua = request.META.get('HTTP_USER_AGENT', '')
        if ua:
            self.user_agent = ua


@receiver(pre_save, sender=Post)
def update_modified_on(sender, instance, *args, **kwargs):
    # try to find saved post due uid is populate with Post init
    instance_exist = True
    try:
        Post.objects.get(uid=instance.uid)
    except Post.DoesNotExist:
        instance_exist = False

    if instance_exist:
        instance.modified_on = timezone.now()


class UserPostVote(NamedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    post = models.ForeignKey(Post, related_name='user_post_votes', on_delete=models.CASCADE)
    val = IntegerRangeField(blank=True, default=0, min_value=-1, max_value=1)


from .meta_badges import *
