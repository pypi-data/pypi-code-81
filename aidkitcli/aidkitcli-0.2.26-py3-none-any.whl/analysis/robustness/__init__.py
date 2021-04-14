"""The robustness pillar groups analyses that assess how the AI model responds
to small noise (perturbations) in the input. Here, aidkit offers adversarial
as well as corruption stress tests, i.e. optimization-based and
non-optimization based methods.
"""
from aidkitcli.analysis.robustness.kri import kri
from aidkitcli.analysis.robustness.fgsm import fgsm
from aidkitcli.analysis.robustness.peak import peak
from aidkitcli.analysis.robustness.random import random
from aidkitcli.analysis.robustness.increase import increase
from aidkitcli.analysis.robustness.constant import constant
from aidkitcli.analysis.robustness.blackbox import blackbox
from aidkitcli.analysis.robustness.correlation import correlation
from aidkitcli.analysis.robustness.relative_constant import relative_constant
from aidkitcli.analysis.robustness.aggregated_constant import aggregated_constant
from aidkitcli.analysis.robustness.aggregated_relative_constant import aggregated_relative_constant
