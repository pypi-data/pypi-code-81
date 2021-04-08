
import datetime

from django.test import TestCase


from django_postgresql_function.functions import datetime as _datetime

from .models.tests.factory_models import CatalogueF
from .models.tests.factory_models import ProductF
from .models.tests.factory_models import StorageF

from .models import models


class DateTestCase(TestCase):

    def setUp(self) -> None:
        self.product = ProductF.create()
        self.storage = StorageF.create(
            product=self.product,
            date_of_manufacture=datetime.date(2020, 1, 1),
        )

        self.catalogue = CatalogueF.create(
            storage=self.storage,
        )

    # def test_age(self):
    # FIXME вернуть после добавления поддержки TZ
    #    qs = models.Storage.objects.filter(
    #        pk=self.storage.pk
    #    ).annotate(
    #        age=_datetime.Age('date_of_manufacture')
    #    ).values('age')
    #
    #    self.assertEqual(
    #        qs[0]['age'], datetime.date.today() - self.storage.date_of_manufacture
    #    )

    def test_age_from_date(self):
        qs = models.Storage.objects.filter(
            pk=self.storage.pk
        ).annotate(
            age=_datetime.Age('date_of_manufacture', datetime.date(2021, 1, 1))
        ).values('age')

        self.assertEqual(
            qs[0]['age'], datetime.timedelta(days=-365)
        )

    def test_date_diff_year(self):
        qs = models.Storage.objects.filter(
            pk=self.storage.pk
        ).annotate(
            date_diff=_datetime.YearsDateDiff(
                'date_of_manufacture', datetime.date(2019, 1, 1)
            )
        ).values('date_diff')

        self.assertEqual(
            qs[0]['date_diff'], 1
        )

    def test_date_diff_month(self):
        qs = models.Storage.objects.filter(
            pk=self.storage.pk
        ).annotate(
            date_diff=_datetime.MonthsDateDiff(
                'date_of_manufacture', datetime.date(2019, 2, 1),
            )
        ).values('date_diff')

        self.assertEqual(
            qs[0]['date_diff'], 11
        )

    def test_date_diff_day(self):
        qs = models.Storage.objects.filter(
            pk=self.storage.pk
        ).annotate(
            date_diff=_datetime.DaysDateDiff(
                'date_of_manufacture', datetime.date(2019, 12, 3),
            )
        ).values('date_diff')

        self.assertEqual(
            qs[0]['date_diff'], 29
        )
