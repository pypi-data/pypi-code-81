# Generated by Django 2.1.9 on 2019-06-18 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("cms", "0022_auto_20180620_1551")]

    operations = [
        migrations.CreateModel(
            name="HTMLSitemapPage",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="html_sitemap_htmlsitemappage",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "max_depth",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Limit the level of nesting that your sitemap will contain below this page. An empty field or 0 equals to no limit.",
                        null=True,
                        verbose_name="max depth",
                    ),
                ),
                (
                    "in_navigation",
                    models.BooleanField(
                        default=False,
                        help_text="Tick to exclude from sitemap the pages that are excluded from navigation.",
                        verbose_name="in navigation",
                    ),
                ),
                (
                    "include_root_page",
                    models.BooleanField(
                        default=True,
                        help_text="Tick to include the root page and its descendants. Untick to include only its descendants.",
                        verbose_name="include root page",
                    ),
                ),
                (
                    "root_page",
                    models.ForeignKey(
                        blank=True,
                        help_text='This page will be at the root of your sitemap (or its children if the "include root page" flag is unticked).',
                        limit_choices_to={"publisher_is_draft": True},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sitemaps",
                        to="cms.Page",
                        verbose_name="root page",
                    ),
                ),
            ],
            options={
                "verbose_name": "HTML Sitemap",
                "verbose_name_plural": "HTML Sitemaps",
            },
            bases=("cms.cmsplugin",),
        )
    ]
