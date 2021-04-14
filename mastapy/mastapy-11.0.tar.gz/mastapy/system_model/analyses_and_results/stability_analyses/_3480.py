'''_3480.py

CylindricalPlanetGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2202
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3479
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CylindricalPlanetGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearStabilityAnalysis',)


class CylindricalPlanetGearStabilityAnalysis(_3479.CylindricalGearStabilityAnalysis):
    '''CylindricalPlanetGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2202.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
