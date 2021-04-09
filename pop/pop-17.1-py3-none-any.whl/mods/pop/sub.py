"""
Control and add subsystems to the running daemon hub
"""
import os
from collections.abc import Mapping
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Iterator
from typing import List
from typing import Tuple

import pop.hub


def add(
    hub: pop.hub.Hub,
    pypath: List[str] or str = None,
    subname: str = None,
    sub: pop.hub.Sub = None,
    static: List[str] or str = None,
    contracts_pypath: List[str] or str = None,
    contracts_static: List[str] or str = None,
    default_contracts: List[str] or str = None,
    virtual: bool = True,
    dyne_name: str = None,
    omit_start: Tuple[str] = ("_",),
    omit_end: Tuple[str] = (),
    omit_func: bool = False,
    omit_class: bool = True,
    omit_vars: bool = False,
    mod_basename: str = "pop.sub",
    stop_on_failures: bool = False,
    init: bool = True,
    load_all: bool = True,
    recursive_contracts_static: List[str] or str = None,
    default_recursive_contracts: List[str]
    or str = None,  # TODO: Not str, pretty sure -W. Werner, 2020-10-20
):
    """
    Add a new subsystem to the hub
    :param hub: The redistributed pop central hub
    :param subname: The name that the sub is going to take on the hub
        if nothing else is passed, it is used as the pypath (TODO make it the dyne_name not the pypath)
    :param sub: The sub to use as the root to add to
    :param pypath: One or many python paths which will be imported
    :param static: Directories that can be explicitly passed
    :param contracts_pypath: Load additional contract paths
    :param contracts_static: Load additional contract paths from a specific directory
    :param default_contracts: Specifies that a specific contract plugin will be applied as a default to all plugins
    :param virtual: Toggle whether or not to process __virtual__ functions
    :param dyne_name: The dynamic name to use to look up paths to find plugins -- linked to conf.py
    :param omit_start: Allows you to pass in a tuple of characters that would omit the loading of any object
        I.E. Any function starting with an underscore will not be loaded onto a plugin
        (You should probably never change this)
    :param omit_end:Allows you to pass in a tuple of characters that would omit the loading of an object
        (You should probably never change this)
    :param omit_func: bool: Don't load any functions
    :param omit_class: bool: Don't load any classes
    :param omit_vars: bool: Don't load any vars
    :param mod_basename: str: Manipulate the location in sys.modules that the plugin will be loaded to.
        Allow plugins to be loaded into a separate namespace.
    :param stop_on_failures: If any module fails to load for any reason, stacktrace and do not continue loading this sub
    :param init: bool: determine whether or not we process __init__ functions
    :param load_all: Load all the plugins on the sub
    """
    if pypath:
        pypath = pop.hub.ex_path(pypath)
        subname = subname if subname else pypath[0].split(".")[-1]
    elif static:
        subname = subname if subname else os.path.basename(static)
    if dyne_name:
        subname = subname if subname else dyne_name
    root = sub or hub
    root._subs[subname] = pop.hub.Sub(
        hub,
        subname,
        root,
        pypath,
        static,
        contracts_pypath,
        contracts_static,
        default_contracts,
        virtual,
        dyne_name,
        omit_start,
        omit_end,
        omit_func,
        omit_class,
        omit_vars,
        mod_basename,
        stop_on_failures,
        init=init,
        sub_virtual=getattr(root, "_subvirt", True),
        recursive_contracts_static=recursive_contracts_static,
        default_recursive_contracts=default_recursive_contracts,
    )
    # init the sub (init.py:__init__) after it can be referenced on the hub!
    root._subs[subname]._sub_init()
    root._iter_subs = sorted(root._subs.keys())
    if load_all:
        root._subs[subname]._load_all()
    for alias in root._subs[subname]._alias:
        root._sub_alias[alias] = subname


def remove(hub: pop.hub.Hub, subname: str):
    """
    Remove a pop from the hub, run the shutdown if needed
    :param hub: The redistributed pop central hub
    :param subname: The name that the sub is going to take on the hub
        if nothing else is passed, it is used as the pypath (TODO make it the dyne_name not the pypath)
    """
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        if hasattr(sub, "init"):
            mod = getattr(sub, "init")
            if hasattr(mod, "shutdown"):
                mod.shutdown()
        hub._remove_subsystem(subname)


def load_all(hub: pop.hub.Hub, subname: str) -> bool:
    """
    Load all modules under a given pop
    :param hub: The redistributed pop central hub
    :param subname: The name that the sub is going to take on the hub
        if nothing else is passed, it is used as the pypath (TODO make it the dyne_name not the pypath)
    """
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        sub._load_all()
        return True
    else:
        return False


def get_dirs(hub: pop.hub.Hub, sub: pop.hub.Sub) -> List[str]:
    """
    Return a list of directories that contain the modules for this subname
    :param hub: The redistributed pop central hub
    :param sub: The pop object that contains the loaded module data
    """
    return sub._dirs


def iter_subs(
    hub: pop.hub.Hub, sub: pop.hub.Sub, recurse: bool = False
) -> Generator[pop.hub.Sub, None, None]:
    """
    Return an iterator that will traverse just the subs. This is useful for
    nested subs
    :param hub: The redistributed pop central hub
    :param recurse: Recursively iterate over nested subs
    """
    for name in sorted(sub._subs):
        ret = sub._subs[name]
        if ret._sub_virtual:
            yield ret
            if recurse:
                if hasattr(ret, "_subs"):
                    yield from hub.pop.sub.iter_subs(ret, recurse)


def load_subdirs(hub: pop.hub.Hub, sub: pop.hub.Sub, recurse: bool = False):
    """
    Given a sub, load all subdirectories found under the sub into a lower namespace
    :param hub: The redistributed pop central hub
    :param sub: The pop object that contains the loaded module data
    :param recurse: Recursively iterate over nested subs
    """
    if not sub._sub_virtual:
        return
    dirs = hub.pop.sub.get_dirs(sub)
    roots = {}
    for dir_ in dirs:
        for fn in os.listdir(dir_):
            if fn.startswith("_"):
                continue
            if fn == "contracts":
                continue
            full = os.path.join(dir_, fn)
            if not os.path.isdir(full):
                continue
            if fn not in roots:
                roots[fn] = [full]
            else:
                roots[fn].append(full)
    for name, sub_dirs in roots.items():
        # Load er up!
        hub.pop.sub.add(
            subname=name,
            sub=sub,
            static=sub_dirs,
            virtual=sub._virtual,
            omit_start=sub._omit_start,
            omit_end=sub._omit_end,
            omit_func=sub._omit_func,
            omit_class=sub._omit_class,
            omit_vars=sub._omit_vars,
            mod_basename=sub._mod_basename,
            stop_on_failures=sub._stop_on_failures,
        )
        if recurse:
            if isinstance(getattr(sub, name), pop.hub.Sub):
                hub.pop.sub.load_subdirs(getattr(sub, name), recurse)


def reload(hub: pop.hub.Hub, subname: str):
    """
    Instruct the hub to reload the modules for the given sub. This does not call
    the init.new function or remove sub level variables. But it does re-read the
    directory list and re-initialize the loader causing all modules to be re-evaluated
    when started.
    :param hub: The redistributed pop central hub
    :param subname: The name that the sub is going to take on the hub
        if nothing else is passed, it is used as the pypath (TODO make it the dyne_name not the pypath)
    """
    if hasattr(hub, subname):
        sub = getattr(hub, subname)
        sub._prepare()
        return True
    else:
        return False


def extend(
    hub: pop.hub.Hub,
    subname: str,
    pypath: List[str] or str = None,
    static: List[str] or str = None,
    contracts_pypath: List[str] or str = None,
    contracts_static: List[str] or str = None,
) -> bool:
    """
    Extend the directory lookup for a given sub. Any of the directory lookup
    arguments can be passed.
    :param hub: The redistributed pop central hub
    :param subname: The name that the sub is going to take on the hub
        if nothing else is passed, it is used as the pypath (TODO make it the dyne_name not the pypath)
    :param pypath: One or many python paths which will be imported
    :param static: Directories that can be explicitly passed
    :param contracts_pypath: Load additional contract paths
    :param contracts_static: Load additional contract paths from a specific directory
    """
    if not hasattr(hub, subname):
        return False
    sub = getattr(hub, subname)
    if pypath:
        sub._pypath.extend(pop.hub.ex_path(pypath))
    if static:
        sub._static.extend(pop.hub.ex_path(static))
    if contracts_pypath:
        sub._contracts_pypath.extend(pop.hub.ex_path(contracts_pypath))
    if contracts_static:
        sub._contracts_static.extend(pop.hub.ex_path(contracts_static))
    sub._prepare()
    return True


def dynamic(hub: pop.hub.Hub, sub: pop.hub.Sub, get_reference: Callable):
    """
    Create dynamic subs underneath the named sub.
    When a dynamic sub is called, determine the actual path that should be used
    and call the reference with the parameters passed to the Dynamic Sub

    :param hub: The redistributed pop central hub
    :param sub: The sub to modify to have dynamic subs underneath it
    :param get_reference: A callable function that returns the desired target base sub
    """

    class Dynamic(Mapping):
        def __init__(
            self,
            parent_sub: pop.hub.Sub,
            subs: Dict[str, pop.hub.Sub],
            ref: str = "",
        ):
            """
            :param parent_sub: The sub that owns the Dynamic subs
            :param subs: The subs that belonged to the parent sub
            :param ref: The names of Dynamic subs that led up to this reference
            """
            self._sub = parent_sub
            self._subs = subs
            self._ref = ref

        def __getitem__(self, name: str) -> pop.hub.Sub:
            """
            If the sub exists in the parent sub dictionary, return it directly.
            If the sub does not exist in the parent, then create a CallableSub
            that can be used to call the desired function when the ref has been fully built.
            :param name: The name of the sub to return
            """
            # Return the sub if it exists, this is a static reference
            if name in self._subs:
                return self._subs[name]
            else:
                # Check if one of our static subs has the name we are looking for
                for static_sub in self._subs.values():
                    if name in static_sub._alias:
                        return static_sub

            # We are working with an unresolved reference

            # Keep track of the dynamic reference chain that has led up to the current dynamic sub
            if self._ref:
                ref = f"{self._ref}.{name}"
            else:
                ref = name

            # In case the unresolved reference happens to be a function, create a callable sub
            callable_sub = CallableSub(
                hub=hub, subname=name, root=self._sub, init=False, ref=ref
            )

            # Any subsequent references are just as unresolved as this one, replace subs with Dynamic subs
            callable_sub._subs = Dynamic(callable_sub, {}, ref)
            return callable_sub

        # These methods maintain the functionality of being a mapping of sub-names to subs
        def __setitem__(self, name: str, new_sub: pop.hub.Sub):
            self._subs[name] = new_sub

        def __len__(self) -> int:
            return len(self._subs)

        def __iter__(self) -> Iterator[str]:
            return iter(self._subs)

    class CallableSub(pop.hub.Sub):
        """
        A Sub that transforms a Dynamic reference on the hub to a static reference and calls it.
        """

        def __init__(self, ref: str, *args, **kwargs):
            self._ref = ref
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            # Get the actual base reference based on user logic
            func = get_reference(*args, **kwargs)
            # Transform the built reference determined by parent dynamic subs into a real function located on the hub
            for ref in self._ref.split("."):
                func = getattr(func, ref)

            if isinstance(func, CallableSub):
                # If the reference didn't resolve, we need to preventan infinite recursion error
                full_ref = sub._subname
                sub_root = sub._root
                while isinstance(sub_root, pop.hub.Sub):
                    full_ref = f"{sub_root._subname}.{full_ref}"
                    sub_root = sub_root._root
                raise ModuleNotFoundError(
                    f"Reference does not exist {full_ref}.{self._ref}"
                )

            # Call the target function with the parameters passed to the callable sub
            return func(*args, **kwargs)

    # replace the _subs dict with a dynamically referenced version
    sub._subs = Dynamic(sub, sub._subs)
