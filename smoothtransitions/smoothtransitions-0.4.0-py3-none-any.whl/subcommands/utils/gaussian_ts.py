import numpy as np
from cclib.parser.data import ccData_optdone_bool
from cclib.parser.gaussianparser import Gaussian
from cclib.parser.utils import PeriodicTable

periodic_table = PeriodicTable()


class GaussianTS(Gaussian):
    """A Gaussian 98/03 log file with additional functions."""

    def __init__(self, *args, **kwargs):

        # Call the __init__ method of the superclass
        super(Gaussian, self).__init__(datatype=ccData_gaussian_ts, *args, **kwargs)


class ccData_gaussian_ts(ccData_optdone_bool):
    def __init__(self, *args, **kwargs):
        super(ccData_gaussian_ts, self).__init__(*args, **kwargs)
        self.atomelements = self.get_elements()

    def calculate_distances(self, atoms):
        """Takes a tuple of atom indicies at returns their distances.

        This is done for all structues in the logfile.

        Args:
            atoms (tuple): atom index of the atoms between which the distances
                should be calculated.
        """
        distances = np.linalg.norm(
            self.atomcoords[:, atoms[0]] - self.atomcoords[:, atoms[1]], axis=1
        )
        return distances

    def get_elements(self):
        try:
            return [periodic_table.element[a] for a in self.atomnos]
        except KeyError:
            return None

    @property
    def opt_done(self):
        return (
            hasattr(self, "optdone")
            and self.optdone
            and "success" in self.metadata.keys()
            and self.metadata["success"]
        )

    @property
    def freq_done(self):
        return (
            hasattr(self, "vibfreqs")
            and "success" in self.metadata.keys()
            and self.metadata["success"]
        )

    # according to https://gaussian.com/faq3/ the first definition
    # of a stationary point is that all values of the last
    # optimised structure are below the target thresholds
    @property
    def stationary_full(self):
        return (
            self.opt_done
            and self.freq_done
            and (self.geovalues[-1] < self.geotargets).all()
        )

    # according to https://gaussian.com/faq3/ the second definition
    # of a stationary point is that Maximum and RMS Force values of the last
    # optimised structure are two orders of magnitude smaller than their target
    # thresholds
    @property
    def stationary_close_enough(self):
        return (
            self.opt_done
            and self.freq_done
            and (self.geovalues[-1, :2] < self.geotargets[:2] / 1e2).all()
        )

    @property
    def is_spe(self):
        return (
            not hasattr(self, "optdone")
            and self.atomcoords.shape[0] == 1
            and len(self.scfenergies) == 1
        )

    @property
    def spe_done(self):
        return (
            self.is_spe
            and "success" in self.metadata.keys()
            and self.metadata["success"]
        )

    @property
    def is_constrained(self):
        return hasattr(self, "constraints")
