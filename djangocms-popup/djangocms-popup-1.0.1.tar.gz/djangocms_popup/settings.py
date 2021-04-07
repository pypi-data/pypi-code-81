from django.conf import settings


# add_list_button is content of djangocms_popup_add_list_button or true
ADD_LIST_BUTTON = getattr(settings, "DJANGOCMS_POPUP_ADD_LIST_BUTTON", True)
