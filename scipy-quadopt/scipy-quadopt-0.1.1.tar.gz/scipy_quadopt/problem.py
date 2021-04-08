import scipy.optimize
import numpy as np
from typing import List, Optional


def objective_fn(w: List[float],
                 c: List[float],
                 Q: List[List[float]]) -> float:
    """objective function of the optimization problem"""
    return -np.dot(w, c) + np.sqrt(np.dot(w, np.dot(Q, w)))


def get_weights(c: List[float],
                Q: List[List[float]],
                lam: Optional[float] = 0.5,
                bnd_up: Optional[float] = 1.0,
                dtype=np.float64,
                maxiter: Optional[int] = 100,
                ftol: Optional[float] = 1e-06
                ) -> (List[float], scipy.optimize.OptimizeResult):
    """Maximize "total goodness" and minimize "total similarity"


    """
    # error checking
    if lam < 0:
        raise Exception(f"the preference lambda='{lam}' must be positive")
    if bnd_up <= 0 or bnd_up > 1:
        raise Exception(f"the upper bound must be 1.0>={bnd_up}>0.0")

    # how big is `N`
    n_examples = len(c)

    # set the intial values
    x0 = np.ones(n_examples, dtype=dtype) / n_examples

    # convert to numpy
    # - Trick: We can multipy `lam*Q` beforehand and save compute time!
    args = (
        np.array(c, dtype=dtype),
        np.array(Q, dtype=dtype) * lam
    )

    # auto correct upper bound
    if (bnd_up is None) or (float(1.0 / n_examples) > bnd_up):
        bnd_up = min(2.0 * float(1.0 / n_examples), 1.0)
        print(f"upper bound changed to bnd_up={bnd_up}")

    # specify the non-negativity constraint >0, and set the upper bound
    con_lo_up = scipy.optimize.Bounds(0, bnd_up)

    # specify the "budget" constraint
    con_budget = {
        'type': 'eq',
        'fun': lambda x: np.sum(x) - 1
    }

    # SLSQP specific options
    options = {'maxiter': maxiter, 'ftol': ftol, 'disp': False}

    # run the numerical optimization algorithm
    results = scipy.optimize.minimize(
        objective_fn, x0=x0, args=args,
        bounds=con_lo_up, constraints=[con_budget],
        method='SLSQP', options=options
    )

    # done
    return results.x, results
