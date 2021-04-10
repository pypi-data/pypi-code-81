from NEMO.forms import ProjectForm
from NEMO.models import Project, Account, User, MembershipHistory, ActivityHistory
from NEMO.views.accounts_and_projects import select_accounts_and_projects
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import models
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from NEMO_billing.invoices.models import ProjectBillingDetails
from NEMO_billing.invoices.utilities import render_combine_responses
from NEMO_billing.rates.models import RateCategory


class ProjectDetailsForm(models.ModelForm):
    class Meta:
        model = ProjectBillingDetails
        fields = ["category", "project_name", "contact_name", "contact_email", "details", "no_charge"]


@staff_member_required(login_url=None)
@require_http_methods(["GET", "POST"])
def edit_project(request, project_id=None):
    try:
        project = Project.objects.get(id=project_id)
    except (Project.DoesNotExist, ValueError):
        project = None
    try:
        project_details = project.projectbillingdetails
    except (ProjectBillingDetails.DoesNotExist, AttributeError):
        project_details = ProjectBillingDetails(project=project)
    form = ProjectForm(request.POST or None, instance=project)
    details_form = ProjectDetailsForm(request.POST or None, instance=project_details)
    dictionary = {
        "account_list": Account.objects.all(),
        "user_list": User.objects.filter(is_active=True),
        "rate_categories": RateCategory.objects.all(),
        "form": form,
        "form_details": details_form,
    }
    if request.method == "GET":
        return render(request, "invoices/project/edit_project.html", dictionary)
    elif request.method == "POST":
        if not form.is_valid() or not details_form.is_valid():
            return render(request, "invoices/project/edit_project.html", dictionary)
        else:
            project = form.save()
            details_form.instance.project = project
            details_form.save()
            active_changed = form.initial.get("active", None) != project.active
            account_changed = form.initial.get("account", None) != project.account.id
            if not project_id or account_changed:
                if project_id and account_changed:
                    removed_account_history = MembershipHistory()
                    removed_account_history.authorizer = request.user
                    removed_account_history.action = MembershipHistory.Action.REMOVED
                    removed_account_history.child_content_object = project
                    removed_account_history.parent_content_object = Account.objects.get(id=form.initial["account"])
                    removed_account_history.save()
                account_history = MembershipHistory()
                account_history.authorizer = request.user
                account_history.action = MembershipHistory.Action.ADDED
                account_history.child_content_object = project
                account_history.parent_content_object = project.account
                account_history.save()
            if not project_id or active_changed:
                project_history = ActivityHistory()
                project_history.authorizer = request.user
                project_history.action = project.active
                project_history.content_object = project
                project_history.save()
            return redirect("project", project.id)


@staff_member_required(login_url=None)
@require_http_methods(["GET", "POST"])
def custom_project_view(request, identifier=None):
    original_response = select_accounts_and_projects(request, kind="project", identifier=identifier)
    return render_combine_responses(
        request, original_response, "invoices/project/view_project_edit_button.html", {"project_id": identifier}
    )
