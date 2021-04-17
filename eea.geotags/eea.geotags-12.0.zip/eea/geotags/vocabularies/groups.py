""" Groups
"""
from zope.component import getUtility, queryUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.i18n.normalizer.interfaces import IIDNormalizer
from eea.geotags.vocabularies.interfaces import IGeoGroups
from collective.taxonomy.interfaces import ITaxonomy


class Groups(object):
    """ Extract countries for group
    """
    implements(IGeoGroups)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        name = 'eea.geolocation.geotags.taxonomy'
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
                identifier_key =  "_".join(value.split(" ")).lower()
                identifier_data.update({identifier_key: data})

            if 'geo' not in value:
                country = value.split(identifier)[-1]
            else:
                geo = value.split(country)[-1]
                data.update({geo: country})

        items = [
            SimpleTerm(dictkey, dictkey, val['title'])
            for dictkey, val in identifier_data.items()
        ]
        return SimpleVocabulary(items)