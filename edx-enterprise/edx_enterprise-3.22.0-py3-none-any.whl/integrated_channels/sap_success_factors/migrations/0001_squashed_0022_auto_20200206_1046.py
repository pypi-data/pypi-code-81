# Generated by Django 2.2.12 on 2020-04-21 18:57

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('sap_success_factors', '0001_initial'), ('sap_success_factors', '0002_auto_20170224_1545'), ('sap_success_factors', '0003_auto_20170317_1402'), ('sap_success_factors', '0004_catalogtransmissionaudit_audit_summary'), ('sap_success_factors', '0005_historicalsapsuccessfactorsenterprisecustomerconfiguration_history_change_reason'), ('sap_success_factors', '0006_sapsuccessfactors_use_enterprise_enrollment_page_waffle_flag'), ('sap_success_factors', '0007_remove_historicalsapsuccessfactorsenterprisecustomerconfiguration_history_change_reason'), ('sap_success_factors', '0008_historicalsapsuccessfactorsenterprisecustomerconfiguration_history_change_reason'), ('sap_success_factors', '0009_sapsuccessfactors_remove_enterprise_enrollment_page_waffle_flag'), ('sap_success_factors', '0010_move_audit_tables_to_base_integrated_channel'), ('sap_success_factors', '0011_auto_20180104_0103'), ('sap_success_factors', '0012_auto_20180109_0712'), ('sap_success_factors', '0013_auto_20180306_1251'), ('sap_success_factors', '0014_drop_historical_table'), ('sap_success_factors', '0015_auto_20180510_1259'), ('sap_success_factors', '0016_sapsuccessfactorsenterprisecustomerconfiguration_additional_locales'), ('sap_success_factors', '0017_sapsuccessfactorsglobalconfiguration_search_student_api_path'), ('sap_success_factors', '0018_sapsuccessfactorsenterprisecustomerconfiguration_show_course_price'), ('sap_success_factors', '0019_auto_20190925_0730'), ('sap_success_factors', '0020_sapsuccessfactorsenterprisecustomerconfiguration_catalogs_to_transmit'), ('sap_success_factors', '0021_sapsuccessfactorsenterprisecustomerconfiguration_show_total_hours'), ('sap_success_factors', '0022_auto_20200206_1046')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enterprise', '0094_add_use_enterprise_catalog_sample'),
    ]

    operations = [
        migrations.CreateModel(
            name='SapSuccessFactorsLearnerDataTransmissionAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sapsf_user_id', models.CharField(max_length=255)),
                ('enterprise_course_enrollment_id', models.PositiveIntegerField(db_index=True)),
                ('course_id', models.CharField(max_length=255)),
                ('course_completed', models.BooleanField(default=True)),
                ('instructor_name', models.CharField(blank=True, max_length=255)),
                ('grade', models.CharField(max_length=100)),
                ('total_hours', models.FloatField(blank=True, null=True)),
                ('completed_timestamp', models.BigIntegerField()),
                ('status', models.CharField(max_length=100)),
                ('error_message', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SAPSuccessFactorsGlobalConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('completion_status_api_path', models.CharField(max_length=255)),
                ('course_api_path', models.CharField(max_length=255)),
                ('oauth_api_path', models.CharField(max_length=255)),
                ('search_student_api_path', models.CharField(max_length=255)),
                ('provider_id', models.CharField(default='EDX', max_length=100)),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT,
                                                 to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
        ),
        migrations.CreateModel(
            name='SAPSuccessFactorsEnterpriseCustomerConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('active', models.BooleanField(help_text='Is this configuration active?')),
                ('transmission_chunk_size', models.IntegerField(default=500,
                                                                help_text='The maximum number of data items to transmit to the integrated channel with each request.')),
                ('channel_worker_username', models.CharField(blank=True,
                                                             help_text='Enterprise channel worker username to get JWT tokens for authenticating LMS APIs.',
                                                             max_length=255, null=True)),
                ('catalogs_to_transmit',
                 models.TextField(blank=True, help_text='A comma-separated list of catalog UUIDs to transmit.',
                                  null=True)),
                ('key',
                 models.CharField(help_text='OAuth client identifier.', max_length=255, verbose_name='Client ID')),
                ('sapsf_base_url', models.CharField(help_text='Base URL of success factors API.', max_length=255,
                                                    verbose_name='SAP Base URL')),
                ('sapsf_company_id', models.CharField(help_text='Success factors company identifier.', max_length=255,
                                                      verbose_name='SAP Company ID')),
                ('sapsf_user_id', models.CharField(help_text='Success factors user identifier.', max_length=255,
                                                   verbose_name='SAP User ID')),
                ('secret',
                 models.CharField(help_text='OAuth client secret.', max_length=255, verbose_name='Client Secret')),
                ('user_type', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user',
                                               help_text='Type of SAP User (admin or user).', max_length=20,
                                               verbose_name='SAP User Type')),
                ('additional_locales',
                 models.TextField(blank=True, default='', help_text='A comma-separated list of additional locales.',
                                  verbose_name='Additional Locales')),
                ('show_course_price', models.BooleanField(default=False)),
                ('transmit_total_hours',
                 models.BooleanField(default=False, help_text='Include totalHours in the transmitted completion data',
                                     verbose_name='Transmit Total Hours')),
                ('enterprise_customer',
                 models.OneToOneField(help_text='Enterprise Customer associated with the configuration.',
                                      on_delete=django.db.models.deletion.CASCADE, to='enterprise.EnterpriseCustomer')),
            ],
        ),
    ]
