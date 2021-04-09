from django.db import models


class ModelExample(models.Model):
    name = models.CharField(max_length=30)
    occupation = models.CharField(max_length=100, choices=[
        ('study', 'Study'),
        ('work', 'Work')
    ], verbose_name='Occupation')
    study = models.CharField(max_length=100, verbose_name='Name Institution', null=True, blank=True)
    semester = models.CharField(max_length=100, verbose_name='Semester', null=True, blank=True)
    company = models.CharField(max_length=100, verbose_name='Company', null=True, blank=True)
    position = models.CharField(max_length=100, verbose_name='Position', null=True, blank=True)
    nick = models.BooleanField(verbose_name='Add NickName', null=True, blank=True, default=True)
    nickname = models.CharField(max_length=100, verbose_name='Nick Name', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Model Example'
        verbose_name_plural = 'Model Example'


class ThemeUI(models.Model):
    name_theme = models.CharField(max_length=200, default='')
    applied = models.BooleanField(help_text='If you select this, the previously applied theme is inactivated, '
                                            'if there is none selected by default, the one from django remains')
    title_window = models.CharField(max_length=200, default='')
    site_name = models.CharField(max_length=200, default='')
    body_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    header_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')
    header_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#417690')
    breadcrumbs_color = models.CharField(max_length=20, null=True, blank=True, default='#c4dce8')
    breadcrumbs_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#79aec8')
    module_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    module_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#79aec8')
    sidebar_current_model_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')
    section_link_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')
    link_color = models.CharField(max_length=20, null=True, blank=True, default='#447e9b')
    link_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#036')
    section_link_visited_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')
    sidebar_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')
    content_related_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#f8f8f8')
    content_related_title_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    content_related_sub_title_color = models.CharField(max_length=20, null=True, blank=True, default='#666')
    quiet_color = models.CharField(max_length=20, null=True, blank=True, default='#999')
    button_tools_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    button_tools_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#999')
    button_tools_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    button_tools_hover_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#417690')
    th_color = models.CharField(max_length=20, null=True, blank=True, default='#666')
    th_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#f6f6f6')
    tr_even_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#f9f9f9')
    paginator_color = models.CharField(max_length=20, null=True, blank=True, default='#666')
    paginator_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    paginator_border_color = models.CharField(max_length=20, null=True, blank=True, default='#eee')
    submit_delete_button_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    submit_delete_button_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#ba2121')
    submit_delete_button_bg_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#a41515')
    submit_save_primary_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    submit_save_primary_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#417690')
    submit_save_primary_bg_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#205067')
    submit_save_secondary_color = models.CharField(max_length=20, null=True, blank=True, default='#fff')
    submit_save_secondary_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#79aec8')
    submit_save_secondary_bg_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#609ab6')
    cancel_button_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    cancel_button_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#ddd')
    cancel_button_bg_hover_color = models.CharField(max_length=20, null=True, blank=True, default='#ccc')
    alert_message_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    alert_message_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#dfd')
    error_alert_message_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    error_alert_message_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#ffefef')
    warning_alert_message_color = models.CharField(max_length=20, null=True, blank=True, default='#333')
    warning_alert_message_bg_color = models.CharField(max_length=20, null=True, blank=True, default='#ffc')

    def __str__(self):
        return self.name_theme

    class Meta:
        verbose_name = 'Theme UI admin'
        verbose_name_plural = 'Theme UI admin'
