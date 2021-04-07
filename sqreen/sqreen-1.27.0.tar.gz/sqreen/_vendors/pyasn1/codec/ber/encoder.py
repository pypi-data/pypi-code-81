#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2018, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pyasn1/license.html
#
from ... import debug
from ... import error
from . import eoo
from ...compat.integer import to_bytes
from ...compat.octets import (int2oct, oct2int, ints2octs, null,
                                  str2octs, isOctetsType)
from ...type import char
from ...type import tag
from ...type import univ
from ...type import useful

__all__ = ['encode']


class AbstractItemEncoder(object):
    supportIndefLenMode = True

    # An outcome of otherwise legit call `encodeFun(eoo.endOfOctets)`
    eooIntegerSubstrate = (0, 0)
    eooOctetsSubstrate = ints2octs(eooIntegerSubstrate)

    # noinspection PyMethodMayBeStatic
    def encodeTag(self, singleTag, isConstructed):
        tagClass, tagFormat, tagId = singleTag
        encodedTag = tagClass | tagFormat
        if isConstructed:
            encodedTag |= tag.tagFormatConstructed
        if tagId < 31:
            return encodedTag | tagId,
        else:
            substrate = tagId & 0x7f,
            tagId >>= 7
            while tagId:
                substrate = (0x80 | (tagId & 0x7f),) + substrate
                tagId >>= 7
            return (encodedTag | 0x1F,) + substrate

    def encodeLength(self, length, defMode):
        if not defMode and self.supportIndefLenMode:
            return (0x80,)
        if length < 0x80:
            return length,
        else:
            substrate = ()
            while length:
                substrate = (length & 0xff,) + substrate
                length >>= 8
            substrateLen = len(substrate)
            if substrateLen > 126:
                raise error.PyAsn1Error('Length octets overflow (%d)' % substrateLen)
            return (0x80 | substrateLen,) + substrate

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        raise error.PyAsn1Error('Not implemented')

    def encode(self, value, asn1Spec=None, encodeFun=None, **options):

        if asn1Spec is None:
            tagSet = value.tagSet
        else:
            tagSet = asn1Spec.tagSet

        # untagged item?
        if not tagSet:
            substrate, isConstructed, isOctets = self.encodeValue(
                value, asn1Spec, encodeFun, **options
            )
            return substrate

        defMode = options.get('defMode', True)

        for idx, singleTag in enumerate(tagSet.superTags):

            defModeOverride = defMode

            # base tag?
            if not idx:
                substrate, isConstructed, isOctets = self.encodeValue(
                    value, asn1Spec, encodeFun, **options
                )

                if not substrate and isConstructed and options.get('ifNotEmpty', False):
                    return substrate

                # primitive form implies definite mode
                if not isConstructed:
                    defModeOverride = True

            header = self.encodeTag(singleTag, isConstructed)
            header += self.encodeLength(len(substrate), defModeOverride)

            if isOctets:
                substrate = ints2octs(header) + substrate

                if not defModeOverride:
                    substrate += self.eooOctetsSubstrate

            else:
                substrate = header + substrate

                if not defModeOverride:
                    substrate += self.eooIntegerSubstrate

        if not isOctets:
            substrate = ints2octs(substrate)

        return substrate


class EndOfOctetsEncoder(AbstractItemEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        return null, False, True


class BooleanEncoder(AbstractItemEncoder):
    supportIndefLenMode = False

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        return value and (1,) or (0,), False, False


class IntegerEncoder(AbstractItemEncoder):
    supportIndefLenMode = False
    supportCompactZero = False

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if value == 0:
            # de-facto way to encode zero
            if self.supportCompactZero:
                return (), False, False
            else:
                return (0,), False, False

        return to_bytes(int(value), signed=True), False, True


class BitStringEncoder(AbstractItemEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is not None:
            # TODO: try to avoid ASN.1 schema instantiation
            value = asn1Spec.clone(value)

        valueLength = len(value)
        if valueLength % 8:
            alignedValue = value << (8 - valueLength % 8)
        else:
            alignedValue = value

        maxChunkSize = options.get('maxChunkSize', 0)
        if not maxChunkSize or len(alignedValue) <= maxChunkSize * 8:
            substrate = alignedValue.asOctets()
            return int2oct(len(substrate) * 8 - valueLength) + substrate, False, True

        baseTag = value.tagSet.baseTag

        # strip off explicit tags
        if baseTag:
            tagSet = tag.TagSet(baseTag, baseTag)
        else:
            tagSet = tag.TagSet()

        alignedValue = alignedValue.clone(tagSet=tagSet)

        stop = 0
        substrate = null
        while stop < valueLength:
            start = stop
            stop = min(start + maxChunkSize * 8, valueLength)
            substrate += encodeFun(alignedValue[start:stop], asn1Spec, **options)

        return substrate, True, True


class OctetStringEncoder(AbstractItemEncoder):

    def encodeValue(self, value, asn1Spec, encodeFun, **options):

        if asn1Spec is None:
            substrate = value.asOctets()

        elif not isOctetsType(value):
            substrate = asn1Spec.clone(value).asOctets()

        else:
            substrate = value

        maxChunkSize = options.get('maxChunkSize', 0)

        if not maxChunkSize or len(substrate) <= maxChunkSize:
            return substrate, False, True

        else:

            # strip off explicit tags for inner chunks

            if asn1Spec is None:
                baseTag = value.tagSet.baseTag

                # strip off explicit tags
                if baseTag:
                    tagSet = tag.TagSet(baseTag, baseTag)
                else:
                    tagSet = tag.TagSet()

                asn1Spec = value.clone(tagSet=tagSet)

            elif not isOctetsType(value):
                baseTag = asn1Spec.tagSet.baseTag

                # strip off explicit tags
                if baseTag:
                    tagSet = tag.TagSet(baseTag, baseTag)
                else:
                    tagSet = tag.TagSet()

                asn1Spec = asn1Spec.clone(tagSet=tagSet)

            pos = 0
            substrate = null

            while True:
                chunk = value[pos:pos + maxChunkSize]
                if not chunk:
                    break

                substrate += encodeFun(chunk, asn1Spec, **options)
                pos += maxChunkSize

            return substrate, True, True


class NullEncoder(AbstractItemEncoder):
    supportIndefLenMode = False

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        return null, False, True


class ObjectIdentifierEncoder(AbstractItemEncoder):
    supportIndefLenMode = False

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is not None:
            value = asn1Spec.clone(value)

        oid = value.asTuple()

        # Build the first pair
        try:
            first = oid[0]
            second = oid[1]

        except IndexError:
            raise error.PyAsn1Error('Short OID %s' % (value,))

        if 0 <= second <= 39:
            if first == 1:
                oid = (second + 40,) + oid[2:]
            elif first == 0:
                oid = (second,) + oid[2:]
            elif first == 2:
                oid = (second + 80,) + oid[2:]
            else:
                raise error.PyAsn1Error('Impossible first/second arcs at %s' % (value,))
        elif first == 2:
            oid = (second + 80,) + oid[2:]
        else:
            raise error.PyAsn1Error('Impossible first/second arcs at %s' % (value,))

        octets = ()

        # Cycle through subIds
        for subOid in oid:
            if 0 <= subOid <= 127:
                # Optimize for the common case
                octets += (subOid,)
            elif subOid > 127:
                # Pack large Sub-Object IDs
                res = (subOid & 0x7f,)
                subOid >>= 7
                while subOid:
                    res = (0x80 | (subOid & 0x7f),) + res
                    subOid >>= 7
                # Add packed Sub-Object ID to resulted Object ID
                octets += res
            else:
                raise error.PyAsn1Error('Negative OID arc %s at %s' % (subOid, value))

        return octets, False, False


class RealEncoder(AbstractItemEncoder):
    supportIndefLenMode = 0
    binEncBase = 2  # set to None to choose encoding base automatically

    @staticmethod
    def _dropFloatingPoint(m, encbase, e):
        ms, es = 1, 1
        if m < 0:
            ms = -1  # mantissa sign
        if e < 0:
            es = -1  # exponenta sign 
        m *= ms
        if encbase == 8:
            m *= 2 ** (abs(e) % 3 * es)
            e = abs(e) // 3 * es
        elif encbase == 16:
            m *= 2 ** (abs(e) % 4 * es)
            e = abs(e) // 4 * es

        while True:
            if int(m) != m:
                m *= encbase
                e -= 1
                continue
            break
        return ms, int(m), encbase, e

    def _chooseEncBase(self, value):
        m, b, e = value
        encBase = [2, 8, 16]
        if value.binEncBase in encBase:
            return self._dropFloatingPoint(m, value.binEncBase, e)
        elif self.binEncBase in encBase:
            return self._dropFloatingPoint(m, self.binEncBase, e)
        # auto choosing base 2/8/16 
        mantissa = [m, m, m]
        exponenta = [e, e, e]
        sign = 1
        encbase = 2
        e = float('inf')
        for i in range(3):
            (sign,
             mantissa[i],
             encBase[i],
             exponenta[i]) = self._dropFloatingPoint(mantissa[i], encBase[i], exponenta[i])
            if abs(exponenta[i]) < abs(e) or (abs(exponenta[i]) == abs(e) and mantissa[i] < m):
                e = exponenta[i]
                m = int(mantissa[i])
                encbase = encBase[i]
        return sign, m, encbase, e

    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is not None:
            value = asn1Spec.clone(value)

        if value.isPlusInf:
            return (0x40,), False, False
        if value.isMinusInf:
            return (0x41,), False, False
        m, b, e = value
        if not m:
            return null, False, True
        if b == 10:
            return str2octs('\x03%dE%s%d' % (m, e == 0 and '+' or '', e)), False, True
        elif b == 2:
            fo = 0x80  # binary encoding
            ms, m, encbase, e = self._chooseEncBase(value)
            if ms < 0:  # mantissa sign
                fo |= 0x40  # sign bit
            # exponenta & mantissa normalization
            if encbase == 2:
                while m & 0x1 == 0:
                    m >>= 1
                    e += 1
            elif encbase == 8:
                while m & 0x7 == 0:
                    m >>= 3
                    e += 1
                fo |= 0x10
            else:  # encbase = 16
                while m & 0xf == 0:
                    m >>= 4
                    e += 1
                fo |= 0x20
            sf = 0  # scale factor
            while m & 0x1 == 0:
                m >>= 1
                sf += 1
            if sf > 3:
                raise error.PyAsn1Error('Scale factor overflow')  # bug if raised
            fo |= sf << 2
            eo = null
            if e == 0 or e == -1:
                eo = int2oct(e & 0xff)
            else:
                while e not in (0, -1):
                    eo = int2oct(e & 0xff) + eo
                    e >>= 8
                if e == 0 and eo and oct2int(eo[0]) & 0x80:
                    eo = int2oct(0) + eo
                if e == -1 and eo and not (oct2int(eo[0]) & 0x80):
                    eo = int2oct(0xff) + eo
            n = len(eo)
            if n > 0xff:
                raise error.PyAsn1Error('Real exponent overflow')
            if n == 1:
                pass
            elif n == 2:
                fo |= 1
            elif n == 3:
                fo |= 2
            else:
                fo |= 3
                eo = int2oct(n & 0xff) + eo
            po = null
            while m:
                po = int2oct(m & 0xff) + po
                m >>= 8
            substrate = int2oct(fo) + eo + po
            return substrate, False, True
        else:
            raise error.PyAsn1Error('Prohibited Real base %s' % b)


class SequenceEncoder(AbstractItemEncoder):
    omitEmptyOptionals = False

    # TODO: handling three flavors of input is too much -- split over codecs

    def encodeValue(self, value, asn1Spec, encodeFun, **options):

        substrate = null

        if asn1Spec is None:
            # instance of ASN.1 schema
            value.verifySizeSpec()

            namedTypes = value.componentType

            for idx, component in enumerate(value.values()):
                if namedTypes:
                    namedType = namedTypes[idx]

                    if namedType.isOptional and not component.isValue:
                            continue

                    if namedType.isDefaulted and component == namedType.asn1Object:
                            continue

                    if self.omitEmptyOptionals:
                        options.update(ifNotEmpty=namedType.isOptional)

                chunk = encodeFun(component, asn1Spec, **options)

                # wrap open type blob if needed
                if namedTypes and namedType.openType:
                    wrapType = namedType.asn1Object
                    if wrapType.tagSet and not wrapType.isSameTypeWith(component):
                        chunk = encodeFun(chunk, wrapType, **options)

                substrate += chunk

        else:
            # bare Python value + ASN.1 schema
            for idx, namedType in enumerate(asn1Spec.componentType.namedTypes):

                try:
                    component = value[namedType.name]

                except KeyError:
                    raise error.PyAsn1Error('Component name "%s" not found in %r' % (namedType.name, value))

                if namedType.isOptional and namedType.name not in value:
                    continue

                if namedType.isDefaulted and component == namedType.asn1Object:
                    continue

                if self.omitEmptyOptionals:
                    options.update(ifNotEmpty=namedType.isOptional)

                chunk = encodeFun(component, asn1Spec[idx], **options)

                # wrap open type blob if needed
                if namedType.openType:
                    wrapType = namedType.asn1Object
                    if wrapType.tagSet and not wrapType.isSameTypeWith(component):
                        chunk = encodeFun(chunk, wrapType, **options)

                substrate += chunk

        return substrate, True, True


class SequenceOfEncoder(AbstractItemEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is None:
            value.verifySizeSpec()
        else:
            asn1Spec = asn1Spec.componentType

        substrate = null

        for idx, component in enumerate(value):
            substrate += encodeFun(value[idx], asn1Spec, **options)

        return substrate, True, True


class ChoiceEncoder(AbstractItemEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is None:
            component = value.getComponent()
        else:
            names = [namedType.name for namedType in asn1Spec.componentType.namedTypes
                     if namedType.name in value]
            if len(names) != 1:
                raise error.PyAsn1Error('%s components for Choice at %r' % (len(names) and 'Multiple ' or 'None ', value))

            name = names[0]

            component = value[name]
            asn1Spec = asn1Spec[name]

        return encodeFun(component, asn1Spec, **options), True, True


class AnyEncoder(OctetStringEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options):
        if asn1Spec is None:
            value = value.asOctets()
        elif not isOctetsType(value):
            value = asn1Spec.clone(value).asOctets()

        return value, not options.get('defMode', True), True


tagMap = {
    eoo.endOfOctets.tagSet: EndOfOctetsEncoder(),
    univ.Boolean.tagSet: BooleanEncoder(),
    univ.Integer.tagSet: IntegerEncoder(),
    univ.BitString.tagSet: BitStringEncoder(),
    univ.OctetString.tagSet: OctetStringEncoder(),
    univ.Null.tagSet: NullEncoder(),
    univ.ObjectIdentifier.tagSet: ObjectIdentifierEncoder(),
    univ.Enumerated.tagSet: IntegerEncoder(),
    univ.Real.tagSet: RealEncoder(),
    # Sequence & Set have same tags as SequenceOf & SetOf
    univ.SequenceOf.tagSet: SequenceOfEncoder(),
    univ.SetOf.tagSet: SequenceOfEncoder(),
    univ.Choice.tagSet: ChoiceEncoder(),
    # character string types
    char.UTF8String.tagSet: OctetStringEncoder(),
    char.NumericString.tagSet: OctetStringEncoder(),
    char.PrintableString.tagSet: OctetStringEncoder(),
    char.TeletexString.tagSet: OctetStringEncoder(),
    char.VideotexString.tagSet: OctetStringEncoder(),
    char.IA5String.tagSet: OctetStringEncoder(),
    char.GraphicString.tagSet: OctetStringEncoder(),
    char.VisibleString.tagSet: OctetStringEncoder(),
    char.GeneralString.tagSet: OctetStringEncoder(),
    char.UniversalString.tagSet: OctetStringEncoder(),
    char.BMPString.tagSet: OctetStringEncoder(),
    # useful types
    useful.ObjectDescriptor.tagSet: OctetStringEncoder(),
    useful.GeneralizedTime.tagSet: OctetStringEncoder(),
    useful.UTCTime.tagSet: OctetStringEncoder()
}

# Put in ambiguous & non-ambiguous types for faster codec lookup
typeMap = {
    univ.Boolean.typeId: BooleanEncoder(),
    univ.Integer.typeId: IntegerEncoder(),
    univ.BitString.typeId: BitStringEncoder(),
    univ.OctetString.typeId: OctetStringEncoder(),
    univ.Null.typeId: NullEncoder(),
    univ.ObjectIdentifier.typeId: ObjectIdentifierEncoder(),
    univ.Enumerated.typeId: IntegerEncoder(),
    univ.Real.typeId: RealEncoder(),
    # Sequence & Set have same tags as SequenceOf & SetOf
    univ.Set.typeId: SequenceEncoder(),
    univ.SetOf.typeId: SequenceOfEncoder(),
    univ.Sequence.typeId: SequenceEncoder(),
    univ.SequenceOf.typeId: SequenceOfEncoder(),
    univ.Choice.typeId: ChoiceEncoder(),
    univ.Any.typeId: AnyEncoder(),
    # character string types
    char.UTF8String.typeId: OctetStringEncoder(),
    char.NumericString.typeId: OctetStringEncoder(),
    char.PrintableString.typeId: OctetStringEncoder(),
    char.TeletexString.typeId: OctetStringEncoder(),
    char.VideotexString.typeId: OctetStringEncoder(),
    char.IA5String.typeId: OctetStringEncoder(),
    char.GraphicString.typeId: OctetStringEncoder(),
    char.VisibleString.typeId: OctetStringEncoder(),
    char.GeneralString.typeId: OctetStringEncoder(),
    char.UniversalString.typeId: OctetStringEncoder(),
    char.BMPString.typeId: OctetStringEncoder(),
    # useful types
    useful.ObjectDescriptor.typeId: OctetStringEncoder(),
    useful.GeneralizedTime.typeId: OctetStringEncoder(),
    useful.UTCTime.typeId: OctetStringEncoder()
}


class Encoder(object):
    fixedDefLengthMode = None
    fixedChunkSize = None

    # noinspection PyDefaultArgument
    def __init__(self, tagMap, typeMap={}):
        self.__tagMap = tagMap
        self.__typeMap = typeMap

    def __call__(self, value, asn1Spec=None, **options):
        try:
            if asn1Spec is None:
                typeId = value.typeId
            else:
                typeId = asn1Spec.typeId

        except AttributeError:
            raise error.PyAsn1Error('Value %r is not ASN.1 type instance '
                                    'and "asn1Spec" not given' % (value,))

        if debug.logger & debug.flagEncoder:
            logger = debug.logger
        else:
            logger = None

        if logger:
            logger('encoder called in %sdef mode, chunk size %s for '
                   'type %s, value:\n%s' % (not options.get('defMode', True) and 'in' or '', options.get('maxChunkSize', 0), asn1Spec is None and value.prettyPrintType() or asn1Spec.prettyPrintType(), value))

        if self.fixedDefLengthMode is not None:
            options.update(defMode=self.fixedDefLengthMode)

        if self.fixedChunkSize is not None:
            options.update(maxChunkSize=self.fixedChunkSize)


        try:
            concreteEncoder = self.__typeMap[typeId]

            if logger:
                logger('using value codec %s chosen by type ID %s' % (concreteEncoder.__class__.__name__, typeId))

        except KeyError:
            if asn1Spec is None:
                tagSet = value.tagSet
            else:
                tagSet = asn1Spec.tagSet

            # use base type for codec lookup to recover untagged types
            baseTagSet = tag.TagSet(tagSet.baseTag, tagSet.baseTag)

            try:
                concreteEncoder = self.__tagMap[baseTagSet]

            except KeyError:
                raise error.PyAsn1Error('No encoder for %r (%s)' % (value, tagSet))

            if logger:
                logger('using value codec %s chosen by tagSet %s' % (concreteEncoder.__class__.__name__, tagSet))

        substrate = concreteEncoder.encode(value, asn1Spec, self, **options)

        if logger:
            logger('codec %s built %s octets of substrate: %s\nencoder completed' % (concreteEncoder, len(substrate), debug.hexdump(substrate)))

        return substrate

#: Turns ASN.1 object into BER octet stream.
#:
#: Takes any ASN.1 object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#: walks all its components recursively and produces a BER octet stream.
#:
#: Parameters
#: ----------
#: value: either a Python or pyasn1 object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#:     A Python or pyasn1 object to encode. If Python object is given, `asnSpec`
#:     parameter is required to guide the encoding process.
#:
#: Keyword Args
#: ------------
#: asn1Spec:
#:     Optional ASN.1 schema or value object e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
#:
#: defMode: :py:class:`bool`
#:     If `False`, produces indefinite length encoding
#:
#: maxChunkSize: :py:class:`int`
#:     Maximum chunk size in chunked encoding mode (0 denotes unlimited chunk size)
#:
#: Returns
#: -------
#: : :py:class:`bytes` (Python 3) or :py:class:`str` (Python 2)
#:     Given ASN.1 object encoded into BER octetstream
#:
#: Raises
#: ------
#: :py:class:`~pyasn1.error.PyAsn1Error`
#:     On encoding errors
#:
#: Examples
#: --------
#: Encode Python value into BER with ASN.1 schema
#:
#: .. code-block:: pycon
#:
#:    >>> seq = SequenceOf(componentType=Integer())
#:    >>> encode([1, 2, 3], asn1Spec=seq)
#:    b'0\t\x02\x01\x01\x02\x01\x02\x02\x01\x03'
#:
#: Encode ASN.1 value object into BER
#:
#: .. code-block:: pycon
#:
#:    >>> seq = SequenceOf(componentType=Integer())
#:    >>> seq.extend([1, 2, 3])
#:    >>> encode(seq)
#:    b'0\t\x02\x01\x01\x02\x01\x02\x02\x01\x03'
#:
encode = Encoder(tagMap, typeMap)
