from django import forms


class ModelExampleForm(forms.ModelForm):
    occupation = forms.ChoiceField(choices=[
        ('study', 'Study'),
        ('work', 'Work')
    ], )
    study = forms.CharField(label='Name Institution', required=False,
                            widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    semester = forms.CharField(label='Semester', required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    company = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': "occupation j__work"}))
    position = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__work"}))

    nick = forms.BooleanField(required=False, label='Add NickName?', help_text='Select if you want to add NickName',
                              widget=forms.CheckboxInput())
    nickname = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "j__nick"}))


class ThemeUIForm(forms.ModelForm):
    body_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    header_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
    header_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#417690'}))
    breadcrumbs_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#C4DCE8'}))
    breadcrumbs_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#79AEC8'}))
    module_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    module_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#79EAC8'}))
    sidebar_current_model_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
    section_link_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
    link_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#447E9B'}))
    link_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#003366'}))
    section_link_visited_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
    sidebar_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
    content_related_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#F8F8F8'}))
    content_related_title_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    content_related_sub_title_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#666666'}))
    quiet_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#999999'}))
    button_tools_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    button_tools_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#999999'}))
    button_tools_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    button_tools_hover_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#417690'}))
    th_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#666666'}))
    th_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#F6F6F6'}))
    tr_even_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#F9F9F9'}))
    paginator_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#666666'}))
    paginator_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    paginator_border_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#EEEEEE'}))
    submit_delete_button_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    submit_delete_button_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#BA2121'}))
    submit_delete_button_bg_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#A41515'}))
    submit_save_primary_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    submit_save_primary_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#417690'}))
    submit_save_primary_bg_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#205067'}))
    submit_save_secondary_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFFF'}))
    submit_save_secondary_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#79EAC8'}))
    submit_save_secondary_bg_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#609AB6'}))
    cancel_button_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    cancel_button_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#DDDDDD'}))
    cancel_button_bg_hover_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#CCCCCC'}))
    alert_message_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    alert_message_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#DDFFDD'}))
    error_alert_message_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    error_alert_message_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFEFEF'}))
    warning_alert_message_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#333333'}))
    warning_alert_message_bg_color = forms.CharField(widget=forms.TextInput({'type': 'color', 'value': '#FFFFCC'}))
