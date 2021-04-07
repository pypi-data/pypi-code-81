# Generated by Django 2.1.7 on 2019-03-26 09:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import filer.fields.image
import parler.models

import richie.apps.core.fields.multiselect
import richie.apps.core.models
import richie.apps.courses.models.category


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
                (
                    "public_extension",
                    models.OneToOneField(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_extension",
                        to="courses.BlogPost",
                    ),
                ),
            ],
            options={
                "verbose_name": "blog post",
                "db_table": "richie_blog_post",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="BlogPostPluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_blogpostpluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        limit_choices_to={
                            "blogpost__isnull": False,
                            "publisher_is_draft": True,
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blogpost_plugins",
                        to="cms.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "blog post plugin",
                "db_table": "richie_blog_post_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
                (
                    "public_extension",
                    models.OneToOneField(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_extension",
                        to="courses.Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "db_table": "richie_category",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="CategoryPluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_categorypluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        limit_choices_to=richie.apps.courses.models.category.get_category_limit_choices_to,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_plugins",
                        to="cms.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "category plugin",
                "db_table": "richie_category_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
                (
                    "public_extension",
                    models.OneToOneField(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_extension",
                        to="courses.Course",
                    ),
                ),
            ],
            options={"verbose_name": "course", "db_table": "richie_course"},
        ),
        migrations.CreateModel(
            name="CoursePluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_coursepluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        limit_choices_to={
                            "course__isnull": False,
                            "node__parent__cms_pages__course__isnull": True,
                            "node__parent__cms_pages__publisher_is_draft": True,
                            "publisher_is_draft": True,
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_plugins",
                        to="cms.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "course plugin",
                "db_table": "richie_course_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="CourseRun",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "resource_link",
                    models.URLField(
                        blank=True, null=True, verbose_name="Resource link"
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="course start"
                    ),
                ),
                (
                    "end",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="course end"
                    ),
                ),
                (
                    "enrollment_start",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="enrollment start"
                    ),
                ),
                (
                    "enrollment_end",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="enrollment end"
                    ),
                ),
                (
                    "languages",
                    richie.apps.core.fields.multiselect.MultiSelectField(
                        choices=[
                            ("af", "Afrikaans"),
                            ("ar", "Arabic"),
                            ("ast", "Asturian"),
                            ("az", "Azerbaijani"),
                            ("bg", "Bulgarian"),
                            ("be", "Belarusian"),
                            ("bn", "Bengali"),
                            ("br", "Breton"),
                            ("bs", "Bosnian"),
                            ("ca", "Catalan"),
                            ("cs", "Czech"),
                            ("cy", "Welsh"),
                            ("da", "Danish"),
                            ("de", "German"),
                            ("dsb", "Lower Sorbian"),
                            ("el", "Greek"),
                            ("en", "English"),
                            ("en-au", "Australian English"),
                            ("en-gb", "British English"),
                            ("eo", "Esperanto"),
                            ("es", "Spanish"),
                            ("es-ar", "Argentinian Spanish"),
                            ("es-co", "Colombian Spanish"),
                            ("es-mx", "Mexican Spanish"),
                            ("es-ni", "Nicaraguan Spanish"),
                            ("es-ve", "Venezuelan Spanish"),
                            ("et", "Estonian"),
                            ("eu", "Basque"),
                            ("fa", "Persian"),
                            ("fi", "Finnish"),
                            ("fr", "French"),
                            ("fy", "Frisian"),
                            ("ga", "Irish"),
                            ("gd", "Scottish Gaelic"),
                            ("gl", "Galician"),
                            ("he", "Hebrew"),
                            ("hi", "Hindi"),
                            ("hr", "Croatian"),
                            ("hsb", "Upper Sorbian"),
                            ("hu", "Hungarian"),
                            ("ia", "Interlingua"),
                            ("id", "Indonesian"),
                            ("io", "Ido"),
                            ("is", "Icelandic"),
                            ("it", "Italian"),
                            ("ja", "Japanese"),
                            ("ka", "Georgian"),
                            ("kab", "Kabyle"),
                            ("kk", "Kazakh"),
                            ("km", "Khmer"),
                            ("kn", "Kannada"),
                            ("ko", "Korean"),
                            ("lb", "Luxembourgish"),
                            ("lt", "Lithuanian"),
                            ("lv", "Latvian"),
                            ("mk", "Macedonian"),
                            ("ml", "Malayalam"),
                            ("mn", "Mongolian"),
                            ("mr", "Marathi"),
                            ("my", "Burmese"),
                            ("nb", "Norwegian Bokmål"),
                            ("ne", "Nepali"),
                            ("nl", "Dutch"),
                            ("nn", "Norwegian Nynorsk"),
                            ("os", "Ossetic"),
                            ("pa", "Punjabi"),
                            ("pl", "Polish"),
                            ("pt", "Portuguese"),
                            ("pt-br", "Brazilian Portuguese"),
                            ("ro", "Romanian"),
                            ("ru", "Russian"),
                            ("sk", "Slovak"),
                            ("sl", "Slovenian"),
                            ("sq", "Albanian"),
                            ("sr", "Serbian"),
                            ("sr-latn", "Serbian Latin"),
                            ("sv", "Swedish"),
                            ("sw", "Swahili"),
                            ("ta", "Tamil"),
                            ("te", "Telugu"),
                            ("th", "Thai"),
                            ("tr", "Turkish"),
                            ("tt", "Tatar"),
                            ("udm", "Udmurt"),
                            ("uk", "Ukrainian"),
                            ("ur", "Urdu"),
                            ("vi", "Vietnamese"),
                            ("zh-hans", "Simplified Chinese"),
                            ("zh-hant", "Traditional Chinese"),
                        ],
                        help_text="The list of languages in which the course content is available.",
                        max_choices=50,
                        max_length=255,
                    ),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
                (
                    "public_extension",
                    models.OneToOneField(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_extension",
                        to="courses.CourseRun",
                    ),
                ),
            ],
            options={"verbose_name": "course run", "db_table": "richie_course_run"},
        ),
        migrations.CreateModel(
            name="Licence",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "url",
                    models.CharField(blank=True, max_length=255, verbose_name="url"),
                ),
                ("content", models.TextField(default="", verbose_name="content")),
                (
                    "logo",
                    filer.fields.image.FilerImageField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="licence",
                        to=settings.FILER_IMAGE_MODEL,
                        verbose_name="logo",
                    ),
                ),
            ],
            options={"verbose_name": "licence", "db_table": "richie_licence"},
        ),
        migrations.CreateModel(
            name="LicencePluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_licencepluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "licence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.Licence",
                    ),
                ),
            ],
            options={
                "verbose_name": "licence plugin",
                "db_table": "richie_licence_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=100,
                        null=True,
                        verbose_name="code",
                    ),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
                (
                    "public_extension",
                    models.OneToOneField(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_extension",
                        to="courses.Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization",
                "db_table": "richie_organization",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="OrganizationPluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_organizationpluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        limit_choices_to={
                            "organization__isnull": False,
                            "publisher_is_draft": True,
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_plugins",
                        to="cms.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization plugin",
                "db_table": "richie_organization_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=200, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=200, verbose_name="Last name"),
                ),
                (
                    "extended_object",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
            ],
            options={"verbose_name": "person", "db_table": "richie_person"},
        ),
        migrations.CreateModel(
            name="PersonPluginModel",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="courses_personpluginmodel",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        limit_choices_to={
                            "person__isnull": False,
                            "publisher_is_draft": True,
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cms.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "person plugin",
                "db_table": "richie_person_plugin",
            },
            bases=("cms.cmsplugin",),
        ),
        migrations.CreateModel(
            name="PersonTitle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
            options={"verbose_name": "person title", "db_table": "richie_person_title"},
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PersonTitleTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Title")),
                (
                    "abbreviation",
                    models.CharField(max_length=10, verbose_name="Title abbreviation"),
                ),
                (
                    "master",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="courses.PersonTitle",
                    ),
                ),
            ],
            options={
                "verbose_name": "person title translation",
                "db_table": "richie_person_title_translation",
            },
        ),
        migrations.AddField(
            model_name="person",
            name="person_title",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="persons",
                to="courses.PersonTitle",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="public_extension",
            field=models.OneToOneField(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="draft_extension",
                to="courses.Person",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="persontitletranslation", unique_together={("language_code", "master")}
        ),
    ]
