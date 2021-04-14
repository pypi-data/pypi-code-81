'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2022 import ClutchConnection
    from ._2023 import ClutchSocket
    from ._2024 import ConceptCouplingConnection
    from ._2025 import ConceptCouplingSocket
    from ._2026 import CouplingConnection
    from ._2027 import CouplingSocket
    from ._2028 import PartToPartShearCouplingConnection
    from ._2029 import PartToPartShearCouplingSocket
    from ._2030 import SpringDamperConnection
    from ._2031 import SpringDamperSocket
    from ._2032 import TorqueConverterConnection
    from ._2033 import TorqueConverterPumpSocket
    from ._2034 import TorqueConverterTurbineSocket
