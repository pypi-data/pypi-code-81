import asyncio
import itertools
from typing import TYPE_CHECKING

import aiomultiprocess
from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSStoppingRun(RunGovernorState):
    """Represents the STOPPING_RUN state.

    Possible next states are
    * :class:`.RGSFinalizing` in the default case.
    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STOPPING_RUN")

    async def run(self):
        await self._stop_processes()

    def next_state(self):
        from . import RGSFinalizing

        self.rgc.state = RGSFinalizing(self.rgc)

    async def _stop_processes(self):
        all_processes = [
            p
            for p in itertools.chain(
                self.rgc.sim_controllers.values(),
                self.rgc.env_conductors.values(),
                self.rgc.agent_conductors.values(),
            )
        ]
        try:
            await asyncio.wait(
                [
                    asyncio.create_task(self._join_process(p))
                    for p in all_processes
                ],
                return_when=asyncio.ALL_COMPLETED,
                timeout=15,
            )
        except asyncio.TimeoutError as e:
            LOG.warn(
                "RunGovernor(id=0x%x, uid=%s) "
                "saw a timeout while waiting for all remaining processes "
                "terminate peacefully; will continue to reap: %s",
                id(self.rgc),
                self.rgc.uid,
                e,
            )

    async def _join_process(self, process: aiomultiprocess.Process):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) "
            "monitoring Process(name=%s, is_alive=%s)",
            id(self.rgc),
            self.rgc.uid,
            process.name,
            process.is_alive(),
        )
        while process.exitcode is None:
            await asyncio.sleep(5)
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "joined Process(name=%s, is_alive=%s, exitcode=%s, PID=%s)",
                id(self.rgc),
                self.rgc.uid,
                process.name,
                process.is_alive(),
                process.exitcode,
                process.pid,
            )
