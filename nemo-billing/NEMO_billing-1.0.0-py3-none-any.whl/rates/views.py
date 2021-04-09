from typing import List, Dict

from NEMO.models import Tool, Area, Consumable
from NEMO.views.pagination import SortedPaginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Model
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET

from NEMO_billing.rates.admin import RateAdminForm
from NEMO_billing.rates.models import RateCategory, Rate, RateType


@staff_member_required(login_url=None)
@require_GET
def rates(request):
    page = SortedPaginator(Rate.objects.all(), request, order_by="type").get_current_page()

    return render(request, "rates/rates.html", {"page": page, "rate_categories_exist": RateCategory.objects.exists()})


@staff_member_required(login_url=None)
@require_http_methods(["GET", "POST"])
def create_or_modify_rate(request, rate_type_choice=None, rate_id=None):
    rate = None
    try:
        rate = Rate.objects.get(id=rate_id)
    except Rate.DoesNotExist:
        pass

    dictionary = {
        "rate_type_choice": rate_type_choice,
        "rate_type_choices": get_rate_type_choices(),
        "rate_id": rate_id,
        "rate_categories": RateCategory.objects.all(),
    }
    rate_types = get_rate_types(rate_type_choice)
    rate_forms = get_rate_forms(request, rate_types, rate)
    dictionary["rate_types"] = rate_types
    dictionary["forms"] = rate_forms
    dictionary["form"] = list(rate_forms.values())[0] if rate_forms else None

    if rate_type_choice == RateType.Type.TOOL:
        dictionary["tools"] = Tool.objects.filter(visible=True).order_by("_category", "name")
    elif rate_type_choice == RateType.Type.AREA:
        dictionary["areas"] = Area.objects.filter(area_children_set__isnull=True)
    elif rate_type_choice == RateType.Type.CONSUMABLE:
        dictionary["consumables"] = Consumable.objects.all().order_by("category", "name")

    forms_all_valid = all([form.is_valid() for form in rate_forms.values()]) if rate_forms else False
    if request.method == "POST" and forms_all_valid:
        # Don't commit since we want to save it using our own method
        for rate_form in rate_forms.values():
            form_rate: Rate = rate_form.save(commit=False)
            form_rate.save_with_user(request.user)
            rate_form.save_m2m()
            message_item = f" for {form_rate.get_item()}" if isinstance(form_rate.get_item(), Model) else ""
            message = f'Your {form_rate.type.get_type_display()} rate{message_item} was successfully {"updated" if rate_id else "created"}.'
            messages.success(request, message=message)
        return redirect("rates")
    else:
        return render(request, "rates/rate.html", dictionary)


# We are building forms for each rate type, for each category.
# The goal is to have all rate forms related to one group type (Tool, Area, Supply etc.) in one view.
def get_rate_forms(request, rate_types: List[RateType], rate: Rate) -> Dict[str, RateAdminForm]:
    forms = {}
    categories = RateCategory.objects.all()
    for rate_type in rate_types:
        if rate_type.category_specific and categories:
            for category in categories:
                rate_type_name = rate_type.get_type_form_name(category)
                data = get_data_from_request(request, rate_type, category)
                instance = None
                if rate:
                    try:
                        instance = Rate.objects.get(
                            type=rate_type,
                            category=category,
                            tool_id=rate.tool_id,
                            area_id=rate.area_id,
                            consumable_id=rate.consumable_id,
                        )
                    except Rate.DoesNotExist:
                        pass
                forms[rate_type_name] = RateAdminForm(data=data, instance=instance)
        else:
            rate_type_name = rate_type.get_type_form_name()
            data = get_data_from_request(request, rate_type)
            instance = None
            if rate:
                try:
                    instance = Rate.objects.get(
                        type=rate_type, tool_id=rate.tool_id, area_id=rate.area_id, consumable_id=rate.consumable_id
                    )
                except Rate.DoesNotExist:
                    pass
            forms[rate_type_name] = RateAdminForm(data=data, instance=instance)
    return forms


def get_data_from_request(request, rate_type: RateType, category: RateCategory = None):
    # Get data from request. We have common fields and type/category specific fields
    if request.method != "POST":
        return None
    data = {
        "type": rate_type.id,
        "category": category.id if category else "",
        "tool": request.POST.get("tool"),
        "area": request.POST.get("area"),
        "consumable": request.POST.get("consumable"),
    }
    type_form_name = rate_type.get_type_form_name(category)
    data["id"] = request.POST.get(type_form_name + "_id")
    data["amount"] = request.POST.get(type_form_name + "_amount")
    data["flat"] = request.POST.get(type_form_name + "_flat")
    data["minimum_charge"] = request.POST.get(type_form_name + "_minimum_charge")
    return data


def get_rate_type_choices():
    # Since we want to group all tool related types, we only have a subset here
    rate_type_choices = set()
    for rate_type in RateType.objects.all():
        if rate_type.is_tool_rate() and rate_type.item_specific:
            rate_type_choices.add((RateType.Type.TOOL, "Tool"))
        elif rate_type.is_area_rate() and rate_type.item_specific:
            rate_type_choices.add((RateType.Type.AREA, "Area"))
        elif rate_type.is_consumable_rate() and rate_type.item_specific:
            rate_type_choices.add((rate_type.type, rate_type.get_type_display()))
        else:
            rate_type_choices.add((rate_type.type, rate_type.get_type_display()))
    return sorted(rate_type_choices)


def get_rate_types(rate_type_choice: str):
    rate_types = []
    if rate_type_choice:
        if rate_type_choice == RateType.Type.TOOL:
            rate_types = RateType.objects.filter(
                type__in=[
                    RateType.Type.TOOL_USAGE,
                    RateType.Type.TOOL_MISSED_RESERVATION,
                    RateType.Type.TOOL_TRAINING_INDIVIDUAL,
                    RateType.Type.TOOL_TRAINING_GROUP,
                ],
                item_specific=True,
            )
        elif rate_type_choice == RateType.Type.AREA:
            rate_types = RateType.objects.filter(
                type__in=[RateType.Type.AREA_USAGE, RateType.Type.AREA_MISSED_RESERVATION], item_specific=True
            )
        elif rate_type_choice == RateType.Type.CONSUMABLE:
            rate_types = RateType.objects.filter(type=RateType.Type.CONSUMABLE)
        else:
            rate_types = RateType.objects.filter(type=rate_type_choice)
    return rate_types
