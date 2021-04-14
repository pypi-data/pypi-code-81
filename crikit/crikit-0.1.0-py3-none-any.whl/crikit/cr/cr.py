import jax.numpy as jnp
from jax import nn
import numpy as np
import jax
from ..invariants import (
    InvariantInfo,
    TensorType,
    LeviCivitaType,
    get_invariant_functions,
    get_invariant_descriptions,
)
from jax.tree_util import (
    Partial as partial,
)  # JAX-friendlier version of functools.partial
from .types import PointMap
from .space_builders import DirectSum
from pyadjoint_utils.jax_adjoint import array, ndarray, overload_jax, get_default_dtype
from .jax_utils import JAXArrays, UFLExprSpace_To_JAX, JAX_UFLFunctionSpace_Covering
from crikit.logging import logger
from typing import Union, Any, Optional, Tuple, Sequence, Iterable, Callable

Array = Any


class CR(PointMap):
    """A Constitutive Relation that automatically generates scalar and form
    invariants with :mod:`crikit.invariants`. All you need to provide is a function
    to compute scalar values of the scalar invariants that can be multiplied
    against the form invariants to form an equivariant tensor function in
    accordance with the canonical representation of Wineman and Pipkin, who
    showed that any equivariant (under a physical group) tensor function can be
    represented as a linear combination of scalar functions of scalar invariants
    and form invariants. In other words, this is a function that takes in
    the scalar invariants at a point as a one-dimensional JAX array (as well as any
    parameters you specify), and returns a one-dimensional JAX array, with one element
    for each form invariant.

    You can use :func:`cr_function_shape` to determine how many scalar invariants
    your function will take in and how many scalar values your function will
    need to output.

    """

    def __init__(
        self,
        output_type: TensorType,
        input_types: Sequence[TensorType],
        cr_function: Optional[Callable] = None,
        param_argnums: Optional[Sequence[int]] = None,
        params: Optional[Sequence[Array]] = None,
        cr_static_argnums: Optional[Sequence[int]] = None,
        vmap: bool = True,
        nojit: bool = False,
        strain_energy: bool = False,
        **cr_jax_kwargs,
    ):
        """Constructor for CR

        :param output_type: a TensorType corresponding to the output. If you want a
            strain-energy CR (one which computes the stress
            as the partial derivative of a strain energy functional with respect to the first
            input, then pass :meth:`crikit.invariants.TensorType.make_scalar` as the output type
            (i.e. a scalar).
        :type output_type: TensorType
        :param input_types: a sequence of TensorTypes corresponding to the inputs
        :type input_types: Sequence[TensorType]
        :param cr_function: The function to evaluate.
        :type cr_function: Callable, optional
        :param param_argnums: the argument numbers of the parameters of the CR
        :type param_argnums: Sequence[int], optional
        :param params: the initial values of the parameters, default None
        :type params: Sequence[jnp.ndarray], optional
        :param cr_static_argnums: the static_argnums parameter for :func:`jax.jit` for your cr_function
        :type cr_static_argnums: Union[int,Iterable[int]], optional
        :param vmap:  should we :func:`jax.vmap` the CR function over the inputs? True if your CR is going to be
            given input values at multiple points on a mesh (i.e. if the input is one second-order tensor in
            3-d, and you plan to evaluate the CR at multiple points at once by stacking the inputs, you want
            this to be True), default True
        :type vmap: bool, optional
        :param nojit: if True, do NOT jit-compile the CR function, defaults to False
        :type nojit: bool, optional
        :param strain_energy: if True, implies that this CR has a strain energy function -- that is, ``cr_function`` is a scalar
            function that gives the strain energy as a function of a symmetric second-order input (and possibly other inputs), and the CR
            computes the stress as the derivative of strain energy with respect to the symmetric second-order input. Defaults to False
        :type strain_energy: bool, optional
        :return: a CR object
        :rtype: CR

        """
        self._out_type = output_type
        self._in_types = tuple(input_types)
        self._dims = max(
            tuple(max(x.shape) if len(x.shape) > 0 else 0 for x in self._in_types)
        )
        self._invariant_info = InvariantInfo(self._dims, self._in_types, self._out_type)
        self._strain_energy = strain_energy
        _, self._in_types = self._invariant_info.get_group_symbol(
            sanitize_input_types=True
        )

        ignore_warnings = self._out_type.order == 0
        self._scalar_invt_func, self._form_invt_func = get_invariant_functions(
            self._invariant_info, suppress_warning_print=ignore_warnings
        )
        if isinstance(cr_function, str):
            self.load_tensorflow_model(cr_function)
        else:
            self._f = cr_function

        if param_argnums == 0:
            param_argnums = (0,)
        self._param_argnums = param_argnums or []
        self._params = params or []
        self._diff_argnums = tuple(
            i for i in range(len(self._params) + len(self._in_types))
        )
        if len(self._param_argnums) != len(self._params):
            if len(self._param_argnums) == 0:
                logger.warning(
                    f"Passed {len(self._params)} params to CR.__init__(), but no corresponding param_argnums. Assuming the params are the last parameters of the function."
                )
                self._param_argnums = tuple(
                    len(self._in_types) + i for i in range(len(self._params))
                )
            else:
                raise ValueError(
                    f"Passed {len(self._params)} params to CR.__init__(), but {len(self._param_argnums)} param_argnums!"
                )

        self._num_scalar_invts = None
        self._form_invt_shape = (
            None  # shape of the result of a call to self.form_invt_func()
        )
        self._determine_invariants_shape()
        # cr function takes one array containing scalar invariants and some params
        self._total_num_inputs = 1 + len(self._param_argnums)
        self._vmap_axes = tuple(
            None if i in self._param_argnums else 0
            for i in range(self._total_num_inputs)
        )
        if self._f is None:
            vmap = False

        if vmap:
            self._scalar_invt_func = jax.vmap(
                self._scalar_invt_func
            )  # ,in_axes=tuple(0 for i in self._in_types))
            self._form_invt_func = jax.vmap(self._form_invt_func)
            self._invariant_evaluator = jax.vmap(partial(jnp.tensordot, axes=1))
            self._f = jax.vmap(self._f, in_axes=self._vmap_axes)
            batched_in_shapes = tuple(
                tuple([-1] + list(x.shape)) for x in self._in_types
            )
            batched_out_shape = tuple(
                [-1]
                + list(
                    self._out_type.shape
                    if not self._strain_energy
                    else (self._dims, self._dims)
                )
            )
        else:
            self._invariant_evaluator = partial(jnp.tensordot, axes=1)
            batched_in_shapes = tuple(x.shape for x in self._in_types)
            batched_out_shape = (
                self._out_type.shape
                if not self._strain_energy
                else (self._dims, self._dims)
            )

        self._nojit = nojit
        self._vmap = vmap
        self._static_argnums = cr_static_argnums

        # overload (the backend of) self.__call__() so we can differentiate it with JAX
        self._overloaded_call = self._make_overloaded_call()
        source = (
            DirectSum(JAXArrays(*batched_in_shapes))
            if len(batched_in_shapes) > 1
            else JAXArrays(batched_in_shapes[0])
        )
        target = JAXArrays(batched_out_shape)
        super().__init__(source, target)

    @staticmethod
    def from_arrays(
        example_output: jnp.ndarray,
        example_inputs: Iterable[jnp.ndarray],
        cr_function: Optional[Callable] = None,
        param_argnums: Optional[Iterable[int]] = None,
        params: Optional[Iterable[Array]] = None,
        cr_static_argnums: Optional[Sequence[int]] = None,
        vmap: bool = True,
        **kwargs,
    ):
        """The preferred way to construct a crikit.cr.CR if you don't want to manually construct the :class:`crikit.invariants.TensorType` s corresponding
        to your input and outputs tensor types. Ensure that, if your material has
        a structural tensor, you include it in `example_inputs`
        For example, a plank of wood is frequently modeled as being
        transverse-isotropic, with the structural tensor being a vector field
        pointing in the direction of the grain. If you want the symmetry to not include
        flips--that is, a subset of hemitropy instead of isotropy--ensure that you
        pass the Levi-Civita tensor (eps_ij or eps_ijk, depending on how many spatial
        dimensions you're in) as an :code:`example_input`, but DO NOT pass it into :func:`CR.__call__()`.
        If you pass the Levi-Civita tensor as an :code:`example_input`, we will account for
        its presence in the inputs without you passing it in.

        :param example_output: an example of what the output of the CR might look like; if that's a symmetric rank-two tensor,
            then example_output should also be that (e.g. :code:`jnp.eye(number_of_spatial_dimensions)`), etc.
        :type example_output: jnp.ndarray
        :param example_inputs: an iterable of JAX arrays of the same shape and symmetry as the inputs to the CR function
        :type example_inputs: Sequence[Array]
        :type cr_function: Either the function to evaluate OR a directory containing a saved TensorFlow model
            to load.
        :type cr_function: Union[function,str], optional
        :param param_argnums: the argument numbers of the parameters of the CR
        :type param_argnums: Iterable[int], optional
        :param params: the initial values of the parameters, default None
        :type params: Iterable[jnp.ndarray], optional
        :param cr_static_argnums: the static_argnums parameter for :func:`jax.jit` for your cr_function
        :type cr_static_argnums: Union[int,Iterable[int]], optional
        :param vmap:  should we :func:`jax.vmap` the CR function over the inputs? True if your CR is going to be
            given input values at multiple points on a mesh (i.e. if the input is one second-order tensor in
            3-d, and you plan to evaluate the CR at multiple points at once by stacking the inputs, you want
            this to be True), default True
        :type vmap: bool, optional
        :return: A crikit.cr.CR with the cr_input_shape (AKA number of scalar invariants) and num_form_invariants properties set.
        :rtype: CR

        """
        info = InvariantInfo.from_arrays(example_output, *example_inputs, **kwargs)
        cr = CR(
            info.output_type,
            info.input_types,
            cr_function=cr_function,
            param_argnums=param_argnums,
            params=params,
            static_argnums=cr_static_argnums,
            vmap=vmap,
            **kwargs,
        )
        return cr

    def __call__(self, *inputs, **kwargs) -> Union[ndarray, Tuple[ndarray]]:
        """Evaluates the CR

        :param \\*inputs: the inputs to the CR, as JAX arrays, or :class:`pyadjoint_utils.jax_adjoint.ndarray` s
           (if you're differentiating with Pyadjoint)
        :type \\*inputs: Union[Iterable[pyadjoint_utils.jax_adjoint.ndarray,jnp.ndarray]]
        :return: The value of the invariant CR function (self.function) evaluated
           with the scalar and form-invariants generated by `inputs`
        :rtype: Union[ndarray, Tuple[ndarray]]

        """
        try:
            self._check_inputs(inputs)
            params = kwargs.get("params", self._params)
            val = self._overloaded_call(inputs, *params)
            return val
        except Exception as e:
            print(
                f"""Caught exception in CR.__call__():
            {e}
            Recall that inputs to CR.__call__() are passed directly to the scalar and form-invariant calculating functions."""
            )
            raise e

    def set_params(self, new_params: Iterable[Array]) -> None:
        if len(new_params) != len(self._params):
            raise ValueError(
                f"Tried to set_params() with {len(new_params)} params, but this CR expects {len(self._params)}!"
            )
        self._params = new_params

    @partial(jax.jit, static_argnums=(0,))
    def _evaluate_scalar_jax_cr(self, *args):
        inputs = args[0]
        params = args[1:]
        scalar_invariants = self._scalar_invt_func(*inputs)
        return self._f(scalar_invariants, *params)

    def _nojit_evaluate_scalar_jax_cr(self, *args):
        inputs = args[0]
        params = args[1:]
        scalar_invariants = self._scalar_invt_func(*inputs)
        return self._f(scalar_invariants, *params)

    @partial(jax.jit, static_argnums=(0,))
    def _evaluate_jax_cr(self, *args):
        inputs = args[0]
        params = args[1:]
        scalar_invariants = self._scalar_invt_func(*inputs)
        form_invariants = self._form_invt_func(*inputs)
        scalar_function_values = self._f(scalar_invariants, *params)
        # the generalized Wineman-Pipkin theorem of Zheng and Boehler (1994) guarantees that an extremely broad class of tensor functions
        # -- broad enough that we can say that, for our purposes, all tensor functions -- with a physical symmetry can be represented
        # as a linear combination of scalar functions of the scalar invariants, and form invariant functions
        return self._invariant_evaluator(scalar_function_values, form_invariants)

    def _nojit_evaluate_jax_cr(self, *args):
        inputs = args[0]
        params = args[1:]
        scalar_invariants = self._scalar_invt_func(*inputs)
        form_invariants = self._form_invt_func(*inputs)
        scalar_function_values = self._f(scalar_invariants, *params)
        # the generalized Wineman-Pipkin theorem of Zheng and Boehler (1994) guarantees that an extremely broad class of tensor functions
        # -- broad enough that we can say that, for our purposes, all tensor functions -- with a physical symmetry can be represented
        # as a linear combination of scalar functions of the scalar invariants, and form invariant functions
        return self._invariant_evaluator(scalar_function_values, form_invariants)

    def load_tensorflow_model(self, directory: str) -> None:
        raise NotImplementedError  # not working right now
        import tensorflow as tf

        restored = tf.saved_model.load(directory)

        def model(invts, *params):
            return restored.f(
                tuple(tf.convert_to_tensor(x) for x in params),
                tf.convert_to_tensor(invts),
            )

        self._f = model

    def _make_overloaded_call(self):
        vmapped_argnums = []
        vmap_ax = self._vmap_axes if self._vmap else [None] * self._total_num_inputs
        for ax in vmap_ax:
            if ax is None:
                vmapped_argnums.append(False)
            else:
                vmapped_argnums.append(True)
        if self._nojit:
            if self._strain_energy:

                def g(*args):
                    outs, pullback = jax.vjp(self._evaluate_scalar_jax_cr, *args)
                    return pullback(jnp.ones_like(outs))[0][0]

                return overload_jax(
                    g,
                    function_name=(self._f.__name__ if self._f else "JAX CR"),
                    argnums=self._diff_argnums,
                    static_argnums=self._static_argnums,
                    nojit=self._nojit,
                    pointwise=vmapped_argnums,
                )
            f = (
                self._nojit_evaluate_jax_cr
                if self._out_type.order > 0
                else self._nojit_evaluate_scalar_jax_cr
            )
            return overload_jax(
                f,
                function_name=(self._f.__name__ if self._f else "JAX CR"),
                argnums=self._diff_argnums,
                static_argnums=self._static_argnums,
                nojit=self._nojit,
                pointwise=vmapped_argnums,
            )
        else:
            if self._strain_energy:

                def g(*args):
                    outs, pullback = jax.vjp(self._evaluate_scalar_jax_cr, *args)
                    return pullback(jnp.ones_like(outs))[0][0]

                return overload_jax(
                    g,
                    function_name=(self._f.__name__ if self._f else "JAX CR"),
                    argnums=self._diff_argnums,
                    static_argnums=self._static_argnums,
                    nojit=self._nojit,
                    pointwise=vmapped_argnums,
                )
            # tuple(i+1 for i in range(len(self._params))),
            f = (
                self._evaluate_jax_cr
                if self._out_type.order > 0
                else self._evaluate_scalar_jax_cr
            )
            return overload_jax(
                f,
                function_name=(self._f.__name__ if self._f else "JAX CR"),
                argnums=self._diff_argnums,
                static_argnums=self._static_argnums,
                nojit=self._nojit,
                pointwise=vmapped_argnums,
            )

    @property
    def cr_input_shape(self):
        """
        The shape of the array of scalar invariants that the CR function takes
        as its first parameter.
        """
        if self._num_scalar_invts is None:
            self._determine_invariants_shape()

        return (self._num_scalar_invts,)

    @property
    def form_invariant_shape(self):
        """
        The shape of the array of form invariants
        """
        if self._form_invt_shape is None:
            self._determine_invariants_shape()

        return self._form_invt_shape

    @property
    def num_scalar_functions(self):
        """
        The number of scalar functions we need to make (each taking in the scalar invariants)
        in order to right-multiply the row vector of them against the form invariants
        For example, in 3d, an O(3)-invariant function of a symmetric rank-two tensor
        and a vector that outputs a symmetric rank-two has a _form_invt_shape of (6,3,3),
        so we need 6 scalar functions to make the right row vector to get a result of shape (3,3)
        """
        return self.form_invariant_shape[0] if len(self.form_invariant_shape) > 0 else 1

    def invariant_descriptions(
        self, ipython: Optional[bool] = None, html: Optional[bool] = None
    ) -> str:
        """
        A string describing both the scalar and form invariant functions, including their
        indices in the input/output of the CR.

        :param ipython: Are you in IPython mode? (e.g. in a Jupyter notebook) By default,
            tries to guess whether or not you are in IPython mode; set this manually if the
            behavior is not as desired.
        :type ipython: bool, optional
        :param html: Return an HTML string instead of a plain-text string? defaults to None, unless
            ``ipython`` is True, then True
        :return: A string describing the invariants
        :rtype: str
        """
        return get_invariant_descriptions(
            self._invariant_info, ipython=ipython, html=html
        )

    @property
    def function(self):
        return self._f

    @function.setter
    def function(self, f):
        """
        Set the CR function

        :param f: a function to set as the CR function
        :return: None
        """
        if isinstance(f, str):
            self.load_tensorflow_model(f)
        else:
            self._f = f
        self._overloaded_call = self._make_overloaded_call()

    def scalar_invariants(self, *inputs) -> jnp.ndarray:
        """
        Computes scalar invariants given inputs

        :param \\*inputs: the inputs to the CR
        :type \\*inputs: Iterable[jnp.ndarray]
        :return: A JAX DeviceArray containing the scalar invariants
        :rtype: jnp.ndarray
        """
        return self._scalar_invt_func(*inputs)

    def form_invariants(self, *inputs):
        """
        Computes form invariants given inputs

        :param \\*inputs: the inputs to the CR
        :type \\*inputs: Iterable[jnp.ndarray]
        :return: A JAX DeviceArray containing the stacked form-invariants
        :rtype: jnp.ndarray
        """
        return self._form_invt_func(*inputs)

    def save_model(self, directory):
        """Save the internal function (the one you can pass as ``cr_function`` in :meth:`CR.__init__` ) of a
        JAX-based CR to a directory by converting it to a TensorFlow model
        and then saving that. You can recover the model by using :meth:`CR.load_tensorflow_model`.

        :param directory: The directory name to save it to
        :type directory: str

        :return: None

         .. todo:: figure out a format in which we can save both the input/output types of the CR and the tf model together so we can reconstruct a whole CR object from a file and check that it matches this object's input and output types

        """
        save_jax_cr(self, directory)

    def _check_inputs(self, inputs):
        if len(inputs) != len(self._in_types):
            raise ValueError(
                f"Expected {len(self._in_types)} inputs, but received {len(inputs)}!"
            )

        for i, (inpt, expected) in enumerate(zip(inputs, self._in_types)):
            shape = inpt.shape[1:] if self._vmap else inpt.shape
            if tuple(shape) != tuple(expected.shape):
                if expected.shape == ():
                    if shape == (1,):
                        continue

                raise ValueError(
                    f"Expected input {i+1} to have shape {expected.shape}, but it has {shape}!"
                )

    def _determine_invariants_shape(self):
        _, in_types = self._invariant_info.get_group_symbol(sanitize_input_types=True)
        example_inputs = tuple(ipt.get_array_like() for ipt in in_types)

        self._num_scalar_invts = self._scalar_invt_func(*example_inputs).size
        self._form_invt_shape = (
            self._form_invt_func(*example_inputs).shape
            if self._out_type.order > 0
            else ()
        )


def cr_function_shape(
    output: Union[Array, TensorType],
    inputs: Union[Sequence[TensorType], Sequence[Array]],
) -> Tuple[int, int]:
    """
    Computes the number of scalar invariants that a CR function for
    given inputs and outputs must take, as well as the number of scalar values
    that function must output to generate an invariant CR, and returns a tuple
    of (num_scalar_invariants,num_output_scalar_values).

    :param output: either an array (Numpy or JAX) or a TensorType representing the
       correct shape and symmetry of an output tensor from this CR.
    :type output: Union[Array,TensorType]
    :param inputs: an Iterable of either TensorType instances or arrays of the correct
       shape and symmetry as the input tensors of this CR; must contain the same
       type as output (i.e. if output is a TensorType, inputs must contain only
       TensorTypes, and likewise if output is an array, inputs must only contain
       arrays.
    :type inputs: Union[Sequence[TensorType], Sequence[Array]]
    :return: A tuple of (number of scalar invariants, number of output scalar values)
    :rtype: tuple
    """
    # NOTE: this definitely isn't the most efficient possible implementation, since constructing a CR does some other things that aren't
    # related to this computation, but this function is probably only called at most once per program execution during setup, and is
    # pretty cheap anyway
    if isinstance(output, TensorType):
        for ip in inputs:
            if not isinstance(ip, TensorType):
                raise TypeError(
                    f"If the output is a TensorType, all inputs must be TensorTypes, but you passed a {type(ip)}!"
                )
        cr = CR(output, inputs)

    array_types = (
        ndarray,
        jax.interpreters.xla.DeviceArray,
        jnp.ndarray,
        np.ndarray,
        float,
        int,
    )
    if isinstance(output, array_types):
        for ip in inputs:
            if not isinstance(ip, array_types):
                raise TypeError(
                    f"If the output is an array, all inputs must be arrays too, but you passed a {type(ip)}!"
                )
        cr = CR.from_arrays(output, inputs)

    num_scalar_invts = cr.cr_input_shape[0]
    num_scalar_funcs = cr.num_scalar_functions
    return (num_scalar_invts, num_scalar_funcs)


def save_jax_cr(cr: CR, directory: str):
    """Save a JAX-based CR to a directory by converting it to a TensorFlow model
    and then saving that. You can recover the model by using :meth:`CR.load_tensorflow_model`.

    :param cr: The CR to save
    :type cr: CR
    :param directory: The directory name to save it to
    :type directory: str

    :return: None

    """
    import tensorflow as tf
    from jax.experimental import jax2tf

    model = tf.Module()
    jax_dtype = get_default_dtype()
    tf_dtype = tf.float64 if jax_dtype == np.float64 else tf.dtype(jax_dtype)
    model.f = tf.function(
        jax2tf.convert(cr.function), autograph=False
    )  # , input_signature=[tf.TensorSpec(cr.cr_input_shape, tf_dtype)])

    tf.saved_model.save(model, directory)


class P_Laplacian(CR):
    """A CR that represents a p-Laplacian."""

    def __init__(self, p, spatial_dims=3, eps2=1.0e-12, vmap=True, strain_energy=False):
        input_types = (TensorType.make_symmetric(2, spatial_dims),)
        output_type = TensorType.make_scalar()
        self.eps2 = eps2
        cr_function = self._eval_p_laplacian
        super().__init__(
            output_type,
            input_types,
            cr_function,
            param_argnums=(1,),
            params=(p,),
            vmap=vmap,
            nojit=False,
            strain_energy=strain_energy,
        )

    def _eval_p_laplacian(self, scalar_invts, p):
        return (scalar_invts[1] + self.eps2) ** ((p - 2) / 2)


class RivlinModel(CR):
    """A CR that represents a Rivlin model -- that is, one of the form
    :math:`W = \sum\limits_{i=0}^n\sum\limits_{j=0}^n C_{ij} (I_1 - 3)^i (I_2 - 3)^j + \sum\limits_{k=1}^m D_k (J - 1)^{2k}`, where
    :math:`J = \mathrm{det}(B)`.
    """

    def __init__(self, C, D=None, spatial_dims=3, vmap=True, optimize_d=False):
        """

        :param C: The material constants :math:`C_{ij}`
        :type C: ndarray
        :param D: The material constants :math:`D_k`, defaults to None
        :type D: ndarray, optional
        :param spatial_dims: how many spatial dimensions? defaults to 3
        :type spatial_dims: int, optional
        :param vmap: the ``vmap`` parameter of :meth:`CR.__init__` , defaults to True
        :type vmap: bool, optional
        :param optimize_d: Controls which parameter we're optimizing the CR
            with respect to. If True, optimize ``D``, else optimize ``C``.
            Defaults to False.
        :type optimize_d: bool, optional
        :returns: a :class:`RivlinModel`
        :rtype: RivlinModel

        """

        self._C = C
        self._D = D
        self.incompressible = D is None
        self.n = C.shape[0]
        if C.shape[1] < C.shape[0]:
            raise ValueError("Must pass square array of parameter values C!")

        self.m = 0 if self.incompressible else D.size
        # inputs are just the left Cauchy-Green tensor
        input_types = (TensorType.make_symmetric(2, spatial_dims),)
        output_type = TensorType.make_scalar()
        cr_function = (
            self._eval_incompressible_rivlin_model
            if self.incompressible
            else self._eval_rivlin_model
        )
        if not self.incompressible:
            cr_function = (
                self._eval_rivlin_model_d if optimize_d else self._eval_rivlin_model
            )
        param_argnums = (1,)

        params = (D,) if optimize_d else (C,)
        super().__init__(
            output_type,
            input_types,
            cr_function,
            param_argnums=param_argnums,
            params=params,
            vmap=vmap,
            nojit=False,
            strain_energy=True,
        )
        self._params = params

    @property
    def C(self):
        return self._C

    @C.setter
    def set_C(self, new_C):
        self._params[0] = new_C
        self._C = new_C

    @property
    def D(self):
        return self._D

    @D.setter
    def set_D(self, new_D):
        self._params[1] = new_D
        self._D = new_D

    def _eval_rivlin_model(self, scalar_invts, C):
        I_1 = scalar_invts[0]
        I_2 = 0.5 * (scalar_invts[0] ** 2 - scalar_invts[1])
        J = self._det_from_traces(scalar_invts)

        W = np.array(0)
        for i in range(self.n):
            for j in range(self.n):
                W = W + C[i, j] * (I_1 - 3) ** i * (I_2 - 3) ** j

        for k in range(self.m):
            W = W + self._D[k] * (J - 1) ** (2 * k)

        return W

    def _eval_rivlin_model_d(self, scalar_invts, D):
        I_1 = scalar_invts[0]
        I_2 = 0.5 * (scalar_invts[0] ** 2 - scalar_invts[1])
        J = self._det_from_traces(scalar_invts)

        W = np.array(0)
        for i in range(self.n):
            for j in range(self.n):
                W = W + self._C[i, j] * (I_1 - 3) ** i * (I_2 - 3) ** j

        for k in range(self.m):
            W = W + D[k] * (J - 1) ** (2 * k)

        return W

    def _eval_incompressible_rivlin_model(self, scalar_invts, C):
        I_1 = scalar_invts[0]
        I_2 = 0.5 * (scalar_invts[0] ** 2 - scalar_invts[1])

        W = np.array(0)
        for i in range(self.n):
            for j in range(self.n):
                W = W + C[i, j] * (I_1 - 3) ** i * (I_2 - 3) ** j

        return W

    def _det_from_traces(self, scalar_invts):
        """
        The handy-dandy calculator at https://demonstrations.wolfram.com/TheDeterminantUsingTraces/
        tells us that the determinant of a 3-by-3 matrix :math:`A` is :math:`|A| = \frac{\text{tr}(A)^3}{6} - \frac{1}{2}\text{tr}(A^2)\text{tr}(A) + \frac{\text{tr}(A^3)}{3}`
        """
        ta, ta2, ta3 = scalar_invts[0], scalar_invts[1], scalar_invts[2]
        return (ta ** 3) / 6 - (ta2 * ta) / 2 + ta3 / 3
