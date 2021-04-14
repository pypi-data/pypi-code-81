'''_620.py

HobbingProcessSimulationNew
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _615, _617, _618, _614,
    _616, _622, _633, _619
)
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessSimulationNew',)


class HobbingProcessSimulationNew(_633.ProcessSimulationNew['_619.HobbingProcessSimulationInput']):
    '''HobbingProcessSimulationNew

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_SIMULATION_NEW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hobbing_process_lead_calculation(self) -> '_615.HobbingProcessLeadCalculation':
        '''HobbingProcessLeadCalculation: 'HobbingProcessLeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_615.HobbingProcessLeadCalculation)(self.wrapped.HobbingProcessLeadCalculation) if self.wrapped.HobbingProcessLeadCalculation else None

    @property
    def hobbing_process_pitch_calculation(self) -> '_617.HobbingProcessPitchCalculation':
        '''HobbingProcessPitchCalculation: 'HobbingProcessPitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_617.HobbingProcessPitchCalculation)(self.wrapped.HobbingProcessPitchCalculation) if self.wrapped.HobbingProcessPitchCalculation else None

    @property
    def hobbing_process_profile_calculation(self) -> '_618.HobbingProcessProfileCalculation':
        '''HobbingProcessProfileCalculation: 'HobbingProcessProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_618.HobbingProcessProfileCalculation)(self.wrapped.HobbingProcessProfileCalculation) if self.wrapped.HobbingProcessProfileCalculation else None

    @property
    def hobbing_process_gear_shape_calculation(self) -> '_614.HobbingProcessGearShape':
        '''HobbingProcessGearShape: 'HobbingProcessGearShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_614.HobbingProcessGearShape)(self.wrapped.HobbingProcessGearShapeCalculation) if self.wrapped.HobbingProcessGearShapeCalculation else None

    @property
    def hobbing_process_mark_on_shaft_calculation(self) -> '_616.HobbingProcessMarkOnShaft':
        '''HobbingProcessMarkOnShaft: 'HobbingProcessMarkOnShaftCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_616.HobbingProcessMarkOnShaft)(self.wrapped.HobbingProcessMarkOnShaftCalculation) if self.wrapped.HobbingProcessMarkOnShaftCalculation else None

    @property
    def hobbing_process_total_modification(self) -> '_622.HobbingProcessTotalModificationCalculation':
        '''HobbingProcessTotalModificationCalculation: 'HobbingProcessTotalModification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_622.HobbingProcessTotalModificationCalculation)(self.wrapped.HobbingProcessTotalModification) if self.wrapped.HobbingProcessTotalModification else None
