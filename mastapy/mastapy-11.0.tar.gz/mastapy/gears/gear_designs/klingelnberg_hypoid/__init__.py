'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._907 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._908 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._909 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._910 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
