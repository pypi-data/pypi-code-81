import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from djangoldp.models import Model
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from djangoldp_community.permissions import CommunityPermissions, CommunityCirclePermissions, \
    CommunityProjectPermissions, CommunityJobPermissions, CommunityMembersPermissions, \
    CommunityProfilePermissions
from djangoldp_community.views import CommunityMembersViewset

from djangoldp_circle.models import Circle
from djangoldp_project.models import Project
from djangoldp_joboffer.models import JobOffer

class Community(Model):
    name = models.CharField(max_length=255, blank=True, help_text="Changing a community's name is highly discouraged")
    logo = models.URLField(blank=True, null=True)
    allow_self_registration = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community')
        verbose_name_plural = _("communities")
        permission_classes = [CommunityPermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        superuser_perms = ['view']
        lookup_field = 'slug'
        container_path = "/communities/"
        ordering = ['slug']
        serializer_fields = ['@id', 'name', 'profile', 'addresses', 'logo', 'allow_self_registration',\
                             'projects', 'circles', 'members', 'joboffers']
        rdf_type = "sib:Community"
        depth = 1

class CommunityProfile(Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    shortDescription = models.CharField(max_length=254, blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    phone = models.CharField(max_length=254, blank=True, null=True, default='')
    email = models.EmailField(max_length=254, blank=True, null=True, default='')
    website = models.URLField(blank=True, null=True, default='')
    tweeter = models.URLField(blank=True, null=True, default='')
    facebook = models.URLField(blank=True, null=True, default='')
    linkedin = models.URLField(blank=True, null=True, default='')
    instagram = models.URLField(blank=True, null=True, default='')
    picture1 = models.URLField(blank=True, null=True, default='')
    picture2 = models.URLField(blank=True, null=True, default='')
    picture3 = models.URLField(blank=True, null=True, default='')

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community profile')
        verbose_name_plural = _("community profiles")
        permission_classes = [CommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['view']
        container_path = "community-profiles/"
        serializer_fields = ['@id', 'community', 'shortDescription', 'description', 'phone', 'email', 'website', 'tweeter',\
                             'facebook', 'linkedin', 'instagram', 'picture1', 'picture2', 'picture3']
        rdf_type = "sib:CommunityProfile"

class CommunityAddress(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    address_line1 = models.CharField(max_length=254, blank=True, null=True, default='')
    address_line2 = models.CharField(max_length=254, blank=True, null=True, default='')
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=_("Latitude"))
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name=_("Longitude"))

    def __str__(self):
        try:
            return '{} ({})'.format(self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community address')
        verbose_name_plural = _("community addresses")
        permission_classes = [CommunityProfilePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['view']
        container_path = "community-addresses/"
        serializer_fields = ['@id', 'community', 'address_line1', 'address_line2', 'lat', 'lng']
        rdf_type = "sib:CommunityAddress"

class CommunityMember(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="communities", null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{} -> {} ({})'.format(self.user.urlid, self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community member')
        verbose_name_plural = _("community members")
        view_set = CommunityMembersViewset
        permission_classes = [CommunityMembersPermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit']
        container_path = "community-members/"
        serializer_fields = ['@id', 'community', 'user', 'is_admin']
        rdf_type = "as:items"

class CommunityCircle(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='circles', null=True, blank=True)
    circle = models.OneToOneField(Circle, on_delete=models.CASCADE, related_name="community", null=True, blank=True)

    def __str__(self):
        try:
            return '{} -> {} ({})'.format(self.circle.urlid, self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community circle')
        verbose_name_plural = _("community circles")
        permission_classes = [CommunityPermissions, CommunityCirclePermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit']
        container_path = "community-circles/"
        serializer_fields = ['@id', 'community', 'circle']
        rdf_type = "as:items"

class CommunityProject(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="community", null=True, blank=True)

    def __str__(self):
        try:
            return '{} -> {} ({})'.format(self.project.urlid, self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community project')
        verbose_name_plural = _("community projects")
        permission_classes = [CommunityPermissions, CommunityProjectPermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit']
        container_path = "community-projects/"
        serializer_fields = ['@id', 'community', 'project']
        rdf_type = "as:items"

class CommunityJobOffer(Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='joboffers', null=True, blank=True)
    joboffer = models.OneToOneField(JobOffer, on_delete=models.CASCADE, related_name="community", null=True, blank=True)

    def __str__(self):
        try:
            return '{} -> {} ({})'.format(self.joboffer.urlid, self.community.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _('community job offer')
        verbose_name_plural = _("community job offers")
        permission_classes = [CommunityPermissions, CommunityJobPermissions]
        anonymous_perms = ['view']
        authenticated_perms = ['inherit']
        superuser_perms = ['inherit']
        container_path = "community-joboffers/"
        serializer_fields = ['@id', 'community', 'joboffer']
        rdf_type = "as:items"

@receiver(pre_save, sender=Community)
def pre_create_account(sender, instance, **kwargs):
    if not instance.urlid or instance.urlid.startswith(settings.SITE_URL):
        if getattr(instance, Model.slug_field(instance)) != slugify(instance.name):
            if Community.objects.filter(slug=slugify(instance.name)).count() > 0:
                raise Exception(_("Name already taken"))
            setattr(instance, Model.slug_field(instance), slugify(instance.name))
            setattr(instance, "urlid", "")
    else:
        # Is a distant object, generate a random slug
        setattr(instance, Model.slug_field(instance), uuid.uuid4().hex.upper()[0:8])

@receiver(post_save, sender=Community)
def create_community_profile(instance, created, **kwargs):
    if not Model.is_external(instance):
        CommunityProfile.objects.get_or_create(community=instance)
