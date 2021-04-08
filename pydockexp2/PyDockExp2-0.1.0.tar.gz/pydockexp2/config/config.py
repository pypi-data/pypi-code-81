import configparser
from dataclasses import dataclass, field
import asyncio
# from tqdm import tqdm
import rich
from rich.progress import track
from typing import List, Dict
import logging
import os
import os.path as osp
import errno


DEFAULT_CONF = "/home/lmriccardo/Scrivania/Tuts/Python/PyDocker/config/sample/simple.conf"


@dataclass(frozen=True)
class Configuration:
    # Field without default value
    mnumb: int
    name:  str
    
    # Field with default value
    ncols: int  = field(default=2)
    nrows: int  = field(default=2)
    mtype: int  = field(default=0)
    savem: bool = field(default=False)
    nfile: str  = field(default_factory=str) 


class ConfigExtrapolator:

    def __init__(self, logger: logging.Logger, conf_file: str = DEFAULT_CONF):
        self.conf_file = conf_file
        self.logger    = logger

        # Controllo l'esistenza del file di configurazione
        if not osp.isfile(self.conf_file):
            raise FileNotFoundError(errno.ENOENT, "", self.conf_file)

        # Carico la configurazione
        self.parsing   = configparser.ConfigParser()
        self.parsing.read(self.conf_file)
        self.logger.debug("Loaded {} configuration file".format(self.conf_file))

    async def extract_configuration(self) -> List[Configuration]:
        configurations = list()
        for x in track(self.parsing.sections(), description="Extracting from {}".format(self.conf_file)):
            section = self.parsing[x]
            ncols   = section['ncols'].split(",")
            nrows   = section['nrows'].split(",")
            mtype   = section['mtype'].split(",")
            mnumb   = section['mnumb'].split(",")
            onfile  = section['onfile'].split(",")

            # Se abbiamo una multi configurazione
            for i in range(len(ncols)):
                c = Configuration(
                    name=section,
                    ncols=int(ncols[i]),
                    nrows=int(nrows[i]),
                    mtype=int(mtype[i]),
                    savem=(onfile[i] != "false"),
                    nfile="" if onfile[i] == "false" else onfile[i],
                    mnumb=int(mnumb[i])
                )
                configurations.append(c)
            
        return configurations

    @staticmethod
    async def extrapolate_from_list(files: List[str], logger: logging.Logger) -> Dict[str, List[Configuration]]:
        configurations_dict = {}
        tasks = []

        # Creo un event-loop per ogni configurazione da estrapolare
        for conf_file in files:
            ce = ConfigExtrapolator(logger, conf_file)
            tasks.append(asyncio.create_task(ce.extract_configuration()))

        # Faccio gli await per ottenere i diversi valori di ritorno
        for idx, task in enumerate(tasks):
            configurations_dict[files[idx]] = await task

        return configurations_dict