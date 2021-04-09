from decimal import Decimal
from typing import List, Optional

from NEMO.models import (
    UsageEvent,
    AreaAccessRecord,
    Reservation,
    StaffCharge,
    ConsumableWithdraw,
    TrainingSession,
    Consumable,
    Area,
    Tool,
    User,
)
from NEMO.views.api_billing import get_minutes_between_dates
from django.db.models import Sum, QuerySet, Q, F

from NEMO_billing.invoices.exceptions import NoRateSetException
from NEMO_billing.invoices.models import ProjectBillingDetails, Invoice, InvoiceDetailItem, InvoiceSummaryItem
from NEMO_billing.models import CustomCharge
from NEMO_billing.rates.models import RateType, Rate


def get_rate(
    r_type: str,
    project_details: ProjectBillingDetails,
    tool: Tool = None,
    area: Area = None,
    consumable: Consumable = None,
):
    rate_type = RateType.objects.get(type=r_type)
    kwargs = {"type_id": rate_type.id}
    if rate_type.category_specific:
        kwargs["category"] = project_details.category
    if rate_type.item_specific:
        if tool:
            kwargs["tool_id"] = tool.id
        elif area:
            kwargs["area_id"] = area.id
        elif consumable:
            kwargs["consumable_id"] = consumable.id
    try:
        return Rate.objects.get(**kwargs)
    except Rate.DoesNotExist:
        raise NoRateSetException(rate_type.id, project_details.category, tool=tool, area=area, consumable=consumable)


def get_rate_with_currency(invoice: Invoice, rate: str):
    return f"{invoice.configuration.currency} {rate}"


class InvoiceDataProcessor(object):
    tool_usage_staff_filter = Q(operator__is_staff=True) & ~Q(operator=F("user"))

    def process_data(self, start, end, project_details, configuration, user: User) -> Optional[Invoice]:
        invoice = self.create_invoice(start, end, project_details, configuration, user)
        detail_items: List[InvoiceDetailItem] = []
        detail_items.extend(self.tool_usages_invoice_details(invoice))
        detail_items.extend(self.area_access_records_invoice_details(invoice))
        detail_items.extend(self.missed_reservations_invoice_details(invoice))
        detail_items.extend(self.staff_charges_invoice_details(invoice))
        detail_items.extend(self.consumable_withdrawals_invoice_details(invoice))
        detail_items.extend(self.training_sessions_invoice_details(invoice))
        detail_items.extend(self.custom_charges_invoice_details(invoice))
        if detail_items:
            invoice.save()
            for detail_item in detail_items:
                detail_item.invoice = invoice
                detail_item.save(force_insert=True)
            self.add_invoice_summary_items(invoice)
            return invoice

    def create_invoice(self, start, end, project_details, configuration, user: User) -> Invoice:
        invoice = Invoice()
        invoice.start = start
        invoice.end = end
        invoice.project_details = project_details
        invoice.configuration = configuration
        invoice.created_by = user
        invoice.total_amount = 0
        return invoice

    def tool_usages_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        usage_events = UsageEvent.objects.filter(start__gte=start, end__lte=end, start__lte=end, end__gte=start)
        usage_events = usage_events.filter(project_id=invoice.project_details.project_id).order_by("start")
        # Exclude usage events when operator is staff and different from user
        usage_events = usage_events.exclude(self.tool_usage_staff_filter)
        return [self.item_from_usage_event(invoice, usage_event) for usage_event in usage_events]

    def area_access_records_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        access_records = AreaAccessRecord.objects.filter(
            start__gte=start, end__lte=end, start__lte=end, end__gte=start, staff_charge=None
        )
        access_records = access_records.filter(project_id=invoice.project_details.project_id).order_by("start")
        return [self.item_from_area_access_record(invoice, area_access) for area_access in access_records]

    def missed_reservations_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        misseds = Reservation.objects.filter(
            missed=True, start__gte=start, end__lte=end, start__lte=end, end__gte=start
        )
        misseds = misseds.filter(project_id=invoice.project_details.project_id).order_by("start")
        return [self.item_from_missed_reservation(invoice, missed) for missed in misseds]

    def staff_charges_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        staff_charges = StaffCharge.objects.filter(start__gte=start, end__lte=end, start__lte=end, end__gte=start)
        staff_charges = staff_charges.filter(project_id=invoice.project_details.project_id).order_by("start")
        staff_charge_item_list = [self.item_from_staff_charge(invoice, staff_charge) for staff_charge in staff_charges]
        # Add area access during staff charges
        for area_access in AreaAccessRecord.objects.filter(staff_charge__in=staff_charges):
            area_access_by_staff_item = self.item_from_area_access_record(invoice, area_access)
            area_access_by_staff_item.item_type = InvoiceDetailItem.InvoiceDetailItemType.STAFF_CHARGE
            area_access_by_staff_item.core_facility = None
            staff_charge_item_list.append(area_access_by_staff_item)
        # Add all tool usage by staff members
        usages_by_staff = UsageEvent.objects.filter(start__gte=start, end__lte=end, start__lte=end, end__gte=start)
        usages_by_staff = usages_by_staff.filter(project_id=invoice.project_details.project_id).order_by("start")
        usages_by_staff = usages_by_staff.filter(self.tool_usage_staff_filter)
        for usage_by_staff in usages_by_staff:
            usages_by_staff_item = self.item_from_usage_event(invoice, usage_by_staff)
            usages_by_staff_item.item_type = InvoiceDetailItem.InvoiceDetailItemType.STAFF_CHARGE
            usages_by_staff_item.core_facility = None
            staff_charge_item_list.append(usages_by_staff_item)
        return staff_charge_item_list

    def consumable_withdrawals_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        withdrawals = ConsumableWithdraw.objects.filter(date__gte=start, date__lte=end)
        withdrawals = withdrawals.filter(project_id=invoice.project_details.project_id).order_by("date")
        return [self.item_from_consumable_withdrawal(invoice, withdrawal) for withdrawal in withdrawals]

    def training_sessions_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        training_sessions = TrainingSession.objects.filter(date__gte=start, date__lte=end)
        training_sessions = training_sessions.filter(project_id=invoice.project_details.project_id).order_by("date")
        return [self.item_from_training(invoice, training) for training in training_sessions]

    def custom_charges_invoice_details(self, invoice: Invoice) -> List[InvoiceDetailItem]:
        start, end = invoice.start, invoice.end
        custom_charges = CustomCharge.objects.filter(date__gte=start, date__lte=end)
        custom_charges = custom_charges.filter(project_id=invoice.project_details.project_id).order_by("date")
        return [self.item_from_custom_charge(invoice, custom_charge) for custom_charge in custom_charges]

    def item_from_usage_event(self, invoice: Invoice, usage_event: UsageEvent) -> InvoiceDetailItem:
        duration = get_minutes_between_dates(usage_event.start, usage_event.end)
        item = InvoiceDetailItem(start=usage_event.start, end=usage_event.end, quantity=duration)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.TOOL_USAGE
        item.name = usage_event.tool.name
        item.user = usage_event.user.username
        item.core_facility = usage_event.tool.core_facility
        rate: Rate = get_rate(RateType.Type.TOOL_USAGE, invoice.project_details, tool=usage_event.tool)
        item.amount = rate.calculate_amount(item.quantity)
        item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_area_access_record(self, invoice: Invoice, area_access_record: AreaAccessRecord):
        duration = get_minutes_between_dates(area_access_record.start, area_access_record.end)
        item = InvoiceDetailItem(start=area_access_record.start, end=area_access_record.end, quantity=duration)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.AREA_ACCESS
        item.name = area_access_record.area.name
        item.user = area_access_record.customer.username
        item.core_facility = area_access_record.area.core_facility
        rate: Rate = get_rate(RateType.Type.AREA_USAGE, invoice.project_details, area=area_access_record.area)
        item.amount = rate.calculate_amount(item.quantity)
        item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_missed_reservation(self, invoice: Invoice, missed_reservation: Reservation) -> InvoiceDetailItem:
        item = InvoiceDetailItem(start=missed_reservation.start, end=missed_reservation.end, quantity=1)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.MISSED_RESERVATION
        item.user = missed_reservation.user.username
        if missed_reservation.tool:
            item.core_facility = missed_reservation.tool.core_facility
            item.name = f"{missed_reservation.tool.name}"
            rate = get_rate(
                RateType.Type.TOOL_MISSED_RESERVATION, invoice.project_details, tool=missed_reservation.tool
            )
            item.amount = rate.calculate_amount(item.quantity)
            item.rate = get_rate_with_currency(invoice, rate.display_rate())
        if missed_reservation.area:
            item.core_facility = missed_reservation.area.core_facility
            item.name = f"{missed_reservation.area.name}"
            rate = get_rate(
                RateType.Type.AREA_MISSED_RESERVATION, invoice.project_details, area=missed_reservation.area
            )
            item.amount = rate.calculate_amount(item.quantity)
            item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_staff_charge(self, invoice: Invoice, staff_charge: StaffCharge) -> InvoiceDetailItem:
        duration = get_minutes_between_dates(staff_charge.start, staff_charge.end)
        item = InvoiceDetailItem(start=staff_charge.start, end=staff_charge.end, quantity=duration)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.STAFF_CHARGE
        item.name = "Staff time"
        item.user = staff_charge.customer.username
        rate = get_rate(RateType.Type.STAFF_CHARGE, invoice.project_details)
        item.amount = rate.calculate_amount(item.quantity)
        item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_consumable_withdrawal(self, invoice: Invoice, withdrawal: ConsumableWithdraw) -> InvoiceDetailItem:
        item = InvoiceDetailItem(start=withdrawal.date, end=withdrawal.date, quantity=withdrawal.quantity)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.CONSUMABLE
        item.core_facility = withdrawal.consumable.core_facility
        item.name = withdrawal.consumable.name
        item.user = withdrawal.customer.username
        rate = get_rate(RateType.Type.CONSUMABLE, invoice.project_details, consumable=withdrawal.consumable)
        item.amount = rate.calculate_amount(item.quantity)
        item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_training(self, invoice: Invoice, training: TrainingSession) -> InvoiceDetailItem:
        item = InvoiceDetailItem(start=training.date, end=training.date, quantity=training.duration)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.TRAINING
        item.core_facility = training.tool.core_facility
        item.name = f"{training.tool.name} ({training.get_type_display()})"
        item.user = training.trainee.username
        if training.type == TrainingSession.Type.INDIVIDUAL:
            rate = get_rate(RateType.Type.TOOL_TRAINING_INDIVIDUAL, invoice.project_details, tool=training.tool)
        else:
            rate = get_rate(RateType.Type.TOOL_TRAINING_GROUP, invoice.project_details, tool=training.tool)
        item.amount = rate.calculate_amount(item.quantity)
        item.rate = get_rate_with_currency(invoice, rate.display_rate())
        return item

    def item_from_custom_charge(self, invoice, custom_charge) -> InvoiceDetailItem:
        item = InvoiceDetailItem(start=custom_charge.date, end=custom_charge.date, quantity=1)
        item.item_type = InvoiceDetailItem.InvoiceDetailItemType.CUSTOM_CHARGE
        item.core_facility = custom_charge.core_facility
        item.name = custom_charge.name
        item.user = custom_charge.customer.username
        item.amount = custom_charge.amount
        return item

    def add_invoice_summary_items(self, invoice):
        # Core facilities sorted alphabetically by non empty ones first
        for core_facility in invoice.sorted_core_facilities():
            if core_facility:
                facility_category = InvoiceSummaryItem(invoice=invoice, name=core_facility)
                facility_category.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.CATEGORY
                facility_category.save(force_insert=True)
            self._add_summary_items_for_facility(invoice, core_facility)

        # Facility discounts. Grab all facility discounts and apply them.
        # Note: discounts have negative amounts
        discount_total = Decimal(0)
        discount_items = invoice.invoicesummaryitem_set.filter(
            summary_item_type=InvoiceSummaryItem.InvoiceSummaryItemType.FACILITY_DISCOUNT
        )
        if discount_items:
            for discount_item in discount_items:
                discount_total += discount_item.amount

        # Recap of all charges
        charges = InvoiceSummaryItem(invoice=invoice, name="Total Charges")
        charges.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.CATEGORY
        charges.amount = invoice.invoicedetailitem_set.aggregate(Sum("amount"))["amount__sum"] + discount_total
        charges.save(force_insert=True)

        # Tax
        tax_amount = Decimal(0)
        if invoice.configuration.tax and charges.amount > Decimal(0):
            tax = InvoiceSummaryItem(
                invoice=invoice, name=f"{invoice.configuration.tax_name} ({invoice.configuration.tax_display()}%)"
            )
            tax.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.TAX
            tax_amount = charges.amount * invoice.configuration.tax_amount()
            tax.amount = tax_amount
            tax.save(force_insert=True)

        invoice.total_amount = charges.amount + tax_amount
        invoice.save(update_fields=["total_amount"])

    def _add_summary_items_for_facility(self, invoice: Invoice, core_facility: Optional[str]):
        details = invoice.invoicedetailitem_set.filter(core_facility=core_facility)
        tool_usage = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.TOOL_USAGE)
        self._add_aggregate_items_with_details(invoice, "Tool Usage", core_facility, tool_usage)
        area_access = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.AREA_ACCESS)
        self._add_aggregate_items_with_details(invoice, "Area Access", core_facility, area_access)
        consumables = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.CONSUMABLE)
        self._add_aggregate_items_with_details(invoice, "Supplies/Materials", core_facility, consumables)
        staff_charges = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.STAFF_CHARGE)
        self._add_aggregate_items_with_details(invoice, "Technical Work", core_facility, staff_charges)
        trainings = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.TRAINING)
        self._add_aggregate_items_with_details(invoice, "Training", core_facility, trainings)
        missed_reservations = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.MISSED_RESERVATION)
        self._add_aggregate_items_with_details(invoice, "Missed Reservations", core_facility, missed_reservations)
        custom_charges = details.filter(item_type=InvoiceDetailItem.InvoiceDetailItemType.CUSTOM_CHARGE)
        self._add_aggregate_items_with_details(invoice, "Other", core_facility, custom_charges)
        if core_facility:
            facility_subtotal = InvoiceSummaryItem(invoice=invoice, name="Subtotal", core_facility=core_facility)
            facility_subtotal.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL
            facility_subtotal.amount = details.aggregate(Sum("amount"))["amount__sum"]
            facility_subtotal.save(force_insert=True)

    def _add_aggregate_items_with_details(self, invoice, name, core_facility: str, items: QuerySet):
        if items.exists():
            if not core_facility:
                # Add an category item if we are not inside a core facility group
                summary_item = InvoiceSummaryItem(invoice=invoice, name=name, core_facility=core_facility)
                summary_item.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.CATEGORY
                summary_item.save(force_insert=True)
            item_names = list(items.values_list("name", flat=True).distinct())
            item_names.sort()
            for item_name in item_names:
                item_name_qs = items.filter(name=item_name)
                item_rate = item_name_qs.first().rate
                item_type = item_name_qs.first().item_type
                total_q = item_name_qs.aggregate(Sum("quantity"))["quantity__sum"]
                if InvoiceDetailItem.InvoiceDetailItemType.is_time_type(item_type):
                    quantity_display = f" ({total_q/60:.2f} hours)"
                elif item_type == InvoiceDetailItem.InvoiceDetailItemType.CUSTOM_CHARGE:
                    quantity_display = ""
                else:
                    quantity_display = f" (x {total_q})"
                summary_item_name_prefix = f"{name} - " if core_facility else ""
                summary_item_name = f"{summary_item_name_prefix}{item_name}{quantity_display}"
                summary_item = InvoiceSummaryItem(invoice=invoice, name=summary_item_name, core_facility=core_facility)
                summary_item.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.ITEM
                summary_item.details = item_rate
                summary_item.amount = item_name_qs.aggregate(Sum("amount"))["amount__sum"]
                summary_item.save(force_insert=True)
            if not core_facility:
                # Add an subtotal item if we are not inside a core facility group
                subtotal = InvoiceSummaryItem(invoice=invoice, name="Subtotal")
                subtotal.summary_item_type = InvoiceSummaryItem.InvoiceSummaryItemType.SUBTOTAL
                subtotal.amount = items.aggregate(Sum("amount"))["amount__sum"]
                subtotal.save(force_insert=True)
