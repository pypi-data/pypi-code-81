'''_2343.py

CompoundHarmonicAnalysisOfSingleExcitationAnalysis
'''


from typing import Iterable

from mastapy.system_model.connections_and_sockets.couplings import (
    _2030, _2032, _2028, _2022,
    _2024, _2026
)
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _5567, _5582, _5465, _5464,
    _5466, _5472, _5483, _5484,
    _5489, _5500, _5515, _5516,
    _5520, _5521, _5471, _5525,
    _5539, _5540, _5541, _5542,
    _5543, _5549, _5550, _5551,
    _5558, _5562, _5585, _5586,
    _5559, _5493, _5495, _5517,
    _5519, _5468, _5470, _5475,
    _5477, _5478, _5479, _5480,
    _5482, _5496, _5498, _5511,
    _5513, _5514, _5522, _5524,
    _5526, _5528, _5530, _5532,
    _5533, _5535, _5536, _5538,
    _5548, _5563, _5565, _5569,
    _5571, _5572, _5574, _5575,
    _5576, _5587, _5589, _5590,
    _5592, _5507, _5509, _5553,
    _5544, _5546, _5474, _5485,
    _5487, _5490, _5492, _5501,
    _5503, _5505, _5506, _5552,
    _5560, _5556, _5555, _5566,
    _5568, _5577, _5578, _5579,
    _5580, _5581, _5583, _5584,
    _5561, _5504, _5473, _5488,
    _5499, _5529, _5547, _5557,
    _5467, _5476, _5494, _5518,
    _5570, _5481, _5497, _5469,
    _5512, _5527, _5531, _5534,
    _5537, _5564, _5573, _5588,
    _5591, _5523, _5508, _5510,
    _5554, _5545, _5486, _5491,
    _5502
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2114, _2113, _2115, _2118,
    _2120, _2121, _2122, _2125,
    _2126, _2129, _2130, _2131,
    _2112, _2132, _2139, _2140,
    _2141, _2143, _2145, _2146,
    _2148, _2149, _2151, _2153,
    _2154, _2155
)
from mastapy.system_model.part_model.shaft_model import _2158
from mastapy.system_model.part_model.gears import (
    _2196, _2197, _2203, _2204,
    _2188, _2189, _2190, _2191,
    _2192, _2193, _2194, _2195,
    _2198, _2199, _2200, _2201,
    _2202, _2205, _2207, _2209,
    _2210, _2211, _2212, _2213,
    _2214, _2215, _2216, _2217,
    _2218, _2219, _2220, _2221,
    _2222, _2223, _2224, _2225,
    _2226, _2227, _2228, _2229
)
from mastapy.system_model.part_model.cycloidal import _2243, _2244, _2245
from mastapy.system_model.part_model.couplings import (
    _2263, _2264, _2251, _2253,
    _2254, _2256, _2257, _2258,
    _2259, _2261, _2262, _2265,
    _2273, _2271, _2272, _2275,
    _2276, _2277, _2279, _2280,
    _2281, _2282, _2283, _2285
)
from mastapy.system_model.connections_and_sockets import (
    _1975, _1953, _1948, _1949,
    _1952, _1961, _1967, _1972,
    _1945
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1981, _1985, _1991, _2005,
    _1983, _1987, _1979, _1989,
    _1995, _1998, _1999, _2000,
    _2003, _2007, _2009, _2011,
    _1993
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2015, _2018, _2021
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2294

_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundHarmonicAnalysisOfSingleExcitationAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundHarmonicAnalysisOfSingleExcitationAnalysis',)


class CompoundHarmonicAnalysisOfSingleExcitationAnalysis(_2294.CompoundAnalysis):
    '''CompoundHarmonicAnalysisOfSingleExcitationAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundHarmonicAnalysisOfSingleExcitationAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_spring_damper_connection(self, design_entity: '_2030.SpringDamperConnection') -> 'Iterable[_5567.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5567.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_torque_converter_connection(self, design_entity: '_2032.TorqueConverterConnection') -> 'Iterable[_5582.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5582.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_abstract_shaft(self, design_entity: '_2114.AbstractShaft') -> 'Iterable[_5465.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_5465.AbstractShaftCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_abstract_assembly(self, design_entity: '_2113.AbstractAssembly') -> 'Iterable[_5464.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5464.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2115.AbstractShaftOrHousing') -> 'Iterable[_5466.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None), constructor.new(_5466.AbstractShaftOrHousingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bearing(self, design_entity: '_2118.Bearing') -> 'Iterable[_5472.BearingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BearingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None), constructor.new(_5472.BearingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bolt(self, design_entity: '_2120.Bolt') -> 'Iterable[_5483.BoltCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BoltCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None), constructor.new(_5483.BoltCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bolted_joint(self, design_entity: '_2121.BoltedJoint') -> 'Iterable[_5484.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None), constructor.new(_5484.BoltedJointCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_component(self, design_entity: '_2122.Component') -> 'Iterable[_5489.ComponentCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ComponentCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5489.ComponentCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_connector(self, design_entity: '_2125.Connector') -> 'Iterable[_5500.ConnectorCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConnectorCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None), constructor.new(_5500.ConnectorCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_datum(self, design_entity: '_2126.Datum') -> 'Iterable[_5515.DatumCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.DatumCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None), constructor.new(_5515.DatumCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_external_cad_model(self, design_entity: '_2129.ExternalCADModel') -> 'Iterable[_5516.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_5516.ExternalCADModelCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_fe_part(self, design_entity: '_2130.FEPart') -> 'Iterable[_5520.FEPartCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.FEPartCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None), constructor.new(_5520.FEPartCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_flexible_pin_assembly(self, design_entity: '_2131.FlexiblePinAssembly') -> 'Iterable[_5521.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5521.FlexiblePinAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_assembly(self, design_entity: '_2112.Assembly') -> 'Iterable[_5471.AssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5471.AssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_guide_dxf_model(self, design_entity: '_2132.GuideDxfModel') -> 'Iterable[_5525.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_5525.GuideDxfModelCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_mass_disc(self, design_entity: '_2139.MassDisc') -> 'Iterable[_5539.MassDiscCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.MassDiscCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None), constructor.new(_5539.MassDiscCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_measurement_component(self, design_entity: '_2140.MeasurementComponent') -> 'Iterable[_5540.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5540.MeasurementComponentCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_mountable_component(self, design_entity: '_2141.MountableComponent') -> 'Iterable[_5541.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5541.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_oil_seal(self, design_entity: '_2143.OilSeal') -> 'Iterable[_5542.OilSealCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.OilSealCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None), constructor.new(_5542.OilSealCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_part(self, design_entity: '_2145.Part') -> 'Iterable[_5543.PartCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PartCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None), constructor.new(_5543.PartCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_planet_carrier(self, design_entity: '_2146.PlanetCarrier') -> 'Iterable[_5549.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None), constructor.new(_5549.PlanetCarrierCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_point_load(self, design_entity: '_2148.PointLoad') -> 'Iterable[_5550.PointLoadCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PointLoadCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_5550.PointLoadCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_power_load(self, design_entity: '_2149.PowerLoad') -> 'Iterable[_5551.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_5551.PowerLoadCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_root_assembly(self, design_entity: '_2151.RootAssembly') -> 'Iterable[_5558.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5558.RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_specialised_assembly(self, design_entity: '_2153.SpecialisedAssembly') -> 'Iterable[_5562.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5562.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_unbalanced_mass(self, design_entity: '_2154.UnbalancedMass') -> 'Iterable[_5585.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None), constructor.new(_5585.UnbalancedMassCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_virtual_component(self, design_entity: '_2155.VirtualComponent') -> 'Iterable[_5586.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5586.VirtualComponentCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_shaft(self, design_entity: '_2158.Shaft') -> 'Iterable[_5559.ShaftCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ShaftCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_5559.ShaftCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_gear(self, design_entity: '_2196.ConceptGear') -> 'Iterable[_5493.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5493.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_gear_set(self, design_entity: '_2197.ConceptGearSet') -> 'Iterable[_5495.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5495.ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_face_gear(self, design_entity: '_2203.FaceGear') -> 'Iterable[_5517.FaceGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.FaceGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5517.FaceGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_face_gear_set(self, design_entity: '_2204.FaceGearSet') -> 'Iterable[_5519.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5519.FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2188.AGMAGleasonConicalGear') -> 'Iterable[_5468.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5468.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2189.AGMAGleasonConicalGearSet') -> 'Iterable[_5470.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5470.AGMAGleasonConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_differential_gear(self, design_entity: '_2190.BevelDifferentialGear') -> 'Iterable[_5475.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5475.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2191.BevelDifferentialGearSet') -> 'Iterable[_5477.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5477.BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2192.BevelDifferentialPlanetGear') -> 'Iterable[_5478.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5478.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2193.BevelDifferentialSunGear') -> 'Iterable[_5479.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5479.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_gear(self, design_entity: '_2194.BevelGear') -> 'Iterable[_5480.BevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5480.BevelGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_gear_set(self, design_entity: '_2195.BevelGearSet') -> 'Iterable[_5482.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5482.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_conical_gear(self, design_entity: '_2198.ConicalGear') -> 'Iterable[_5496.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5496.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_conical_gear_set(self, design_entity: '_2199.ConicalGearSet') -> 'Iterable[_5498.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5498.ConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cylindrical_gear(self, design_entity: '_2200.CylindricalGear') -> 'Iterable[_5511.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5511.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cylindrical_gear_set(self, design_entity: '_2201.CylindricalGearSet') -> 'Iterable[_5513.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5513.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2202.CylindricalPlanetGear') -> 'Iterable[_5514.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5514.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_gear(self, design_entity: '_2205.Gear') -> 'Iterable[_5522.GearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.GearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5522.GearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_gear_set(self, design_entity: '_2207.GearSet') -> 'Iterable[_5524.GearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.GearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5524.GearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_hypoid_gear(self, design_entity: '_2209.HypoidGear') -> 'Iterable[_5526.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5526.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_hypoid_gear_set(self, design_entity: '_2210.HypoidGearSet') -> 'Iterable[_5528.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5528.HypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2211.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5530.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5530.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2212.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5532.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5532.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2213.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5533.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5533.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2214.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5535.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5535.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2215.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5536.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5536.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5538.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5538.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_planetary_gear_set(self, design_entity: '_2217.PlanetaryGearSet') -> 'Iterable[_5548.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5548.PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_spiral_bevel_gear(self, design_entity: '_2218.SpiralBevelGear') -> 'Iterable[_5563.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5563.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2219.SpiralBevelGearSet') -> 'Iterable[_5565.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5565.SpiralBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2220.StraightBevelDiffGear') -> 'Iterable[_5569.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5569.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2221.StraightBevelDiffGearSet') -> 'Iterable[_5571.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5571.StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_gear(self, design_entity: '_2222.StraightBevelGear') -> 'Iterable[_5572.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5572.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2223.StraightBevelGearSet') -> 'Iterable[_5574.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5574.StraightBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2224.StraightBevelPlanetGear') -> 'Iterable[_5575.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5575.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2225.StraightBevelSunGear') -> 'Iterable[_5576.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5576.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_worm_gear(self, design_entity: '_2226.WormGear') -> 'Iterable[_5587.WormGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.WormGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5587.WormGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_worm_gear_set(self, design_entity: '_2227.WormGearSet') -> 'Iterable[_5589.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5589.WormGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_zerol_bevel_gear(self, design_entity: '_2228.ZerolBevelGear') -> 'Iterable[_5590.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5590.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2229.ZerolBevelGearSet') -> 'Iterable[_5592.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5592.ZerolBevelGearSetCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cycloidal_assembly(self, design_entity: '_2243.CycloidalAssembly') -> 'Iterable[_5507.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5507.CycloidalAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cycloidal_disc(self, design_entity: '_2244.CycloidalDisc') -> 'Iterable[_5509.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None), constructor.new(_5509.CycloidalDiscCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_ring_pins(self, design_entity: '_2245.RingPins') -> 'Iterable[_5553.RingPinsCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RingPinsCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None), constructor.new(_5553.RingPinsCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2263.PartToPartShearCoupling') -> 'Iterable[_5544.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5544.PartToPartShearCouplingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2264.PartToPartShearCouplingHalf') -> 'Iterable[_5546.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5546.PartToPartShearCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_belt_drive(self, design_entity: '_2251.BeltDrive') -> 'Iterable[_5474.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None), constructor.new(_5474.BeltDriveCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_clutch(self, design_entity: '_2253.Clutch') -> 'Iterable[_5485.ClutchCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ClutchCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None), constructor.new(_5485.ClutchCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_clutch_half(self, design_entity: '_2254.ClutchHalf') -> 'Iterable[_5487.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5487.ClutchHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_coupling(self, design_entity: '_2256.ConceptCoupling') -> 'Iterable[_5490.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5490.ConceptCouplingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_coupling_half(self, design_entity: '_2257.ConceptCouplingHalf') -> 'Iterable[_5492.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5492.ConceptCouplingHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_coupling(self, design_entity: '_2258.Coupling') -> 'Iterable[_5501.CouplingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CouplingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5501.CouplingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_coupling_half(self, design_entity: '_2259.CouplingHalf') -> 'Iterable[_5503.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5503.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cvt(self, design_entity: '_2261.CVT') -> 'Iterable[_5505.CVTCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CVTCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None), constructor.new(_5505.CVTCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cvt_pulley(self, design_entity: '_2262.CVTPulley') -> 'Iterable[_5506.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_5506.CVTPulleyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_pulley(self, design_entity: '_2265.Pulley') -> 'Iterable[_5552.PulleyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PulleyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_5552.PulleyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_shaft_hub_connection(self, design_entity: '_2273.ShaftHubConnection') -> 'Iterable[_5560.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5560.ShaftHubConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_rolling_ring(self, design_entity: '_2271.RollingRing') -> 'Iterable[_5556.RollingRingCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RollingRingCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None), constructor.new(_5556.RollingRingCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_rolling_ring_assembly(self, design_entity: '_2272.RollingRingAssembly') -> 'Iterable[_5555.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5555.RollingRingAssemblyCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_spring_damper(self, design_entity: '_2275.SpringDamper') -> 'Iterable[_5566.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None), constructor.new(_5566.SpringDamperCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_spring_damper_half(self, design_entity: '_2276.SpringDamperHalf') -> 'Iterable[_5568.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5568.SpringDamperHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_synchroniser(self, design_entity: '_2277.Synchroniser') -> 'Iterable[_5577.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None), constructor.new(_5577.SynchroniserCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_synchroniser_half(self, design_entity: '_2279.SynchroniserHalf') -> 'Iterable[_5578.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5578.SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_synchroniser_part(self, design_entity: '_2280.SynchroniserPart') -> 'Iterable[_5579.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None), constructor.new(_5579.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_synchroniser_sleeve(self, design_entity: '_2281.SynchroniserSleeve') -> 'Iterable[_5580.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None), constructor.new(_5580.SynchroniserSleeveCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_torque_converter(self, design_entity: '_2282.TorqueConverter') -> 'Iterable[_5581.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None), constructor.new(_5581.TorqueConverterCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_torque_converter_pump(self, design_entity: '_2283.TorqueConverterPump') -> 'Iterable[_5583.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None), constructor.new(_5583.TorqueConverterPumpCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_torque_converter_turbine(self, design_entity: '_2285.TorqueConverterTurbine') -> 'Iterable[_5584.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None), constructor.new(_5584.TorqueConverterTurbineCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1975.ShaftToMountableComponentConnection') -> 'Iterable[_5561.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5561.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cvt_belt_connection(self, design_entity: '_1953.CVTBeltConnection') -> 'Iterable[_5504.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5504.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_belt_connection(self, design_entity: '_1948.BeltConnection') -> 'Iterable[_5473.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5473.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_coaxial_connection(self, design_entity: '_1949.CoaxialConnection') -> 'Iterable[_5488.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5488.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_connection(self, design_entity: '_1952.Connection') -> 'Iterable[_5499.ConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5499.ConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1961.InterMountableComponentConnection') -> 'Iterable[_5529.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5529.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_planetary_connection(self, design_entity: '_1967.PlanetaryConnection') -> 'Iterable[_5547.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5547.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_rolling_ring_connection(self, design_entity: '_1972.RollingRingConnection') -> 'Iterable[_5557.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5557.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_1945.AbstractShaftToMountableComponentConnection') -> 'Iterable[_5467.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5467.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1981.BevelDifferentialGearMesh') -> 'Iterable[_5476.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5476.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_gear_mesh(self, design_entity: '_1985.ConceptGearMesh') -> 'Iterable[_5494.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5494.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_face_gear_mesh(self, design_entity: '_1991.FaceGearMesh') -> 'Iterable[_5518.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5518.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_2005.StraightBevelDiffGearMesh') -> 'Iterable[_5570.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5570.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_bevel_gear_mesh(self, design_entity: '_1983.BevelGearMesh') -> 'Iterable[_5481.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5481.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_conical_gear_mesh(self, design_entity: '_1987.ConicalGearMesh') -> 'Iterable[_5497.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5497.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1979.AGMAGleasonConicalGearMesh') -> 'Iterable[_5469.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5469.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1989.CylindricalGearMesh') -> 'Iterable[_5512.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5512.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1995.HypoidGearMesh') -> 'Iterable[_5527.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5527.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1998.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5531.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5531.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1999.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5534.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5534.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5537.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5537.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_2003.SpiralBevelGearMesh') -> 'Iterable[_5564.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5564.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_2007.StraightBevelGearMesh') -> 'Iterable[_5573.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5573.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_worm_gear_mesh(self, design_entity: '_2009.WormGearMesh') -> 'Iterable[_5588.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5588.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_2011.ZerolBevelGearMesh') -> 'Iterable[_5591.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5591.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_gear_mesh(self, design_entity: '_1993.GearMesh') -> 'Iterable[_5523.GearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.GearMeshCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5523.GearMeshCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_2015.CycloidalDiscCentralBearingConnection') -> 'Iterable[_5508.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5508.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_2018.CycloidalDiscPlanetaryBearingConnection') -> 'Iterable[_5510.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5510.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_ring_pins_to_disc_connection(self, design_entity: '_2021.RingPinsToDiscConnection') -> 'Iterable[_5554.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5554.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_2028.PartToPartShearCouplingConnection') -> 'Iterable[_5545.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5545.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_clutch_connection(self, design_entity: '_2022.ClutchConnection') -> 'Iterable[_5486.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5486.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_concept_coupling_connection(self, design_entity: '_2024.ConceptCouplingConnection') -> 'Iterable[_5491.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5491.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation))

    def results_for_coupling_connection(self, design_entity: '_2026.CouplingConnection') -> 'Iterable[_5502.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5502.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation))
