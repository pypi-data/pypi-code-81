from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from schools.models import School, Subscription
from common import common_helpers
from common.common_helpers import TRIAL_LENGTH
from common.email import new_school_email, new_user_existing_school_email, add_send_in_blue_contact
from config.settings.base import PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_RELEASE_DATE, PROGRAM_DESCRIPTION_SCHOOL, \
    PROGRAM_DESCRIPTION_DEPARTMENTAL, LAUNCH_PAGE, FAQ_PAGE
from core_nav.forms import UserDetailsForm, SchoolDetailsForm, ShowHelpForm, SchoolCodeForm
from help import overview_help_guides
from users.models import User
from emails.email_helpers import send_user_email



class HomeView(LoginRequiredMixin, TemplateView):
    home_template_name = 'core_nav/home.html'
    welcome_template_name = 'core_nav/user-details.html'

    def get(self, request, *args, **kwargs):

        user = request.user

        if user.is_authenticated:

            if len(user.first_name) > 0 and user.school is not None:

                is_departmental = request.user.is_departmental()
                if is_departmental:
                    program_description = PROGRAM_DESCRIPTION_DEPARTMENTAL
                else:
                    program_description = PROGRAM_DESCRIPTION_SCHOOL

                context = {
                    'program_name': PROGRAM_NAME,
                    'program_description': program_description,
                    'launch_page': reverse(LAUNCH_PAGE),
                    'show_overview_help': user.show_overview_help
                }

                return render(request, self.home_template_name, context)
            else:

                user_details_form = UserDetailsForm()
                school_details_form = SchoolDetailsForm()

                context = {
                    'program_name': PROGRAM_NAME,
                    'user_details_form': user_details_form,
                    'school_details_form': school_details_form,

                }

                return render(request, self.welcome_template_name, context)


        else:
            return redirect('account_login')

    def post(self, request, *args, **kwargs):

        if 'save_name' in request.POST:

            user_details_form = UserDetailsForm(request.POST)

            if user_details_form.is_valid():
                request.user.first_name = user_details_form.clean_first_name()
                request.user.last_name = user_details_form.clean_last_name()
                request.user.save()

                send_user_email(request.user, 'welcome')


                return HttpResponseRedirect(reverse('core_nav:choose-signup-option'))


        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class SchoolDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/school-details.html'

    def get(self, request, *args, **kwargs):

        school_details_form = SchoolDetailsForm()

        context = {
            'program_name': PROGRAM_NAME,
            'school_details_form': school_details_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if 'save_school' in request.POST:

            school_details_form = SchoolDetailsForm(request.POST)

            if school_details_form.is_valid():
                school_name = school_details_form.clean_school_name()
                authority = school_details_form.clean_authority()
                school_type = school_details_form.clean_school_type()

                school = School.objects.new_school_account(school_name, authority, school_type)
                User.objects.update_school(request.user, school)

                Subscription.objects.create_individual_subscription(request.user, school)

                new_school_email(request.user, school_name, authority, school_type)

                add_send_in_blue_contact(request.user)

                return HttpResponseRedirect(reverse('core_nav:get-started'))

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



class GetStarted(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/get-started.html'

    def get(self, request, *args, **kwargs):

        subscription = Subscription.objects.get_subscription_details(request.user)
        if subscription.individual_subscription:
            new_account = True
        else:
            new_account = False


        context = {
            'program_name': PROGRAM_NAME,
            'trial_length': TRIAL_LENGTH,
            'school_name': request.user.school.school_name,
            'new_account': new_account,
            'school_code': request.user.school.school_code
        }

        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/settings.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user

        user_department_membership_count = current_user.count_user_department_membership()
        can_upload_badge = common_helpers.can_upload_badge()
        school_badge_url = common_helpers.get_school_badge_url(current_user.school)

        subscription = Subscription.objects.get_subscription_details(request.user)

        context = {
            'program_name': PROGRAM_NAME,
            'faq_page': FAQ_PAGE,
            'current_user': current_user,
            'user_department_membership_count': user_department_membership_count,
            'can_upload_badge': can_upload_badge,
            'school_badge_url': school_badge_url,
            'subscription': subscription
        }

        return render(request, self.template_name, context)


class AboutView(LoginRequiredMixin, TemplateView):

    template_name = 'core_nav/about.html'

    def get(self, request, *args, **kwargs):

        context = {
            'program_name': PROGRAM_NAME,
            'program_version': PROGRAM_VERSION,
            'program_release_date': PROGRAM_RELEASE_DATE
        }

        return render(request, self.template_name, context)


class OverviewHelp(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/overview-help.html'

    def get(self, request, *args, **kwargs):

        show_help_form = ShowHelpForm()
        show_help_form.set_initial()

        help_pages = overview_help_guides.get_help_text()

        paginator = Paginator(help_pages, 1)
        page = request.GET.get('page')
        paginated_pages = paginator.get_page(page)

        context = {
            'program_name': PROGRAM_NAME,
            'show_help_form': show_help_form,
            'help_pages': help_pages,
            'paginated_pages': paginated_pages,
            'paginator': paginator
        }



        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if 'done' in request.POST:
            show_help_form = ShowHelpForm(request.POST)
            if show_help_form.is_valid():
                dont_show_help = show_help_form.clean_dont_show_help()
                User.objects.update_dont_show_help(dont_show_help, request.user)

        return HttpResponseRedirect(reverse(LAUNCH_PAGE))

class ChooseSignUpOption(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/choose-signup-option.html'

    def get(self, request, *args, **kwargs):

        context = {

        }

        return render(request, self.template_name, context)

class SchoolCode(LoginRequiredMixin, TemplateView):
    template_name = 'core_nav/school-code.html'

    def get(self, request, *args, **kwargs):

        school_code_form = SchoolCodeForm()


        context = {
            'school_code_form': school_code_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if 'save-school' in request.POST:

            school_code_form = SchoolCodeForm(request.POST)
            if school_code_form.is_valid():
                typed_code = school_code_form.clean_school_code()

                school_code_exists = School.objects.school_code_exists(typed_code)

                if school_code_exists:
                    school = School.objects.get_school_by_school_code(typed_code)
                    User.objects.update_school(request.user, school)

                    new_user_existing_school_email(request.user, school)

                    add_send_in_blue_contact(request.user)

                    return HttpResponseRedirect(reverse('core_nav:get-started'))
            else:

                context = {
                    'school_code_form': school_code_form
                }

                return render(request, self.template_name, context)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')



def check_school_code(request):

    typed_code = request.POST.get('typed_code', None)

    school_code_exists = School.objects.school_code_exists(typed_code)


    if school_code_exists:
        school = School.objects.get_school_by_school_code(typed_code)
        new_html = 'School: ' + school.school_name

        button_enabled_html = '<button type="submit" class="btn btn-success" name="save-school" value="Save"">Next <i class="material-icons">chevron_right</i><br></button>'
        new_button_html = button_enabled_html


    else:
        new_html = "<p><span>&#8203;</span></p>"
        new_button_html = '<button type="submit" class="btn btn-success disabled">Next <i class="material-icons">chevron_right</i><br></button>'



    data = {
        'new_html': new_html,
        'new_button_html': new_button_html
    }



    return JsonResponse(data)
