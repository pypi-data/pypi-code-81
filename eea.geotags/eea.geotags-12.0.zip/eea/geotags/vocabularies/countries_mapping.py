""" Countries
"""
from zope.component import getUtility, queryUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.i18n.normalizer.interfaces import IIDNormalizer
from eea.geotags.vocabularies.interfaces import IGeoCountriesMapping
from collective.taxonomy.interfaces import ITaxonomy


class Countries_Mapping(object):
    """ Extract countries for group
    """
    implements(IGeoCountriesMapping)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        name = 'eea.geolocation.countries_mapping.taxonomy'
        identifier = 'placeholderidentifier'
        data = {}
        normalizer = getUtility(IIDNormalizer)
        normalized_name = normalizer.normalize(name).replace("-", "")
        utility_name = "collective.taxonomy." + normalized_name
        taxonomy = queryUtility(ITaxonomy, name=utility_name)

        try:
            vocabulary = taxonomy(self)
        except:
            vocabulary = taxonomy.makeVocabulary('en')

        for value, key in vocabulary.iterEntries():
            value = value.encode('ascii', 'ignore').decode('ascii')

            if identifier not in value:
                identifier = value
            else:
                country = value.split(identifier)[-1]
                if country == "":
                    country = identifier
                data.update({country: identifier})

        items = [
            SimpleTerm(dictkey, dictkey, val)
            for dictkey, val in data.items()
        ]
        return SimpleVocabulary(items)