
import datetime
import factory

from ..models import Catalogue
from ..models import Product
from ..models import Storage

from .utils import FuzzyTimeStamp


class ProductF(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: 'name_%s' % n)
    shelf_life = FuzzyTimeStamp(start_timestamp=1000)


class CatalogueF(factory.django.DjangoModelFactory):

    class Meta:
        model = Catalogue

    storage = factory.SubFactory(ProductF)
    date_of_add = datetime.datetime.now()


class StorageF(factory.django.DjangoModelFactory):

    class Meta:
        model = Storage

    product = factory.SubFactory(ProductF)
    date_of_delivery = datetime.datetime.now()
    date_of_manufacture = datetime.datetime.now()
