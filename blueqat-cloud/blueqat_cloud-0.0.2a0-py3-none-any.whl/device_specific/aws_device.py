from typing import Optional

from blueqat import Circuit
from bqbraket import convert

from braket.device_schema import GateModelParameters
from braket.device_schema.ionq import IonqDeviceParameters
from braket.device_schema.rigetti import RigettiDeviceParameters
#from braket.device_schema.simulators import GateModelSimulatorDeviceParameters

from ..device import Device
from ..data import ExecutionRequest


def make_executiondata(c: Circuit, dev: Device, shots: int, group: Optional[str],
        send_email: bool) -> ExecutionRequest:
    action = convert(c).to_ir().json()
    dev_params = make_device_params(c, dev)
    return ExecutionRequest(action, dev.value, dev_params, shots, group, send_email)


def make_device_params(c: Circuit, dev: Device) -> str:
    paradigm_params = GateModelParameters(qubitCount=c.n_qubits,
                                          disableQubitRewiring=False)
    if "/rigetti/" in dev.value:
        return RigettiDeviceParameters(
            paradigmParameters=paradigm_params).json()
    if "/ionq/" in dev.value:
        return IonqDeviceParameters(paradigmParameters=paradigm_params).json()
    raise ValueError("Unknown AWS device.")
