""" Groups
"""
from zope.component import getUtility, queryUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.i18n.normalizer.interfaces import IIDNormalizer

from eea.geotags.vocabularies.interfaces import IBioGroups
from collective.taxonomy.interfaces import ITaxonomy


class BioGroups(object):
    """ Biogeographical regions
    """
    implements(IBioGroups)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        name = 'eea.geolocation.biotags.taxonomy'
        identifier = 'placeholderidentifier'
        identifier_data = {}
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
                data = {}
                data.update({'title': identifier})

            if 'latitude' in value:
                latitude = value.split('latitude')[-1]
                data.update({'latitude': latitude})

            if 'longitude' in value:
                longitude = value.split('longitude')[-1]
                data.update({'longitude': longitude})

            if 'Abbreviation' in value:
                identifier_key = value.split('Abbreviation')[-1]
                identifier_data.update({identifier_key: data})
        del identifier_data['']
        items = [
            SimpleTerm(dictkey, dictkey, val['title'])
            for dictkey, val in identifier_data.items()
        ]
        return SimpleVocabulary(items)