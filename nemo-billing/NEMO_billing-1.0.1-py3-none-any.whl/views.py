from NEMO.models import User
from NEMO.views.pagination import SortedPaginator
from django.conf import settings
from django.contrib import messages

from NEMO_billing.admin import CustomChargeAdminForm

from NEMO_billing.models import CustomCharge, CoreFacility
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


@staff_member_required(login_url=None)
@require_http_methods(["GET", "POST"])
def custom_charges(request):
    page = SortedPaginator(CustomCharge.objects.all(), request, order_by="-date").get_current_page()
    core_facilities_exist = CoreFacility.objects.exists()
    return render(
        request, "billing/custom_charges.html", {"page": page, "core_facilities_exist": core_facilities_exist}
    )


@staff_member_required(login_url=None)
@require_http_methods(["GET", "POST"])
def create_or_modify_custom_charge(request, custom_charge_id=None):
    custom_charge = None
    try:
        custom_charge = CustomCharge.objects.get(id=custom_charge_id)
    except CustomCharge.DoesNotExist:
        pass

    form = CustomChargeAdminForm(request.POST or None, instance=custom_charge)

    dictionary = {
        "core_facilities": CoreFacility.objects.all(),
        "core_facility_required": settings.CUSTOM_CHARGE_CORE_FACILITY_REQUIRED,
        "form": form,
        "users": User.objects.filter(is_active=True),
    }
    if request.method == "POST" and form.is_valid():
        charge: CustomCharge = form.save()
        message = f'Your custom charge "{charge.name}" of {charge.amount} for {charge.customer} was successfully logged and will be billed to project {charge.project}.'
        messages.success(request, message=message)
        return redirect("custom_charges")
    else:
        if custom_charge:
            dictionary["projects"] = custom_charge.customer.active_projects()
        if hasattr(form, "cleaned_data") and "customer" in form.cleaned_data:
            dictionary["projects"] = form.cleaned_data["customer"].active_projects()
        return render(request, "billing/custom_charge.html", dictionary)
