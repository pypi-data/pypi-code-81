'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._874 import DesignConstraint
    from ._875 import DesignConstraintCollectionDatabase
    from ._876 import DesignConstraintsCollection
    from ._877 import GearDesign
    from ._878 import GearDesignComponent
    from ._879 import GearMeshDesign
    from ._880 import GearSetDesign
    from ._881 import SelectedDesignConstraintsCollection
