# Standard Library
from functools import reduce
from operator import mul


def constant(k):
    return k


###############################################################################
# Mass Action
###############################################################################


def mass_action_1(S1, k_fwd):
    return k_fwd * S1


def mass_action_2(S1, S2, k_fwd):
    return k_fwd * S1 * S2


def mass_action_3(S1, S2, S3, k_fwd):
    return k_fwd * S1 * S2 * S3


def mass_action_4(S1, S2, S3, S4, k_fwd):
    return k_fwd * S1 * S2 * S3 * S4


def mass_action_variable(*args):
    return reduce(mul, args, 1)


###############################################################################
# Reversible Mass Action
###############################################################################


def reversible_mass_action_1_1(S1, P1, k_fwd, k_bwd):
    return k_fwd * S1 - k_bwd * P1


def reversible_mass_action_2_1(S1, S2, P1, k_fwd, k_bwd):
    return k_fwd * S1 * S2 - k_bwd * P1


def reversible_mass_action_3_1(S1, S2, S3, P1, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 - k_bwd * P1


def reversible_mass_action_4_1(S1, S2, S3, S4, P1, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 * S4 - k_bwd * P1


def reversible_mass_action_1_2(S1, P1, P2, k_fwd, k_bwd):
    return k_fwd * S1 - k_bwd * P1 * P2


def reversible_mass_action_2_2(S1, S2, P1, P2, k_fwd, k_bwd):
    return k_fwd * S1 * S2 - k_bwd * P1 * P2


def reversible_mass_action_3_2(S1, S2, S3, P1, P2, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 - k_bwd * P1 * P2


def reversible_mass_action_4_2(S1, S2, S3, S4, P1, P2, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 * S4 - k_bwd * P1 * P2


def reversible_mass_action_1_3(S1, P1, P2, P3, k_fwd, k_bwd):
    return k_fwd * S1 - k_bwd * P1 * P2 * P3


def reversible_mass_action_2_3(S1, S2, P1, P2, P3, k_fwd, k_bwd):
    return k_fwd * S1 * S2 - k_bwd * P1 * P2 * P3


def reversible_mass_action_3_3(S1, S2, S3, P1, P2, P3, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 - k_bwd * P1 * P2 * P3


def reversible_mass_action_4_3(S1, S2, S3, S4, P1, P2, P3, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 * S4 - k_bwd * P1 * P2 * P3


def reversible_mass_action_1_4(S1, P1, P2, P3, P4, k_fwd, k_bwd):
    return k_fwd * S1 - k_bwd * P1 * P2 * P3 * P4


def reversible_mass_action_2_4(S1, S2, P1, P2, P3, P4, k_fwd, k_bwd):
    return k_fwd * S1 * S2 - k_bwd * P1 * P2 * P3 * P4


def reversible_mass_action_3_4(S1, S2, S3, P1, P2, P3, P4, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 - k_bwd * P1 * P2 * P3 * P4


def reversible_mass_action_4_4(S1, S2, S3, S4, P1, P2, P3, P4, k_fwd, k_bwd):
    return k_fwd * S1 * S2 * S3 * S4 - k_bwd * P1 * P2 * P3 * P4


def reversible_mass_action_variable_1(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:1]
    products = metabolites[1:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_2(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:2]
    products = metabolites[2:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_3(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:3]
    products = metabolites[3:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_4(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:4]
    products = metabolites[4:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_5(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:5]
    products = metabolites[5:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_6(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:6]
    products = metabolites[6:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_7(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:7]
    products = metabolites[7:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


def reversible_mass_action_variable_8(*args):
    *metabolites, k_fwd, k_bwd = args
    substrates = metabolites[:8]
    products = metabolites[8:]
    return k_fwd * reduce(mul, substrates, 1) - k_bwd * reduce(mul, products, 1)


###############################################################################
# Michaelis Menten
###############################################################################


def michaelis_menten(S, vmax, km):
    return S * vmax / (S + km)


def competitive_inhibition(S, I, vmax, km, ki):
    return vmax * S / (S + km * (1 + I / ki))


def competitive_activation(S, A, vmax, km, ka):
    return vmax * S / (S + km * (1 + ka / A))


def uncompetitive_inhibition(S, I, vmax, km, ki):
    return vmax * S / (S * (1 + I / ki) + km)


def uncompetitive_activation(S, A, vmax, km, ka):
    return vmax * S / (S * (1 + ka / A) + km)


def noncompetitive_inhibition(S, I, vmax, km, ki):
    return vmax * S / ((S + km) * (1 + I / ki))


def noncompetitive_activation(S, A, vmax, km, ka):
    return vmax * S / ((S + km) * (1 + ka / A))


def mixed_inhibition(S, I, vmax, km, ki):
    return vmax * S / (S * (1 + I / ki) + km * (1 + I / ki))


def mixed_activation(S, A, vmax, km, ka):
    return vmax * S / (S * (1 + ka / A) + km * (1 + ka / A))


###############################################################################
# Reversible Michaelis-Menten
###############################################################################


def reversible_michaelis_menten(S, P, vmax_fwd, vmax_bwd, kms, kmp):
    return (vmax_fwd * S / kms - vmax_bwd * P / kmp) / (1 + S / kms + P / kmp)


def reversible_uncompetitive_inhibition(S, P, I, vmax_fwd, vmax_bwd, kms, kmp, ki):
    return (vmax_fwd * S / kms - vmax_bwd * P / kmp) / (1 + (S / kms) + (P / kmp) * (1 + I / ki))


def reversible_noncompetitive_inhibition(S, P, I, vmax_fwd, vmax_bwd, kms, kmp, ki):
    return (vmax_fwd * S / kms - vmax_bwd * P / kmp) / ((1 + S / kms + P / kmp) * (1 + I / ki))


def reversible_michaelis_menten_keq(S, P, vmax_fwd, kms, kmp, keq):
    return vmax_fwd / kms * (S - P / keq) / (1 + S / kms + P / kmp)


def reversible_uncompetitive_inhibition_keq(S, P, I, vmax_fwd, kms, kmp, ki, keq):
    return vmax_fwd / kms * (S - P / keq) / (1 + (S / kms) + (P / kmp) * (1 + I / ki))


def reversible_noncompetitive_inhibition_keq(S, P, I, vmax_fwd, kms, kmp, ki, keq):
    return vmax_fwd / kms * (S - P / keq) / ((1 + S / kms + P / kmp) * (1 + I / ki))


###############################################################################
# Multi-substrate
###############################################################################


def ordered_2(A, B, vmax, kmA, kmB, kiA):
    return vmax * A * B / (A * B + kmB * A + kmA * B + kiA * kmB)


def ordered_2_2(A, B, P, Q, vmaxf, vmaxr, kmA, kmB, kmP, kmQ, kiA, kiB, kiP, kiQ):
    nominator = vmaxf * A * B / (kiA * kmB) - vmaxr * P * Q / (kmP * kiQ)
    denominator = (
        1
        + (A / kiA)
        + (kmA * B / (kiA * kmB))
        + (kmQ * P / (kmP * kiQ))
        + (Q / kiQ)
        + (A * B / (kiA * kmB))
        + (kmQ * A * P / (kiA * kmP * kiQ))
        + (kmA * B * Q / (kiA * kmB * kiQ))
        + (P * Q / (kmP * kiQ))
        + (A * B * P / (kiA * kmB * kiP))
        + (B * P * Q) / (kiB * kmP * kiQ)
    )
    return nominator / denominator


def random_order_2(A, B, vmax, kmA, kmB, kiA):
    return vmax * A * B / (A * B + kmB * A + kmA * B + kiA * kmB)


def random_order_2_2(A, B, P, Q, vmaxf, vmaxr, kmB, kmP, kiA, kiB, kiP, kiQ):
    nominator = vmaxf * A * B / (kiA * kmB) - vmaxr * P * Q / (kmP * kiQ)
    denominator = 1 + (A / kiA) + (B / kiB) + (P / kiP) + (Q / kiQ) + (A * B / (kiA * kmB)) + (P * Q / (kmP * kiQ))
    return nominator / denominator


def ping_pong_2(A, B, vmax, kmA, kmB):
    return vmax * A * B / (A * B + kmA * B + kmB * A)


def ping_pong_3(A, B, C, vmax, kmA, kmB, kmC):
    return (vmax * A * B * C) / (A * B * C + (kmA * B * C) + (kmB * A * C) + (kmC * A * B))


def ping_pong_4(A, B, C, D, vmax, kmA, kmB, kmC, kmD):
    return (vmax * A * B * C * D) / (
        A * B * C * D + (kmA * B * C * D) + (kmB * A * C * D) + (kmC * A * B * D) + (kmD * A * B * C)
    )


###############################################################################
# Cooperativity
###############################################################################


def hill(S, vmax, kd, n):
    return vmax * S ** n / (kd + S ** n)


###############################################################################
# Generalised
###############################################################################

# def hanekom():
#     pass

# def convenience():
#     pass
