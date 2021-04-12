from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now
from django_scopes import scopes_disabled
from pretix.base.models import Event, Quota
from pretix.base.services.quotas import QuotaAvailability


class Command(BaseCommand):
    help = "Hide sold out events"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--allow-republish", action="store_true")

    @scopes_disabled()
    def handle(self, *args, **options):
        eqs = Event.objects.filter(plugins__contains="pretix_hide_sold_out", live=True)
        if not options.get("allow_republish"):
            eqs = eqs.filter(is_public=True)
        for e in eqs:
            if e.has_subevents:
                subevents = (
                    e.subevents_annotated("web")
                    .filter(
                        active=True,
                        is_public=True,
                    )
                    .filter(
                        Q(presale_end__gte=now())
                        | Q(
                            Q(presale_end__isnull=True)
                            & Q(Q(date_to__gte=now()) | Q(date_from__gte=now()))
                        )
                    )
                )
                subevents = list(subevents)
                quotas_to_compute = []
                for se in subevents:
                    quotas_to_compute += [
                        q
                        for q in se.active_quotas
                    ]
                if quotas_to_compute:
                    qa = QuotaAvailability()
                    qa.queue(*quotas_to_compute)
                    qa.compute(allow_cache=True)
                any_available = False
                for se in subevents:
                    if quotas_to_compute:
                        se._quota_cache = qa.results
                    if se.best_availability_state in (
                        Quota.AVAILABILITY_RESERVED,
                        Quota.AVAILABILITY_OK,
                    ):
                        any_available = True
                        break
            else:
                quotas_to_compute = e.quotas.all()
                if quotas_to_compute:
                    qa = QuotaAvailability()
                    qa.queue(*quotas_to_compute)
                    qa.compute(allow_cache=True)
                any_available = any(
                    r[0] in (Quota.AVAILABILITY_RESERVED, Quota.AVAILABILITY_OK)
                    for r in qa.results.values()
                )

            if any_available and not e.is_public and options.get("allow_republish"):
                if options.get("dry_run"):
                    print(f"Event {e.organizer.slug}/{e.slug} will be made public.")
                else:
                    e.is_public = True
                    e.save()
            elif not any_available and e.is_public:
                if options.get("dry_run"):
                    print(f"Event {e.organizer.slug}/{e.slug} will be made non-public.")
                else:
                    e.is_public = False
                    e.save()
