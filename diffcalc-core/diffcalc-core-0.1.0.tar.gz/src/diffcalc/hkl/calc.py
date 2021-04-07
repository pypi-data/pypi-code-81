"""Routines for calculating miller indices and diffractometer positions.

Module implementing calculations based on UB matrix data and diffractometer
constraints.
"""
from itertools import product
from math import acos, asin, atan, atan2, cos, isnan, pi, sin, sqrt, tan
from typing import Dict, Iterator, List, Optional, Tuple

import numpy as np
from diffcalc.hkl.geometry import (
    Position,
    get_rotation_matrices,
    rot_CHI,
    rot_ETA,
    rot_MU,
    rot_PHI,
)
from diffcalc.log import logging
from diffcalc.util import (
    SMALL,
    TODEG,
    DiffcalcException,
    I,
    angle_between_vectors,
    bound,
    cross3,
    is_small,
    normalised,
    radians_equivalent,
    sign,
    x_rotation,
    y_rotation,
    z_rotation,
)
from numpy.linalg import inv, norm

logger = logging.getLogger("diffcalc.hkl.calc")


class HklCalculation:
    """Class for converting between miller indices and diffractometer position.

    Attributes
    ----------
    ubcalc: UBcalculation
        Reference to UBcalculation object containing UB matrix data.
    constraints:
        Reference to Constraints object containing diffractometer constraint settings.

    Methods
    -------
    get_hkl(pos: Position, wavelength: float) -> Tuple[float, float, float]
        Calculate miller indices corresponding to a diffractometer positions.
    get_virtual_angles(pos: Position) -> Dict[str,float]
        Calculate pseudo-angles corresponding to a diffractometer position.
    """

    def __init__(self, ubcalc, constraints):
        self.ubcalc = ubcalc  # to get the UBMatrix
        self.constraints = constraints

    def __str__(self):
        """Return string representing class instance.

        Returns
        -------
        str:
            String representation of constraints table.
        """
        return self.constraints.__str__()

    def __repr_mode(self):
        return repr(self.constraints.asdict)

    def get_hkl(self, pos: Position, wavelength: float) -> Tuple[float, float, float]:
        """Calculate miller indices corresponding to a diffractometer positions.
        
        Parameters
        ----------
        pos: Position
            Diffractometer position

        Returns
        -------
        Tuple[float, float, float]
            Miller indices corresponding to the specified diffractometer
            position at the given wavelength.
        """
        [MU, DELTA, NU, ETA, CHI, PHI] = get_rotation_matrices(pos)

        q_lab = (NU @ DELTA - I) @ np.array([[0], [2 * pi / wavelength], [0]])  # 12

        hkl = inv(self.ubcalc.UB) @ inv(PHI) @ inv(CHI) @ inv(ETA) @ inv(MU) @ q_lab

        return hkl[0, 0], hkl[1, 0], hkl[2, 0]

    def get_virtual_angles(self, pos: Position) -> Dict[str, float]:
        """Calculate pseudo-angles corresponding to a diffractometer position.

        Parameters
        ----------
        pos: Position
            Diffractometer position

        Returns
        -------
        Dict[str, float]
            Returns alpha, beta, betain, betaout, naz, psi, qaz, tau, theta and
            ttheta angles.
        """
        theta, qaz = self._theta_and_qaz_from_detector_angles(pos.delta, pos.nu)  # (19)

        [MU, DELTA, NU, ETA, CHI, PHI] = get_rotation_matrices(pos)
        Z = MU @ ETA @ CHI @ PHI
        D = NU @ DELTA

        # Compute incidence and outgoing angles bin and betaout
        surf_nphi = Z @ self.ubcalc.surf_nphi
        kin = np.array([[0], [1], [0]])
        kout = D @ np.array([[0], [1], [0]])
        betain = angle_between_vectors(kin, surf_nphi) - pi / 2.0
        betaout = pi / 2.0 - angle_between_vectors(kout, surf_nphi)

        n_lab = Z @ self.ubcalc.n_phi
        alpha = asin(bound(-n_lab[1, 0]))
        naz = atan2(n_lab[0, 0], n_lab[2, 0])  # (20)

        cos_tau = cos(alpha) * cos(theta) * cos(naz - qaz) + sin(alpha) * sin(theta)
        tau = acos(bound(cos_tau))  # (23)

        # Compute Tau using the dot product directly (THIS ALSO WORKS)
        # q_lab = ( (NU @ DELTA - I ) @ np.array([[0],[1],[0]])
        # norm = norm(q_lab)
        # q_lab = np.array([[1],[0],[0]]) if norm == 0 else q_lab * (1/norm)
        # tau_from_dot_product = acos(bound(dot3(q_lab, n_lab)))

        sin_beta = 2 * sin(theta) * cos(tau) - sin(alpha)
        beta = asin(bound(sin_beta))  # (24)

        psi = next(self._calc_psi(alpha, theta, tau, qaz, naz))

        return {
            "theta": theta,
            "ttheta": 2 * theta,
            "qaz": qaz,
            "alpha": alpha,
            "naz": naz,
            "tau": tau,
            "psi": psi,
            "beta": beta,
            "betain": betain,
            "betaout": betaout,
        }

    def get_position(
        self, h: float, k: float, l: float, wavelength: float
    ) -> List[Tuple[Position, Dict[str, float]]]:
        """Calculate diffractometer position from miller indices and wavelength.

        The calculated positions and angles are verified by checking that they 
        map to the requested miller indices.

        Parameters
        ----------
            h: float
                h miller index
            k: float
                k miller index
            l: float
                l miller index
            wavelength: float
                wavelength in Angstroms

        Returns
        -------
            List[Tuple[Position, Dict[str, float]]]
                List of all solutions matching the input miller indices that
                consists of pairs of diffractometer position object and virtual
                angles dictionary.
        """
        pos_virtual_angles_pairs = self._calc_hkl_to_position(h, k, l, wavelength)
        assert pos_virtual_angles_pairs
        pos_virtual_angles_pairs_in_degrees = []

        for pos_virtual_angles in pos_virtual_angles_pairs:
            self._verify_pos_map_to_hkl(h, k, l, wavelength, pos_virtual_angles[0])
            self._verify_virtual_angles(h, k, l, *pos_virtual_angles)
            pos_virtual_angles_pairs_in_degrees.append(pos_virtual_angles)

        return pos_virtual_angles_pairs_in_degrees

    def _calc_hkl_to_position(
        self, h: float, k: float, l: float, wavelength: float
    ) -> List[Tuple[Position, Dict[str, float]]]:
        if not self.constraints.is_fully_constrained():
            raise DiffcalcException(
                "Diffcalc is not fully constrained.\n"
                "Type 'help con' for instructions"
            )

        if not self.constraints.is_current_mode_implemented():
            raise DiffcalcException(
                "Sorry, the selected constraint combination is valid but "
                "is not implemented. Type 'help con' for implemented combinations"
            )

        # constraints are dictionaries
        ref_constraint = self.constraints._reference
        if ref_constraint:
            ref_constraint_name, ref_constraint_value = next(
                iter(ref_constraint.items())
            )
        det_constraint = self.constraints._detector
        naz_constraint = {"naz": self.constraints.naz} if self.constraints.naz else None
        samp_constraints = self.constraints._sample

        assert not (
            det_constraint and naz_constraint
        ), "Two 'detector' constraints given"

        h_phi = self.ubcalc.UB @ np.array([[h], [k], [l]])
        theta = (
            self.ubcalc.get_ttheta_from_hkl((h, k, l), 12.39842 / wavelength) / 2.0
        )  # __calc_theta(h_phi, wavelength)
        tau = angle_between_vectors(h_phi, self.ubcalc.n_phi)
        surf_tau = angle_between_vectors(h_phi, self.ubcalc.surf_nphi)

        if is_small(sin(tau)) and ref_constraint:
            if ref_constraint_name == "psi":
                raise DiffcalcException(
                    "Azimuthal angle 'psi' is undefined as reference and scattering vectors parallel.\n"
                    "Please constrain one of the sample angles or choose different reference vector orientation."
                )
            elif ref_constraint_name == "a_eq_b":
                raise DiffcalcException(
                    "Reference constraint 'a_eq_b' is redundant as reference and scattering vectors are parallel.\n"
                    "Please constrain one of the sample angles or choose different reference vector orientation."
                )
        if (
            is_small(sin(surf_tau))
            and ref_constraint
            and ref_constraint_name == "bin_eq_bout"
        ):
            raise DiffcalcException(
                "Reference constraint 'bin_eq_bout' is redundant as scattering vectors is parallel to the surface normal.\n"
                "Please select another constrain to define sample azimuthal orientation."
            )

        ### Reference constraint column ###

        n_phi = self.ubcalc.n_phi
        if ref_constraint:
            if {"psi", "a_eq_b", "alpha", "beta"}.issuperset(ref_constraint.keys()):
                # An angle for the reference vector (n) is given      (Section 5.2)
                alpha, _ = self._calc_remaining_reference_angles(
                    ref_constraint_name, ref_constraint_value, theta, tau
                )
            elif {"bin_eq_bout", "betain", "betaout"}.issuperset(ref_constraint.keys()):
                alpha, _ = self._calc_remaining_reference_angles(
                    ref_constraint_name, ref_constraint_value, theta, surf_tau
                )
                tau = surf_tau
                n_phi = self.ubcalc.surf_nphi

        solution_tuples = []
        if det_constraint or naz_constraint:

            if len(samp_constraints) == 1:
                for (
                    qaz,
                    naz,
                    delta,
                    nu,
                ) in self._calc_det_angles_given_det_or_naz_constraint(
                    det_constraint, naz_constraint, theta, tau, alpha
                ):
                    for (
                        mu,
                        eta,
                        chi,
                        phi,
                    ) in self._calc_sample_angles_from_one_sample_constraint(
                        samp_constraints, h_phi, theta, alpha, qaz, naz, n_phi
                    ):
                        solution_tuples.append((mu, delta, nu, eta, chi, phi))

            elif len(samp_constraints) == 2:
                if det_constraint:
                    det_constraint_name, det_constraint_val = next(
                        iter(det_constraint.items())
                    )
                    for delta, nu, qaz in self._calc_remaining_detector_angles(
                        det_constraint_name, det_constraint_val, theta
                    ):
                        for (
                            mu,
                            eta,
                            chi,
                            phi,
                        ) in self._calc_sample_angles_given_two_sample_and_detector(
                            samp_constraints, qaz, theta, h_phi, n_phi
                        ):
                            solution_tuples.append((mu, delta, nu, eta, chi, phi))

                else:
                    raise DiffcalcException(
                        "No code yet to handle this combination of detector and sample constraints!"
                    )

        elif len(samp_constraints) == 2:
            if ref_constraint_name == "psi":
                psi_vals = iter(
                    [
                        ref_constraint_value,
                    ]
                )
            else:
                psi_vals = self._calc_psi(alpha, theta, tau)
            for psi in psi_vals:
                solution_tuples.extend(
                    self._calc_sample_given_two_sample_and_reference(
                        samp_constraints, h_phi, theta, psi, n_phi
                    )
                )

        elif len(samp_constraints) == 3:
            solution_tuples.extend(
                self._calc_angles_given_three_sample_constraints(
                    samp_constraints,
                    h_phi,
                    theta,
                )
            )

        if not solution_tuples:
            raise DiffcalcException(
                "No solutions were found. "
                "Please consider using an alternative set of constraints."
            )

        tidy_solutions = [
            self._tidy_degenerate_solutions(Position(*pos)) for pos in solution_tuples
        ]

        # def _find_duplicate_angles(el):
        #    idx, tpl = el
        #    for tmp_tpl in filtered_solutions[idx:]:
        #        if False not in [abs(x-y) < SMALL for x,y in zip(tmp_tpl, tpl)]:
        #            return False
        #    return True
        # merged_solution_tuples = filter(_find_duplicate_angles, enumerate(filtered_solutions, 1))
        position_pseudo_angles_pairs = self._create_position_pseudo_angles_pairs(
            tidy_solutions
        )
        if not position_pseudo_angles_pairs:
            raise DiffcalcException(
                "No solutions were found. Please consider using "
                "an alternative pseudo-angle constraints."
            )

        return position_pseudo_angles_pairs

    def _create_position_pseudo_angles_pairs(
        self, merged_solution_tuples: List[Position]
    ) -> List[Tuple[Position, Dict[str, float]]]:

        position_pseudo_angles_pairs = []
        for position in merged_solution_tuples:
            # Create position
            # position = self._tidy_degenerate_solutions(position)
            # if position.phi <= -pi + SMALL:
            #    position.phi += 2 * pi
            # pseudo angles calculated along the way were for the initial solution
            # and may be invalid for the chosen solution TODO: anglesToHkl need no
            # longer check the pseudo_angles as they will be generated with the
            # same function and it will prove nothing
            pseudo_angles = self.get_virtual_angles(position)
            try:
                for constraint in [
                    self.constraints._reference,
                    self.constraints._detector,
                ]:
                    for constraint_name, constraint_value in constraint.items():
                        if constraint_name == "a_eq_b":
                            assert radians_equivalent(
                                pseudo_angles["alpha"], pseudo_angles["beta"]
                            )
                        elif constraint_name == "bin_eq_bout":
                            assert radians_equivalent(
                                pseudo_angles["betain"], pseudo_angles["betaout"]
                            )
                        elif constraint_name not in pseudo_angles:
                            continue
                        else:
                            assert radians_equivalent(
                                constraint_value, pseudo_angles[constraint_name]
                            )
                position_pseudo_angles_pairs.append((position, pseudo_angles))
            except AssertionError:
                continue
        return position_pseudo_angles_pairs

    def _calc_N(self, Q: np.ndarray, n: np.ndarray) -> np.ndarray:
        """Return N as described by Equation 31."""
        Q = normalised(Q)
        n = normalised(n)
        if is_small(angle_between_vectors(Q, n)):
            # Replace the reference vector with an alternative vector from Eq.(78)
            def __key_func(v):
                return v[1]  # Workaround for mypy issue #9590

            idx_min, _ = min(
                enumerate([abs(Q[0, 0]), abs(Q[1, 0]), abs(Q[2, 0])]),
                key=__key_func,
            )
            idx_1, idx_2 = [idx for idx in range(3) if idx != idx_min]
            qval = sqrt(Q[idx_1, 0] * Q[idx_1, 0] + Q[idx_2, 0] * Q[idx_2, 0])
            n[idx_min, 0] = qval
            n[idx_1, 0] = -Q[idx_min, 0] * Q[idx_1, 0] / qval
            n[idx_2, 0] = -Q[idx_min, 0] * Q[idx_2, 0] / qval
            if is_small(norm(n)):
                n[idx_min, 0] = 0
                n[idx_1, 0] = Q[idx_2, 0] / qval
                n[idx_2, 0] = -Q[idx_1, 0] / qval
        Qxn = cross3(Q, n)
        QxnxQ = cross3(Qxn, Q)
        QxnxQ = normalised(QxnxQ)
        Qxn = normalised(Qxn)
        return np.array(
            [
                [Q[0, 0], QxnxQ[0, 0], Qxn[0, 0]],
                [Q[1, 0], QxnxQ[1, 0], Qxn[1, 0]],
                [Q[2, 0], QxnxQ[2, 0], Qxn[2, 0]],
            ]
        )

    def _calc_angle_between_naz_and_qaz(
        self, theta: float, alpha: float, tau: float
    ) -> float:
        # Equation 30:
        top = cos(tau) - sin(alpha) * sin(theta)
        bottom = cos(alpha) * cos(theta)
        if is_small(bottom):
            if is_small(cos(alpha)):
                raise ValueError("cos(alpha) is too small")
            if is_small(cos(theta)):
                raise ValueError("cos(theta) is too small")
        if is_small(sin(tau)):
            return 0.0
        return acos(bound(top / bottom))

    def _calc_psi(
        self,
        alpha: float,
        theta: float,
        tau: float,
        qaz: Optional[float] = None,
        naz: Optional[float] = None,
    ) -> Iterator[float]:
        """Calculate psi from Eq. (18), (25) and (28)."""
        sin_tau = sin(tau)
        cos_theta = cos(theta)
        if is_small(sin_tau):
            # The reference vector is parallel to the scattering vector
            yield float("nan")
        elif is_small(cos_theta):
            # Reflection is unreachable as theta angle is too close to 90 deg
            yield float("nan")
        elif is_small(sin(theta)):
            # Reflection is unreachable as |Q| is too small
            yield float("nan")
        else:
            cos_psi = (cos(tau) * sin(theta) - sin(alpha)) / cos_theta  # (28)
            if qaz is None or naz is None:
                try:
                    acos_psi = acos(bound(cos_psi / sin_tau))
                    if is_small(acos_psi):
                        yield 0.0
                    else:
                        for psi in [acos_psi, -acos_psi]:
                            yield psi
                except AssertionError:
                    print("WARNING: Diffcalc could not calculate an azimuth (psi)")
                    yield float("nan")
            else:
                sin_psi = cos(alpha) * sin(qaz - naz)
                sgn = sign(sin_tau)
                eps = sin_psi ** 2 + cos_psi ** 2
                sigma_ = eps / sin_tau ** 2 - 1
                if not is_small(sigma_):
                    print(
                        "WARNING: Diffcalc could not calculate a unique azimuth "
                        "(psi) because of loss of accuracy in numerical calculation"
                    )
                    yield float("nan")
                else:
                    psi = atan2(sgn * sin_psi, sgn * cos_psi)
                    yield psi

    def _calc_remaining_reference_angles(
        self, name: str, value: float, theta: float, tau: float
    ) -> Tuple[float, float]:
        """Return alpha and beta given one of a_eq_b, alpha, beta or psi."""
        UNREACHABLE_MSG = (
            "The current combination of constraints with %s = %.4f\n"
            "prohibits a solution for the specified reflection."
        )
        if name == "psi":
            psi = value
            # Equation 26 for alpha
            sin_alpha = cos(tau) * sin(theta) - cos(theta) * sin(tau) * cos(psi)
            if abs(sin_alpha) > 1 + SMALL:
                raise DiffcalcException(UNREACHABLE_MSG % (name, value * TODEG))
            alpha = asin(bound(sin_alpha))
            # Equation 27 for beta
            sin_beta = cos(tau) * sin(theta) + cos(theta) * sin(tau) * cos(psi)
            if abs(sin_beta) > 1 + SMALL:
                raise DiffcalcException(UNREACHABLE_MSG % (name, value * TODEG))

            beta = asin(bound(sin_beta))

        elif name == "a_eq_b" or name == "bin_eq_bout":
            alpha = beta = asin(cos(tau) * sin(theta))  # (24)

        elif name == "alpha" or name == "betain":
            alpha = value  # (24)
            sin_beta = 2 * sin(theta) * cos(tau) - sin(alpha)
            if abs(sin_beta) > 1 + SMALL:
                raise DiffcalcException(UNREACHABLE_MSG % (name, value * TODEG))
            beta = asin(sin_beta)

        elif name == "beta" or name == "betaout":
            beta = value
            sin_alpha = 2 * sin(theta) * cos(tau) - sin(beta)  # (24)
            if abs(sin_alpha) > 1 + SMALL:
                raise DiffcalcException(UNREACHABLE_MSG % (name, value * TODEG))

            alpha = asin(sin_alpha)

        return alpha, beta

    def _calc_det_angles_given_det_or_naz_constraint(
        self,
        det_constraint: Dict[str, Optional[float]],
        naz_constraint: Dict[str, Optional[float]],
        theta: float,
        tau: float,
        alpha: float,
    ) -> Iterator[Tuple[float, float, float, float]]:

        assert det_constraint or naz_constraint
        try:
            naz_qaz_angle = self._calc_angle_between_naz_and_qaz(theta, alpha, tau)
        except AssertionError:
            return
        if det_constraint:
            # One of the detector angles is given                 (Section 5.1)
            det_constraint_name, det_constraint_value = next(
                iter(det_constraint.items())
            )
            for delta, nu, qaz in self._calc_remaining_detector_angles(
                det_constraint_name, det_constraint_value, theta
            ):
                if is_small(naz_qaz_angle):
                    naz_angles = [
                        qaz,
                    ]
                else:
                    naz_angles = [qaz - naz_qaz_angle, qaz + naz_qaz_angle]
                for naz in naz_angles:
                    yield qaz, naz, delta, nu
        elif naz_constraint:  # The 'detector' angle naz is given:
            naz_name, naz = next(iter(naz_constraint.items()))
            assert naz_name == "naz"
            if is_small(naz_qaz_angle):
                qaz_angles = [
                    naz,
                ]
            else:
                qaz_angles = [naz - naz_qaz_angle, naz + naz_qaz_angle]
            for qaz in qaz_angles:
                for delta, nu, _ in self._calc_remaining_detector_angles(
                    "qaz", qaz, theta
                ):
                    yield qaz, naz, delta, nu

    def _calc_remaining_detector_angles(
        self, constraint_name: str, constraint_value: float, theta: float
    ) -> Iterator[Tuple[float, float, float]]:
        """Return delta, nu and qaz given one detector angle."""
        #                                                         (section 5.1)
        # Find qaz using various derivations of 17 and 18
        sin_2theta = sin(2 * theta)
        cos_2theta = cos(2 * theta)
        if is_small(sin_2theta):
            raise DiffcalcException(
                "No meaningful scattering vector (Q) can be found when "
                f"theta is so small {theta * TODEG:.4f}."
            )

        if constraint_name == "delta":
            delta = constraint_value
            try:
                asin_qaz = asin(bound(sin(delta) / sin_2theta))  # (17 & 18)
            except AssertionError:
                return
            cos_delta = cos(delta)
            if is_small(cos_delta):
                # raise DiffcalcException(
                #    'The %s and %s circles are redundant when delta is constrained to %.0f degrees.'
                #    'Please change delta constraint or use 4-circle mode.' % ("nu", 'mu', delta * TODEG))
                print(
                    (
                        "DEGENERATE: with delta=90, %s is degenerate: choosing "
                        "%s = 0 (allowed because %s is unconstrained)"
                    )
                    % ("nu", "nu", "nu")
                )
                acos_nu = 1.0
            else:
                try:
                    acos_nu = acos(bound(cos_2theta / cos_delta))
                except AssertionError:
                    return
            if is_small(cos(asin_qaz)):
                qaz_angles = [
                    sign(asin_qaz) * pi / 2.0,
                ]
            else:
                qaz_angles = [asin_qaz, pi - asin_qaz]
            if is_small(acos_nu):
                nu_angles = [
                    0.0,
                ]
            else:
                nu_angles = [acos_nu, -acos_nu]
            for qaz, nu in product(qaz_angles, nu_angles):
                sgn_ref = sign(sin_2theta) * sign(cos(qaz))
                sgn_ratio = sign(sin(nu)) * sign(cos_delta)
                if sgn_ref == sgn_ratio:
                    yield delta, nu, qaz

        elif constraint_name == "nu":
            nu = constraint_value
            cos_nu = cos(nu)
            if is_small(cos_nu):
                raise DiffcalcException(
                    "The %s circle constraint to %.0f degrees is redundant."
                    "Please change this constraint or use 4-circle mode."
                    % ("nu", nu * TODEG)
                )
            cos_delta = cos_2theta / cos(nu)
            cos_qaz = cos_delta * sin(nu) / sin_2theta
            try:
                acos_delta = acos(bound(cos_delta))
                acos_qaz = acos(bound(cos_qaz))
            except AssertionError:
                return
            if is_small(acos_qaz):
                qaz_angles = [
                    0.0,
                ]
            else:
                qaz_angles = [acos_qaz, -acos_qaz]
            if is_small(acos_delta):
                delta_angles = [
                    0.0,
                ]
            else:
                delta_angles = [acos_delta, -acos_delta]
            for qaz, delta in product(qaz_angles, delta_angles):
                sgn_ref = sign(sin(delta))
                sgn_ratio = sign(sin(qaz)) * sign(sin_2theta)
                if sgn_ref == sgn_ratio:
                    yield delta, nu, qaz

        elif constraint_name == "qaz":
            qaz = constraint_value
            asin_delta = asin(sin(qaz) * sin_2theta)
            if is_small(cos(asin_delta)):
                delta_angles = [
                    sign(asin_delta) * pi / 2.0,
                ]
            else:
                delta_angles = [asin_delta, pi - asin_delta]
            for delta in delta_angles:
                cos_delta = cos(delta)
                if is_small(cos_delta):
                    print(
                        (
                            "DEGENERATE: with delta=90, %s is degenerate: choosing "
                            "%s = 0 (allowed because %s is unconstrained)"
                        )
                        % ("nu", "nu", "nu")
                    )
                    # raise DiffcalcException(
                    #    'The %s circle is redundant when delta is at %.0f degrees.'
                    #    'Please change detector constraint or use 4-circle mode.' % ("nu", delta * TODEG))
                    nu = 0.0
                else:
                    sgn_delta = sign(cos_delta)
                    nu = atan2(
                        sgn_delta * sin_2theta * cos(qaz), sgn_delta * cos_2theta
                    )
                yield delta, nu, qaz
        else:
            raise DiffcalcException(
                constraint_name + " is not an explicit detector angle "
                "(naz cannot be handled here)"
            )

    def _calc_sample_angles_from_one_sample_constraint(
        self,
        samp_constraints: Dict[str, Optional[float]],
        h_phi: np.ndarray,
        theta: float,
        alpha: float,
        qaz: float,
        naz: float,
        n_phi: np.ndarray,
    ) -> Iterator[Tuple[float, float, float, float]]:

        sample_constraint_name, sample_value = next(iter(samp_constraints.items()))
        q_lab = np.array(
            [[cos(theta) * sin(qaz)], [-sin(theta)], [cos(theta) * cos(qaz)]]
        )  # (18)
        n_lab = np.array(
            [[cos(alpha) * sin(naz)], [-sin(alpha)], [cos(alpha) * cos(naz)]]
        )  # (20)
        yield from self._calc_remaining_sample_angles(
            sample_constraint_name, sample_value, q_lab, n_lab, h_phi, n_phi
        )

    def _calc_sample_given_two_sample_and_reference(
        self,
        samp_constraints: Dict[str, Optional[float]],
        h_phi: np.ndarray,
        theta: float,
        psi: float,
        n_phi: np.ndarray,
    ) -> Iterator[Tuple[float, float, float, float, float, float]]:

        for angles in self._calc_sample_angles_given_two_sample_and_reference(
            samp_constraints, psi, theta, h_phi, n_phi
        ):
            qaz, psi, mu, eta, chi, phi = angles
            values_in_deg = tuple(v * TODEG for v in angles)
            logger.debug(
                "Initial angles: xi=%.3f, psi=%.3f, mu=%.3f, "
                "eta=%.3f, chi=%.3f, phi=%.3f" % values_in_deg
            )  # Try to find a solution for each possible transformed xi

            logger.debug("")
            msg = "---Trying psi={:.3f}, qaz={:.3f}".format(psi * TODEG, qaz * TODEG)
            logger.debug(msg)

            for delta, nu, _ in self._calc_remaining_detector_angles("qaz", qaz, theta):
                logger.debug("delta=%.3f, %s=%.3f", delta * TODEG, "nu", nu * TODEG)
                # for mu, eta, chi, phi in self._generate_sample_solutions(
                #    mu, eta, chi, phi, samp_constraints.keys(), delta,
                #    nu, wavelength, (h, k, l), ref_constraint_name,
                #    ref_constraint_value):
                yield mu, delta, nu, eta, chi, phi

    def _calc_remaining_sample_angles(
        self,
        constraint_name: str,
        constraint_value: float,
        q_lab: np.ndarray,
        n_lab: np.ndarray,
        q_phi: np.ndarray,
        n_phi: np.ndarray,
    ) -> Iterator[Tuple[float, float, float, float]]:
        """Return phi, chi, eta and mu, given one of these."""
        #                                                         (section 5.3)

        N_lab = self._calc_N(q_lab, n_lab)
        N_phi = self._calc_N(q_phi, n_phi)
        Z = N_lab @ N_phi.T

        if constraint_name == "mu":  # (35)
            mu = constraint_value
            V = inv(rot_MU(mu)) @ N_lab @ N_phi.T
            try:
                acos_chi = acos(bound(V[2, 2]))
            except AssertionError:
                return
            if is_small(sin(acos_chi)):
                # chi ~= 0 or 180 and therefor phi || eta The solutions for phi
                # and eta here will be valid but will be chosen unpredictably.
                # Choose eta=0:
                #
                # tan(phi+eta)=v12/v11 from docs/extensions_to_yous_paper.wxm
                chi = acos_chi
                eta = 0.0
                phi = atan2(-V[1, 0], V[1, 1])
                logger.debug(
                    "Eta and phi cannot be chosen uniquely with chi so close "
                    "to 0 or 180. Returning phi=%.3f and eta=%.3f",
                    phi * TODEG,
                    eta * TODEG,
                )
                yield mu, eta, chi, phi
            else:
                for chi in [acos_chi, -acos_chi]:
                    sgn = sign(sin(chi))
                    phi = atan2(-sgn * V[2, 1], -sgn * V[2, 0])
                    eta = atan2(-sgn * V[1, 2], sgn * V[0, 2])
                    yield mu, eta, chi, phi

        elif constraint_name == "phi":  # (37)
            phi = constraint_value
            V = N_lab @ inv(N_phi) @ rot_PHI(phi).T
            try:
                asin_eta = asin(bound(V[0, 1]))
            except AssertionError:
                return
            if is_small(cos(asin_eta)):
                raise DiffcalcException(
                    "Chi and mu cannot be chosen uniquely "
                    "with eta so close to +/-90."
                )
            for eta in [asin_eta, pi - asin_eta]:
                sgn = sign(cos(eta))
                mu = atan2(sgn * V[2, 1], sgn * V[1, 1])
                chi = atan2(sgn * V[0, 2], sgn * V[0, 0])
                yield mu, eta, chi, phi

        elif constraint_name in ("eta", "chi"):
            if constraint_name == "eta":  # (39)
                eta = constraint_value
                cos_eta = cos(eta)
                if is_small(cos_eta):
                    # TODO: Not likely to happen in real world!?
                    raise DiffcalcException(
                        "Chi and mu cannot be chosen uniquely with eta "
                        "constrained so close to +-90."
                    )
                try:
                    asin_chi = asin(bound(Z[0, 2] / cos_eta))
                except AssertionError:
                    return
                all_eta = [
                    eta,
                ]
                all_chi = [asin_chi, pi - asin_chi]

            else:  # constraint_name == 'chi'                            # (40)
                chi = constraint_value
                sin_chi = sin(chi)
                if is_small(sin_chi):
                    raise DiffcalcException(
                        "Eta and phi cannot be chosen uniquely with chi "
                        "constrained so close to 0. (Please contact developer "
                        "if this case is useful for you)"
                    )
                try:
                    acos_eta = acos(bound(Z[0, 2] / sin_chi))
                except AssertionError:
                    return
                all_eta = [acos_eta, -acos_eta]
                all_chi = [
                    chi,
                ]

            for chi, eta in product(all_chi, all_eta):
                top_for_mu = Z[2, 2] * sin(eta) * sin(chi) + Z[1, 2] * cos(chi)
                bot_for_mu = -Z[2, 2] * cos(chi) + Z[1, 2] * sin(eta) * sin(chi)
                if is_small(top_for_mu) and is_small(bot_for_mu):
                    # chi == +-90, eta == 0/180 and therefore phi || mu cos(chi) ==
                    # 0 and sin(eta) == 0 Experience shows that even though e.g.
                    # the z[2, 2] and z[1, 2] values used to calculate mu may be
                    # basically 0 (1e-34) their ratio in every case tested so far
                    # still remains valid and using them will result in a phi
                    # solution that is continuous with neighbouring positions.
                    #
                    # We cannot test phi minus mu here unfortunately as the final
                    # phi and mu solutions have not yet been chosen (they may be
                    # +-x or 180+-x). Otherwise we could choose a sensible solution
                    # here if the one found was incorrect.

                    # tan(phi+eta)=v12/v11 from extensions_to_yous_paper.wxm
                    # phi_minus_mu = -atan2(Z[2, 0], Z[1, 1])
                    raise DiffcalcException(
                        "Mu cannot be chosen uniquely as mu || phi with chi so close "
                        "to +/-90 and eta so close 0 or 180.\nPlease choose "
                        "a different set of constraints."
                    )
                mu = atan2(-top_for_mu, -bot_for_mu)  # (41)

                top_for_phi = Z[0, 1] * cos(eta) * cos(chi) - Z[0, 0] * sin(eta)
                bot_for_phi = Z[0, 1] * sin(eta) + Z[0, 0] * cos(eta) * cos(chi)
                if is_small(bot_for_phi) and is_small(top_for_phi):
                    DiffcalcException(
                        "Phi cannot be chosen uniquely as mu || phi with chi so close "
                        "to +/-90 and eta so close 0 or 180.\nPlease choose a "
                        "different set of constraints."
                    )
                phi = atan2(top_for_phi, bot_for_phi)  # (42)
                yield mu, eta, chi, phi

        else:
            raise DiffcalcException("Given angle must be one of phi, chi, eta or mu")

    def _calc_angles_given_three_sample_constraints(
        self,
        samp_constraints: Dict[str, Optional[float]],
        h_phi: np.ndarray,
        theta: float,
    ) -> Iterator[Tuple[float, float, float, float, float, float]]:
        def __get_last_sample_angle(A: float, B: float, C: float) -> List[float]:
            if is_small(A) and is_small(B):
                raise DiffcalcException(
                    "Sample orientation cannot be chosen uniquely. Please choose a different set of constraints."
                )
            ks = atan2(A, B)
            acos_alp = acos(bound(C / sqrt(A ** 2 + B ** 2)))
            if is_small(acos_alp):
                alp_list = [
                    ks,
                ]
            else:
                alp_list = [acos_alp + ks, -acos_alp + ks]
            return alp_list

        def __get_qaz_value(mu: float, eta: float, chi: float, phi: float) -> float:
            V0 = (
                h2 * cos(eta) * sin(chi)
                + (h0 * cos(chi) * cos(eta) + h1 * sin(eta)) * cos(phi)
                + (h1 * cos(chi) * cos(eta) - h0 * sin(eta)) * sin(phi)
            )
            V2 = (
                -h2 * sin(chi) * sin(eta) * sin(mu)
                + h2 * cos(chi) * cos(mu)
                - (
                    h0 * cos(mu) * sin(chi)
                    + (h0 * cos(chi) * sin(eta) - h1 * cos(eta)) * sin(mu)
                )
                * cos(phi)
                - (
                    h1 * cos(mu) * sin(chi)
                    + (h1 * cos(chi) * sin(eta) + h0 * cos(eta)) * sin(mu)
                )
                * sin(phi)
            )
            sgn_theta = sign(cos(theta))
            qaz = atan2(sgn_theta * V0, sgn_theta * V2)
            return qaz

        h_phi_norm = normalised(h_phi)  # (68,69)
        h0, h1, h2 = h_phi_norm[0, 0], h_phi_norm[1, 0], h_phi_norm[2, 0]

        if "mu" not in samp_constraints:
            eta = self.constraints._sample["eta"]
            chi = self.constraints._sample["chi"]
            phi = self.constraints._sample["phi"]

            A = h0 * cos(phi) * sin(chi) + h1 * sin(chi) * sin(phi) - h2 * cos(chi)
            B = (
                -h2 * sin(chi) * sin(eta)
                - (h0 * cos(chi) * sin(eta) - h1 * cos(eta)) * cos(phi)
                - (h1 * cos(chi) * sin(eta) + h0 * cos(eta)) * sin(phi)
            )
            C = -sin(theta)
            try:
                mu_vals = __get_last_sample_angle(A, B, C)
            except AssertionError:
                return
            for mu in mu_vals:
                qaz = __get_qaz_value(mu, eta, chi, phi)
                logger.debug("--- Trying mu:%.f qaz_%.f", mu * TODEG, qaz * TODEG)
                for delta, nu, _ in self._calc_remaining_detector_angles(
                    "qaz", qaz, theta
                ):
                    logger.debug("delta=%.3f, %s=%.3f", delta * TODEG, "nu", nu * TODEG)
                    yield mu, delta, nu, eta, chi, phi

        elif "eta" not in samp_constraints:
            mu = self.constraints._sample["mu"]
            chi = self.constraints._sample["chi"]
            phi = self.constraints._sample["phi"]

            A = (
                -h0 * cos(chi) * cos(mu) * cos(phi)
                - h1 * cos(chi) * cos(mu) * sin(phi)
                - h2 * cos(mu) * sin(chi)
            )
            B = h1 * cos(mu) * cos(phi) - h0 * cos(mu) * sin(phi)
            C = (
                -h0 * cos(phi) * sin(chi) * sin(mu)
                - h1 * sin(chi) * sin(mu) * sin(phi)
                + h2 * cos(chi) * sin(mu)
                - sin(theta)
            )
            try:
                eta_vals = __get_last_sample_angle(A, B, C)
            except AssertionError:
                return
            for eta in eta_vals:
                qaz = __get_qaz_value(mu, eta, chi, phi)
                logger.debug("--- Trying eta:%.f qaz_%.f", eta * TODEG, qaz * TODEG)
                for delta, nu, _ in self._calc_remaining_detector_angles(
                    "qaz", qaz, theta
                ):
                    logger.debug("delta=%.3f, %s=%.3f", delta * TODEG, "nu", nu * TODEG)
                    yield mu, delta, nu, eta, chi, phi

        elif "chi" not in samp_constraints:
            mu = self.constraints._sample["mu"]
            eta = self.constraints._sample["eta"]
            phi = self.constraints._sample["phi"]

            A = (
                -h2 * cos(mu) * sin(eta)
                + h0 * cos(phi) * sin(mu)
                + h1 * sin(mu) * sin(phi)
            )
            B = (
                -h0 * cos(mu) * cos(phi) * sin(eta)
                - h1 * cos(mu) * sin(eta) * sin(phi)
                - h2 * sin(mu)
            )
            C = (
                -h1 * cos(eta) * cos(mu) * cos(phi)
                + h0 * cos(eta) * cos(mu) * sin(phi)
                - sin(theta)
            )
            try:
                chi_vals = __get_last_sample_angle(A, B, C)
            except AssertionError:
                return
            for chi in chi_vals:
                qaz = __get_qaz_value(mu, eta, chi, phi)
                logger.debug("--- Trying chi:%.f qaz_%.f", chi * TODEG, qaz * TODEG)
                for delta, nu, _ in self._calc_remaining_detector_angles(
                    "qaz", qaz, theta
                ):
                    logger.debug("delta=%.3f, %s=%.3f", delta * TODEG, "nu", nu * TODEG)
                    yield mu, delta, nu, eta, chi, phi

        elif "phi" not in samp_constraints:
            mu = self.constraints._sample["mu"]
            eta = self.constraints._sample["eta"]
            chi = self.constraints._sample["chi"]

            A = h1 * sin(chi) * sin(mu) - (
                h1 * cos(chi) * sin(eta) + h0 * cos(eta)
            ) * cos(mu)
            B = h0 * sin(chi) * sin(mu) - (
                h0 * cos(chi) * sin(eta) - h1 * cos(eta)
            ) * cos(mu)
            C = (
                h2 * cos(mu) * sin(chi) * sin(eta)
                + h2 * cos(chi) * sin(mu)
                - sin(theta)
            )
            try:
                phi_vals = __get_last_sample_angle(A, B, C)
            except AssertionError:
                return
            for phi in phi_vals:
                qaz = __get_qaz_value(mu, eta, chi, phi)
                logger.debug("--- Trying phi:%.f qaz_%.f", phi * TODEG, qaz * TODEG)
                for delta, nu, _ in self._calc_remaining_detector_angles(
                    "qaz", qaz, theta
                ):
                    logger.debug("delta=%.3f, %s=%.3f", delta * TODEG, "nu", nu * TODEG)
                    yield mu, delta, nu, eta, chi, phi
        else:
            raise DiffcalcException(
                "Internal error: Invalid set of sample constraints."
            )

    def _calc_sample_angles_given_two_sample_and_reference(
        self,
        samp_constraints: Dict[str, Optional[float]],
        psi: float,
        theta: float,
        q_phi: np.ndarray,
        n_phi: np.ndarray,
    ) -> Iterator[Tuple[float, float, float, float, float, float]]:
        """Return sample angles.

        Available combinations:
        chi, phi, reference
        mu, eta, reference,
        chi, eta, reference
        chi, mu, reference
        mu, phi, reference
        eta, phi, reference
        """

        def __get_phi_and_qaz(chi: float, eta: float, mu: float) -> Tuple[float, float]:
            a = sin(chi) * cos(eta)
            b = sin(chi) * sin(eta) * sin(mu) - cos(chi) * cos(mu)
            sin_qaz = V[2, 0] * a - V[2, 2] * b
            cos_qaz = -V[2, 2] * a - V[2, 0] * b
            # atan2_xi = atan2(V[2, 2] * a + V[2, 0] * b,
            #           V[2, 0] * a - V[2, 2] * b)                        # (54)
            qaz = atan2(sin_qaz, cos_qaz)  # (54)

            a = sin(chi) * sin(mu) - cos(mu) * cos(chi) * sin(eta)
            b = cos(mu) * cos(eta)
            phi = atan2(V[1, 1] * a - V[0, 1] * b, V[0, 1] * a + V[1, 1] * b)  # (55)
            #        if is_small(mu+pi/2) and is_small(eta) and False:
            #            phi_general = phi
            #            # solved in extensions_to_yous_paper.wxm
            #            phi = atan2(V[1, 1], V[0, 1])
            #            logger.debug("phi = %.3f or %.3f (std)",
            #                        phi*TODEG, phi_general*TODEG )

            return qaz, phi

        def __get_chi_and_qaz(mu: float, eta: float) -> Tuple[float, float]:
            A = sin(mu)
            B = -cos(mu) * sin(eta)
            sin_chi = A * V[1, 0] + B * V[1, 2]
            cos_chi = B * V[1, 0] - A * V[1, 2]
            if is_small(sin_chi) and is_small(cos_chi):
                raise DiffcalcException(
                    "Chi cannot be chosen uniquely. Please choose a different set of constraints."
                )
            chi = atan2(sin_chi, cos_chi)

            A = sin(eta)
            B = cos(eta) * sin(mu)
            sin_qaz = A * V[0, 1] + B * V[2, 1]
            cos_qaz = B * V[0, 1] - A * V[2, 1]
            qaz = atan2(sin_qaz, cos_qaz)
            return qaz, chi

        N_phi = self._calc_N(q_phi, n_phi)
        THETA = z_rotation(-theta)
        PSI = x_rotation(psi)

        if "chi" in samp_constraints and "phi" in samp_constraints:

            chi = samp_constraints["chi"]
            phi = samp_constraints["phi"]

            CHI = rot_CHI(chi)
            PHI = rot_PHI(phi)
            V = CHI @ PHI @ N_phi @ PSI.T @ THETA.T  # (46)

            # atan2_xi = atan2(-V[2, 0], V[2, 2])
            # atan2_eta = atan2(-V[0, 1], V[1, 1])
            # atan2_mu = atan2(-V[2, 1], sqrt(V[2, 2] ** 2 + V[2, 0] ** 2))
            try:
                asin_mu = asin(bound(-V[2, 1]))
            except AssertionError:
                return
            for mu in [asin_mu, pi - asin_mu]:
                sgn_cosmu = sign(cos(mu))
                # xi = atan2(-sgn_cosmu * V[2, 0], sgn_cosmu * V[2, 2])
                qaz = atan2(
                    sgn_cosmu * V[2, 2],
                    sgn_cosmu * V[2, 0],
                )
                eta = atan2(-sgn_cosmu * V[0, 1], sgn_cosmu * V[1, 1])
                yield qaz, psi, mu, eta, chi, phi

        elif "mu" in samp_constraints and "eta" in samp_constraints:

            mu = samp_constraints["mu"]
            eta = samp_constraints["eta"]

            V = N_phi @ PSI.T @ THETA.T  # (49)
            try:
                bot = bound(
                    -V[2, 1] / sqrt(sin(eta) ** 2 * cos(mu) ** 2 + sin(mu) ** 2)
                )
            except AssertionError:
                return
            if is_small(cos(mu) * sin(eta)):
                eps = atan2(sin(eta) * cos(mu), sin(mu))
                chi_vals = [eps + acos(bot), eps - acos(bot)]
            else:
                eps = atan2(sin(mu), sin(eta) * cos(mu))
                chi_vals = [asin(bot) - eps, pi - asin(bot) - eps]  # (52)

            ## Choose final chi solution here to obtain compatable xi and mu
            ## TODO: This temporary solution works only for one case used on i07
            ##       Return a list of possible solutions?
            # if is_small(eta) and is_small(mu + pi / 2):
            #    for chi in _generate_transformed_values(chi_orig):
            #        if  pi / 2 <= chi < pi:
            #            break
            # else:
            #    chi = chi_orig

            for chi in chi_vals:
                qaz, phi = __get_phi_and_qaz(chi, eta, mu)
                yield qaz, psi, mu, eta, chi, phi

        elif "chi" in samp_constraints and "eta" in samp_constraints:

            chi = samp_constraints["chi"]
            eta = samp_constraints["eta"]

            V = N_phi @ PSI.T @ THETA.T  # (49)
            try:
                bot = bound(
                    -V[2, 1] / sqrt(sin(eta) ** 2 * sin(chi) ** 2 + cos(chi) ** 2)
                )
            except AssertionError:
                return
            if is_small(cos(chi)):
                eps = atan2(cos(chi), sin(chi) * sin(eta))
                mu_vals = [eps + acos(bot), eps - acos(bot)]
            else:
                eps = atan2(sin(chi) * sin(eta), cos(chi))
                mu_vals = [asin(bot) - eps, pi - asin(bot) - eps]  # (52)

            for mu in mu_vals:
                qaz, phi = __get_phi_and_qaz(chi, eta, mu)
                yield qaz, psi, mu, eta, chi, phi

        elif "chi" in samp_constraints and "mu" in samp_constraints:

            chi = samp_constraints["chi"]
            mu = samp_constraints["mu"]

            V = N_phi @ PSI.T @ THETA.T  # (49)

            try:
                asin_eta = asin(
                    bound((-V[2, 1] - cos(chi) * sin(mu)) / (sin(chi) * cos(mu)))
                )
            except AssertionError:
                return

            for eta in [asin_eta, pi - asin_eta]:
                qaz, phi = __get_phi_and_qaz(chi, eta, mu)
                yield qaz, psi, mu, eta, chi, phi

        elif "mu" in samp_constraints and "phi" in samp_constraints:

            mu = samp_constraints["mu"]
            phi = samp_constraints["phi"]

            PHI = rot_PHI(phi)
            V = THETA @ PSI @ inv(N_phi) @ PHI.T

            if is_small(cos(mu)):
                raise DiffcalcException(
                    "Eta cannot be chosen uniquely. Please choose a different set of constraints."
                )
            try:
                acos_eta = acos(bound(V[1, 1] / cos(mu)))
            except AssertionError:
                return
            for eta in [acos_eta, -acos_eta]:
                qaz, chi = __get_chi_and_qaz(mu, eta)
                yield qaz, psi, mu, eta, chi, phi

        elif "eta" in samp_constraints and "phi" in samp_constraints:

            eta = samp_constraints["eta"]
            phi = samp_constraints["phi"]

            PHI = rot_PHI(phi)
            V = THETA @ PSI @ inv(N_phi) @ PHI.T

            if is_small(cos(eta)):
                raise DiffcalcException(
                    "Mu cannot be chosen uniquely. Please choose a different set of constraints."
                )
            try:
                acos_mu = acos(bound(V[1, 1] / cos(eta)))
            except AssertionError:
                return
            for mu in [acos_mu, -acos_mu]:
                qaz, chi = __get_chi_and_qaz(mu, eta)
                yield qaz, psi, mu, eta, chi, phi

        else:
            raise DiffcalcException(
                "No code yet to handle this combination of 2 sample "
                "constraints and one reference!:" + str(samp_constraints)
            )

    def _calc_sample_angles_given_two_sample_and_detector(
        self,
        samp_constraints: Dict[str, Optional[float]],
        qaz: float,
        theta: float,
        q_phi: np.ndarray,
        n_phi: np.ndarray,
    ) -> Iterator[Tuple[float, float, float, float]]:
        """Return sample angles.

        Available combinations:
        chi, phi, detector
        mu, eta, detector
        mu, phi, detector
        mu, chi, detector
        eta, phi, detector
        eta, chi, detector
        """
        N_phi = self._calc_N(q_phi, n_phi)

        if (
            ("mu" in samp_constraints and "eta" in samp_constraints)
            or ("omega" in samp_constraints and "bisect" in samp_constraints)
            or ("mu" in samp_constraints and "bisect" in samp_constraints)
            or ("eta" in samp_constraints and "bisect" in samp_constraints)
        ):

            if "mu" in samp_constraints and "eta" in samp_constraints:
                mu_vals = [
                    samp_constraints["mu"],
                ]
                eta_vals = [
                    samp_constraints["eta"],
                ]
            elif "omega" in samp_constraints and "bisect" in samp_constraints:
                omega = samp_constraints["omega"]
                atan_mu = atan(tan(theta + omega) * cos(qaz))
                asin_eta = asin(sin(theta + omega) * sin(qaz))
                mu_vals = [atan_mu, atan_mu + pi]
                if is_small(abs(asin_eta) - pi / 2):
                    eta_vals = [
                        sign(asin_eta) * pi / 2,
                    ]
                else:
                    eta_vals = [asin_eta, pi - asin_eta]

            elif "mu" in samp_constraints and "bisect" in samp_constraints:
                mu_vals = [
                    samp_constraints["mu"],
                ]
                cos_qaz = cos(qaz)
                tan_mu = tan(samp_constraints["mu"])
                # Vertical scattering geometry with omega = 0
                if is_small(cos_qaz):
                    if is_small(tan_mu):
                        thomega_vals = [
                            theta,
                        ]
                    else:
                        return
                else:
                    atan_thomega = atan(tan_mu / cos_qaz)
                    thomega_vals = [atan_thomega, pi + atan_thomega]
                eta_vals = []
                for thomega in thomega_vals:
                    asin_eta = asin(sin(thomega) * sin(qaz))
                    if is_small(abs(asin_eta) - pi / 2):
                        eta_vals.extend(
                            [
                                sign(asin_eta) * pi / 2,
                            ]
                        )
                    else:
                        eta_vals.extend([asin_eta, pi - asin_eta])

            elif "eta" in samp_constraints and "bisect" in samp_constraints:
                eta_vals = [
                    samp_constraints["eta"],
                ]
                sin_qaz = sin(qaz)
                sin_eta = sin(samp_constraints["eta"])
                # Horizontal scattering geometry with omega = 0
                if is_small(sin_qaz):
                    if is_small(sin_eta):
                        thomega_vals = [
                            theta,
                        ]
                    else:
                        return
                else:
                    asin_thomega = asin(sin_eta / sin_qaz)
                    if is_small(abs(asin_thomega) - pi / 2):
                        thomega_vals = [
                            sign(asin_thomega) * pi / 2,
                        ]
                    else:
                        thomega_vals = [asin_thomega, pi - asin_thomega]
                mu_vals = []
                for thomega in thomega_vals:
                    atan_mu = atan(tan(thomega) * cos(qaz))
                    mu_vals.extend([atan_mu, pi + atan_mu])

            for mu, eta in product(mu_vals, eta_vals):
                F = y_rotation(qaz - pi / 2.0)
                THETA = z_rotation(-theta)
                V = rot_ETA(eta).T @ rot_MU(mu).T @ F @ THETA  # (56)

                phi_vals = []
                try:
                    # For the case of (00l) reflection, where N_phi[0,0] = N_phi[1,0] = 0
                    if is_small(N_phi[0, 0]) and is_small(N_phi[1, 0]):
                        raise DiffcalcException(
                            "Phi cannot be chosen uniquely as q || phi and no reference "
                            "vector or phi constraints have been set.\nPlease choose a different "
                            "set of constraints."
                        )
                    bot = bound(-V[1, 0] / sqrt(N_phi[0, 0] ** 2 + N_phi[1, 0] ** 2))
                    eps = atan2(N_phi[1, 0], N_phi[0, 0])
                    phi_vals = [asin(bot) + eps, pi - asin(bot) + eps]  # (59)
                except AssertionError:
                    continue
                for phi in phi_vals:
                    a = N_phi[0, 0] * cos(phi) + N_phi[1, 0] * sin(phi)
                    chi = atan2(
                        N_phi[2, 0] * V[0, 0] - a * V[2, 0],
                        N_phi[2, 0] * V[2, 0] + a * V[0, 0],
                    )  # (60)
                    yield mu, eta, chi, phi

        elif "chi" in samp_constraints and "phi" in samp_constraints:

            chi = samp_constraints["chi"]
            phi = samp_constraints["phi"]

            CHI = rot_CHI(chi)
            PHI = rot_PHI(phi)
            V = CHI @ PHI @ N_phi  # (62)

            try:
                bot = bound(
                    V[2, 0] / sqrt(cos(qaz) ** 2 * cos(theta) ** 2 + sin(theta) ** 2)
                )
            except AssertionError:
                return
            eps = atan2(-cos(qaz) * cos(theta), sin(theta))
            for mu in [asin(bot) + eps, pi - asin(bot) + eps]:
                a = cos(theta) * sin(qaz)
                b = -cos(theta) * sin(mu) * cos(qaz) + cos(mu) * sin(theta)
                X = V[1, 0] * a + V[0, 0] * b
                Y = V[0, 0] * a - V[1, 0] * b
                if is_small(X) and is_small(Y):
                    raise DiffcalcException(
                        "Eta cannot be chosen uniquely as q || eta and no reference "
                        "vector or eta constraints have been set.\nPlease choose a different "
                        "set of constraints."
                    )
                eta = atan2(X, Y)

                # a = -cos(mu) * cos(qaz) * sin(theta) + sin(mu) * cos(theta)
                # b = cos(mu) * sin(qaz)
                # psi = atan2(-V[2, 2] * a - V[2, 1] * b, V[2, 1] * a - V[2, 2] * b)
                yield mu, eta, chi, phi

        elif "mu" in samp_constraints and "phi" in samp_constraints:

            mu = samp_constraints["mu"]
            phi = samp_constraints["phi"]

            F = y_rotation(qaz - pi / 2.0)
            THETA = z_rotation(-theta)
            V = rot_MU(mu).T @ F @ THETA
            E = rot_PHI(phi) @ N_phi

            try:
                bot = bound(-V[2, 0] / sqrt(E[0, 0] ** 2 + E[2, 0] ** 2))
            except AssertionError:
                return
            eps = atan2(E[2, 0], E[0, 0])
            for chi in [asin(bot) + eps, pi - asin(bot) + eps]:
                a = E[0, 0] * cos(chi) + E[2, 0] * sin(chi)
                eta = atan2(
                    V[0, 0] * E[1, 0] - V[1, 0] * a, V[0, 0] * a + V[1, 0] * E[1, 0]
                )
                yield mu, eta, chi, phi

        elif "mu" in samp_constraints and "chi" in samp_constraints:

            mu = samp_constraints["mu"]
            chi = samp_constraints["chi"]

            V20 = cos(mu) * cos(qaz) * cos(theta) + sin(mu) * sin(theta)
            A = N_phi[1, 0]
            B = N_phi[0, 0]
            if is_small(sin(chi)):
                raise DiffcalcException(
                    "Degenerate configuration with phi || eta axes cannot be set uniquely. Please choose a different set of constraints."
                )
            if is_small(A) and is_small(B):
                raise DiffcalcException(
                    "Phi cannot be chosen uniquely. Please choose a different set of constraints."
                )
            else:
                ks = atan2(A, B)
            try:
                acos_phi = acos(
                    bound(
                        (N_phi[2, 0] * cos(chi) - V20)
                        / (sin(chi) * sqrt(A ** 2 + B ** 2))
                    )
                )
            except AssertionError:
                return
            if is_small(acos_phi):
                phi_list = [
                    ks,
                ]
            else:
                phi_list = [acos_phi + ks, -acos_phi + ks]
            for phi in phi_list:
                A00 = -cos(qaz) * cos(theta) * sin(mu) + cos(mu) * sin(theta)
                B00 = sin(qaz) * cos(theta)
                V00 = (
                    N_phi[0, 0] * cos(chi) * cos(phi)
                    + N_phi[1, 0] * cos(chi) * sin(phi)
                    + N_phi[2, 0] * sin(chi)
                )
                V10 = N_phi[1, 0] * cos(phi) - N_phi[0, 0] * sin(phi)
                sin_eta = V00 * A00 + V10 * B00
                cos_eta = V00 * B00 - V10 * A00
                if is_small(A00) and is_small(B00):
                    raise DiffcalcException(
                        "Eta cannot be chosen uniquely. Please choose a different set of constraints."
                    )
                eta = atan2(sin_eta, cos_eta)
                yield mu, eta, chi, phi

        elif "eta" in samp_constraints and "phi" in samp_constraints:

            eta = samp_constraints["eta"]
            phi = samp_constraints["phi"]

            X = N_phi[2, 0]
            Y = N_phi[0, 0] * cos(phi) + N_phi[1, 0] * sin(phi)
            if is_small(X) and is_small(Y):
                raise DiffcalcException(
                    "Chi cannot be chosen uniquely as q || chi and no reference "
                    "vector or chi constraints have been set.\nPlease choose a different "
                    "set of constraints."
                )

            V = (N_phi[1, 0] * cos(phi) - N_phi[0, 0] * sin(phi)) * tan(eta)
            sgn = sign(cos(eta))
            eps = atan2(X * sgn, Y * sgn)
            try:
                acos_rhs = acos(
                    bound(
                        (sin(qaz) * cos(theta) / cos(eta) - V) / sqrt(X ** 2 + Y ** 2)
                    )
                )
            except AssertionError:
                return
            if is_small(acos_rhs):
                acos_list = [
                    eps,
                ]
            else:
                acos_list = [eps + acos_rhs, eps - acos_rhs]
            for chi in acos_list:
                A = (N_phi[0, 0] * cos(phi) + N_phi[1, 0] * sin(phi)) * sin(
                    chi
                ) - N_phi[2, 0] * cos(chi)
                B = (
                    -N_phi[2, 0] * sin(chi) * sin(eta)
                    - cos(chi)
                    * sin(eta)
                    * (N_phi[0, 0] * cos(phi) + N_phi[1, 0] * sin(phi))
                    - cos(eta) * (N_phi[0, 0] * sin(phi) - N_phi[1, 0] * cos(phi))
                )
                ks = atan2(A, B)
                mu = atan2(cos(theta) * cos(qaz), -sin(theta)) + ks
                yield mu, eta, chi, phi

        elif "eta" in samp_constraints and "chi" in samp_constraints:

            eta = samp_constraints["eta"]
            chi = samp_constraints["chi"]

            A = N_phi[1, 0] * cos(chi) * cos(eta) - N_phi[0, 0] * sin(eta)
            B = N_phi[0, 0] * cos(chi) * cos(eta) + N_phi[1, 0] * sin(eta)
            if is_small(A) and is_small(B):
                raise DiffcalcException(
                    "Phi cannot be chosen uniquely. Please choose a different set of constraints."
                )
            else:
                ks = atan2(A, B)
            try:
                acos_V00 = acos(
                    bound(
                        (cos(theta) * sin(qaz) - N_phi[2, 0] * cos(eta) * sin(chi))
                        / sqrt(A ** 2 + B ** 2)
                    )
                )
            except AssertionError:
                return
            if is_small(acos_V00):
                phi_list = [
                    ks,
                ]
            else:
                phi_list = [acos_V00 + ks, -acos_V00 + ks]
            for phi in phi_list:
                A10 = (
                    N_phi[0, 0] * cos(phi) * sin(chi)
                    + N_phi[1, 0] * sin(chi) * sin(phi)
                    - N_phi[2, 0] * cos(chi)
                )
                B10 = (
                    -N_phi[2, 0] * sin(chi) * sin(eta)
                    - (cos(chi) * cos(phi) * sin(eta) + cos(eta) * sin(phi))
                    * N_phi[0, 0]
                    - (cos(chi) * sin(eta) * sin(phi) - cos(eta) * cos(phi))
                    * N_phi[1, 0]
                )
                V10 = -sin(theta)
                A20 = (
                    -N_phi[2, 0] * sin(chi) * sin(eta)
                    - (cos(chi) * cos(phi) * sin(eta) + cos(eta) * sin(phi))
                    * N_phi[0, 0]
                    - (cos(chi) * sin(eta) * sin(phi) - cos(eta) * cos(phi))
                    * N_phi[1, 0]
                )
                B20 = (
                    -N_phi[0, 0] * cos(phi) * sin(chi)
                    - N_phi[1, 0] * sin(chi) * sin(phi)
                    + N_phi[2, 0] * cos(chi)
                )
                V20 = cos(qaz) * cos(theta)
                sin_mu = (V10 * B20 - V20 * B10) * sign(A10 * B20 - A20 * B10)
                cos_mu = (V10 * A20 - V20 * A10) * sign(B10 * A20 - B20 * A10)
                if is_small(sin_mu) and is_small(cos_mu):
                    raise DiffcalcException(
                        "Mu cannot be chosen uniquely. Please choose a different set of constraints."
                    )
                mu = atan2(sin_mu, cos_mu)
                yield mu, eta, chi, phi

        else:
            raise DiffcalcException(
                "No code yet to handle this combination of 2 sample "
                "constraints and one detector!:" + str(samp_constraints)
            )

    def _tidy_degenerate_solutions(
        self, pos: Position, print_degenerate: bool = False
    ) -> Position:

        detector_like_constraint = self.constraints._detector or self.constraints.naz
        nu_constrained_to_0 = is_small(pos.nu) and detector_like_constraint
        mu_constrained_to_0 = is_small(pos.mu) and "mu" in self.constraints._sample
        delta_constrained_to_0 = is_small(pos.delta) and detector_like_constraint
        eta_constrained_to_0 = is_small(pos.eta) and "eta" in self.constraints._sample
        phi_not_constrained = "phi" not in self.constraints._sample

        if (
            nu_constrained_to_0
            and mu_constrained_to_0
            and phi_not_constrained
            and is_small(pos.chi)
        ):
            # constrained to vertical 4-circle like mode
            # phi || eta
            desired_eta = pos.delta / 2.0
            eta_diff = desired_eta - pos.eta
            if print_degenerate:
                print(
                    "DEGENERATE: with chi=0, phi and eta are colinear:"
                    "choosing eta = delta/2 by adding % 7.3f to eta and "
                    "removing it from phi. (mu=%s=0 only)" % (eta_diff * TODEG, "nu")
                )
                print("            original:", pos)
            newpos = Position(
                pos.mu, pos.delta, pos.nu, desired_eta, pos.chi, pos.phi - eta_diff
            )

        elif (
            delta_constrained_to_0
            and eta_constrained_to_0
            and phi_not_constrained
            and is_small(pos.chi - pi / 2)
        ):
            # constrained to horizontal 4-circle like mode
            # phi || mu
            desired_mu = pos.nu / 2.0
            mu_diff = desired_mu - pos.mu
            if print_degenerate:
                print(
                    "DEGENERATE: with chi=90, phi and mu are colinear: choosing"
                    " mu = %s/2 by adding % 7.3f to mu and to phi. "
                    "(delta=eta=0 only)" % ("nu", mu_diff * TODEG)
                )
                print("            original:", pos)
            newpos = Position(
                desired_mu, pos.delta, pos.nu, pos.eta, pos.chi, pos.phi + mu_diff
            )
        else:
            newpos = pos
        return newpos

    def _theta_and_qaz_from_detector_angles(
        self, delta: float, nu: float
    ) -> Tuple[float, float]:
        # Equation 19:
        cos_2theta = cos(delta) * cos(nu)
        theta = acos(cos_2theta) / 2.0
        sgn = sign(sin(2.0 * theta))
        qaz = atan2(sgn * sin(delta), sgn * cos(delta) * sin(nu))
        return theta, qaz

    def _verify_pos_map_to_hkl(
        self, h: float, k: float, l: float, wavelength: float, pos: Position
    ) -> None:
        hkl = self.get_hkl(pos, wavelength)
        e = 0.001
        if (abs(hkl[0] - h) > e) or (abs(hkl[1] - k) > e) or (abs(hkl[2] - l) > e):
            s = "ERROR: The angles calculated for hkl=({:f},{:f},{:f}) were {}.\n".format(
                h,
                k,
                l,
                str(pos),
            )
            s += "Converting these angles back to hkl resulted in hkl=" "(%f,%f,%f)" % (
                hkl[0],
                hkl[1],
                hkl[2],
            )
            raise DiffcalcException(s)

    def _verify_virtual_angles(
        self,
        h: float,
        k: float,
        l: float,
        pos: Position,
        virtual_angles: Dict[str, float],
    ) -> None:
        # Check that the virtual angles calculated/fixed during the hklToAngles
        # those read back from pos using anglesToVirtualAngles
        virtual_angles_readback = self.get_virtual_angles(pos)
        for key, val in virtual_angles.items():
            if val is not None:  # Some values calculated in some mode_selector
                r = virtual_angles_readback[key]
                if (not isnan(val) or not isnan(r)) and not radians_equivalent(
                    val, r, 1e-5
                ):
                    s = (
                        "ERROR: The angles calculated for hkl=(%f,%f,%f) with"
                        " mode=%s were %s.\n" % (h, k, l, self.__repr_mode(), str(pos))
                    )
                    s += (
                        "During verification the virtual angle %s resulting "
                        "from (or set for) this calculation of %f " % (key, val)
                    )
                    s += (
                        "did not match that calculated by "
                        "anglesToVirtualAngles of %f" % virtual_angles_readback[key]
                    )
                    raise DiffcalcException(s)
