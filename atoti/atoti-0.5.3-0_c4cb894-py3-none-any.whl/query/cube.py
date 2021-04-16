from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Tuple, Union

from .._base._base_cube import BaseCube
from .._docs_utils import doc
from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._multi_condition import MultiCondition
from .._type_utils import BASE_SCENARIO, ScenarioName
from ._mdx_utils import generate_mdx
from ._widget_conversion import WidgetConversionDetails
from .hierarchies import QueryHierarchies
from .level import QueryLevel
from .levels import QueryLevels
from .measure import QueryMeasure
from .measures import QueryMeasures
from .query_result import QueryResult

if TYPE_CHECKING:
    from .session import QuerySession

_EXPLAIN_QUERY_DOC = """Run the query but return an explanation of how the query was executed instead of its result.

        See also:
            :meth:`{corresponding_method}` for the roles of the parameters.

        Returns:
            An explanation containing a summary, global timings, and the query plan with all the retrievals.
        """

_QUERY_ARGS_DOC = """Args:
            measures: The measures to query.
                If ``None``, all the measures are queried.
            condition: The filtering condition.
                Only conditions on level equality with a string are supported.

                Examples:

                    .. doctest:: query

                        >>> cube.query(
                        ...     m["Price.SUM"],
                        ...     levels=[lvl["Country"]],
                        ...     condition=lvl["Continent"] == "Europe",
                        ... )
                                                 Price.SUM
                        Continent Country
                        Europe    France            200.00
                                  Germany           150.00
                                  United Kingdom    120.00


                        >>> cube.query(
                        ...     m["Price.SUM"],
                        ...     levels=[lvl["Country"], lvl["Currency"]],
                        ...     condition=(
                        ...         (lvl["Continent"] == "Europe")
                        ...         & (lvl["Currency"] == "EUR")
                        ...     ),
                        ... )
                                                   Price.SUM
                        Continent Country Currency
                        Europe    France  EUR         200.00
                                  Germany EUR         150.00

                        >>> cube.query(
                        ...     m["Price.SUM"],
                        ...     levels=[lvl["Country"]],
                        ...     condition=h["Geography"].isin(
                        ...         ("America",), ("Europe", "Germany")
                        ...     ),
                        ... )
                                                Price.SUM
                        Continent Country
                        America   Mexico           270.00
                                  United states    240.00
                        Europe    Germany          150.00

            include_totals: Whether the returned DataFrame should include the grand total and subtotals.
                Totals can be useful but they make the DataFrame harder to work with since its index will have some empty values.

                Example:

                    .. doctest:: query

                            >>> cube.query(
                            ...     m["Price.SUM"],
                            ...     levels=[lvl["Country"], lvl["Currency"]],
                            ...     include_totals=True,
                            ... )
                                                              Price.SUM
                            Continent Country        Currency
                            Total                                980.00
                            America                              510.00
                                      Mexico                     270.00
                                                     MXN         270.00
                                      United states              240.00
                                                     USD         240.00
                            Europe                               470.00
                                      France                     200.00
                                                     EUR         200.00
                                      Germany                    150.00
                                                     EUR         150.00
                                      United Kingdom             120.00
                                                     GBP         120.00

            levels: The levels to split on.
                If ``None``, the value of the measures at the top of the cube is returned.
            scenario: The scenario to query.
            timeout: The query timeout in seconds.
"""


_QUERY_DOC = """Query the cube to retrieve the value of the passed measures on the given levels.

        In JupyterLab with the :mod:`atoti-jupyterlab <atoti_jupyterlab>` plugin installed, query results can be converted to interactive widgets with the :guilabel:`Convert to Widget Below` action available in the command palette or by right clicking on the representation of the returned Dataframe.

        .. doctest:: query
            :hide:

            >>> df = pd.DataFrame(
            ...     columns=["Continent", "Country", "Currency", "Price"],
            ...     data=[
            ...         ("Europe", "France", "EUR", 200.0),
            ...         ("Europe", "Germany", "EUR", 150.0),
            ...         ("Europe", "United Kingdom", "GBP", 120.0),
            ...         ("America", "United states", "USD", 240.0),
            ...         ("America", "Mexico", "MXN", 270.0),
            ...     ],
            ... )
            >>> store = session.read_pandas(
            ...     df, keys=["Continent", "Country", "Currency"], store_name="Prices"
            ... )
            >>> cube = session.create_cube(store)
            >>> h, lvl, m = cube.hierarchies, cube.levels, cube.measures
            >>> del h["Continent"]
            >>> del h["Country"]
            >>> h["Geography"] = [store["Continent"], store["Country"]]

        {args}
"""


@dataclass(frozen=True)
class QueryCube(BaseCube[QueryHierarchies, QueryLevels, QueryMeasures]):
    """Query cube."""

    _session: QuerySession = field(repr=False)

    @property
    def levels(self) -> QueryLevels:
        """Levels of the cube."""
        return QueryLevels(self.hierarchies)

    def _generate_mdx(
        self,
        *,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        include_totals: bool,
        levels: Sequence[QueryLevel],
        measures: Sequence[QueryMeasure],
        scenario: ScenarioName,
    ) -> str:
        (
            level_conditions,
            level_isin_conditions,
            hierarchy_isin_conditions,
        ) = _decombine_condition(condition)

        return generate_mdx(
            cube=self,
            hierarchy_isin_conditions=hierarchy_isin_conditions,
            include_totals=include_totals,
            level_conditions=level_conditions,
            level_isin_conditions=level_isin_conditions,
            levels=levels,
            measures=measures,
            scenario=scenario,
        )

    @doc(_QUERY_DOC, args=_QUERY_ARGS_DOC)
    def query(
        self,
        *measures: QueryMeasure,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
        include_totals: bool = False,
        levels: Optional[Union[QueryLevel, Sequence[QueryLevel]]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
        **kwargs: Any,
    ) -> QueryResult:
        levels = [levels] if isinstance(levels, QueryLevel) else (levels or [])

        mdx = self._generate_mdx(
            condition=condition,
            include_totals=include_totals,
            levels=levels,
            measures=measures,
            scenario=ScenarioName(scenario),
        )

        query_result = self._session.query_mdx(
            mdx, keep_totals=include_totals, timeout=timeout, **kwargs
        )

        # Remove this branch when https://github.com/activeviam/atoti/issues/1943 is done.
        if not measures:
            query_result._atoti_widget_conversion_details = None

        # Always use an MDX including totals because ActiveUI 5 then relies on context values to show/hide totals.
        if not include_totals and query_result._atoti_widget_conversion_details:
            query_result._atoti_widget_conversion_details = WidgetConversionDetails(
                mdx=self._generate_mdx(
                    condition=condition,
                    include_totals=True,
                    levels=levels,
                    measures=measures,
                    scenario=ScenarioName(scenario),
                ),
                session_name=query_result._atoti_widget_conversion_details.session_name,
                widget_creation_code=query_result._atoti_widget_conversion_details.widget_creation_code,
            )

        return query_result


def _decombine_condition(
    condition: Optional[
        Union[
            LevelCondition,
            MultiCondition,
            LevelIsInCondition,
            HierarchyIsInCondition,
        ]
    ] = None,
) -> Tuple[
    Sequence[LevelCondition],
    Sequence[LevelIsInCondition],
    Sequence[HierarchyIsInCondition],
]:
    level_conditions: List[LevelCondition] = []
    level_isin_conditions: List[LevelIsInCondition] = []
    hierarchy_isin_conditions: List[HierarchyIsInCondition] = []

    if condition is not None:
        if isinstance(condition, LevelCondition):
            level_conditions.append(condition)
        elif isinstance(condition, LevelIsInCondition):
            level_isin_conditions.append(condition)
        elif isinstance(condition, HierarchyIsInCondition):
            hierarchy_isin_conditions.append(condition)
        elif isinstance(condition, MultiCondition):

            measure_conditions = condition._measure_conditions
            if measure_conditions:
                raise ValueError(
                    f"Multi-conditions with measures are not supported when querying cube:"
                    f" {measure_conditions}"
                )
            level_conditions += condition._level_conditions
            level_isin_conditions += condition._level_isin_conditions
            hierarchy_isin_conditions += condition._hierarchy_isin_condition

        else:
            raise TypeError(f"Unexpected type of query condition: f{type(condition)}")

    return level_conditions, level_isin_conditions, hierarchy_isin_conditions
