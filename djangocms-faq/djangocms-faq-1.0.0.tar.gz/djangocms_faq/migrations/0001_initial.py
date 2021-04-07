# Generated by Django 2.2 on 2021-04-06 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_faq_faqpluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=300, verbose_name='Titre')),
            ],
            options={
                'verbose_name': 'Faq Container',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100, verbose_name='Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='SearchFaqPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_faq_searchfaqpluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=50, verbose_name='Search name')),
                ('search_in', models.ManyToManyField(limit_choices_to={'placeholder__page__publisher_is_draft': False}, to='djangocms_faq.FaqPluginModel', verbose_name='Search in')),
            ],
            options={
                'verbose_name': 'Faq Search',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='QuestionFaqPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_faq_questionfaqpluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('question', models.CharField(max_length=300, verbose_name='Question')),
                ('slug', models.SlugField(blank=True, default='', help_text='Unique slug for this question. Keep empty to let it be auto-generated.', max_length=300)),
                ('keywords', models.ManyToManyField(to='djangocms_faq.Keyword', verbose_name='Keywords')),
            ],
            options={
                'verbose_name': 'Faq Question',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
