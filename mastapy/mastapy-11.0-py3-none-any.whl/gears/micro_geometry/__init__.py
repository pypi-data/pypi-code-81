'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._517 import BiasModification
    from ._518 import FlankMicroGeometry
    from ._519 import LeadModification
    from ._520 import LocationOfEvaluationLowerLimit
    from ._521 import LocationOfEvaluationUpperLimit
    from ._522 import LocationOfRootReliefEvaluation
    from ._523 import LocationOfTipReliefEvaluation
    from ._524 import MainProfileReliefEndsAtTheStartOfRootReliefOption
    from ._525 import MainProfileReliefEndsAtTheStartOfTipReliefOption
    from ._526 import Modification
    from ._527 import ParabolicRootReliefStartsTangentToMainProfileRelief
    from ._528 import ParabolicTipReliefStartsTangentToMainProfileRelief
    from ._529 import ProfileModification
