'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1215 import ContactSpecification
    from ._1216 import CrowningSpecificationMethod
    from ._1217 import CycloidalAssemblyDesign
    from ._1218 import CycloidalDiscDesign
    from ._1219 import CycloidalDiscMaterial
    from ._1220 import CycloidalDiscMaterialDatabase
    from ._1221 import CycloidalDiscModificationsSpecification
    from ._1222 import DirectionOfMeasuredModifications
    from ._1223 import NamedDiscPhase
    from ._1224 import RingPinsDesign
    from ._1225 import RingPinsMaterial
    from ._1226 import RingPinsMaterialDatabase
