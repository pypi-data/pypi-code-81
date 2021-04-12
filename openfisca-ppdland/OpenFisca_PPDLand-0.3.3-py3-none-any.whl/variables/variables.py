
import numpy as np

from openfisca_core.model_api import *
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles


from ppdland.entities import *


class salary(Variable):
    value_type = float
    entity = Individu
    label = "Salary"
    definition_period = YEAR


class potential_salary(Variable):
    value_type = float
    entity = Individu
    label = "Potential salary"
    definition_period = YEAR


class pension(Variable):
    value_type = float
    entity = Individu
    label = "Pension"
    definition_period = YEAR


class income_tax(Variable):
    value_type = float
    entity = Individu
    label = "Income tax"
    definition_period = YEAR

    def formula(individu, period, parameters):
        salary = individu('salary', period)
        pension = individu('pension', period)
        taxable_income = salary + pension
        tax_scale = parameters(period).tax_scale
        return tax_scale.calc(taxable_income)


# class minimum_income(Variable):
#     value_type = float
#     entity = Individu
#     definition_period = YEAR

#     def formula(individu, period, parameters):
#         salary = individu('salary', period)
#         pension = individu('pension', period)
#         minimum_income = parameters(period).minimum_income
#         return max_((minimum_income - salary - pension), 0)


class disposable_income(Variable):
    definition_period = YEAR
    label = "Disposable income"
    entity = Individu
    value_type = float

    def formula(individu, period):
        salary = individu('salary', period)
        pension = individu('pension', period)
        income_tax = individu('income_tax', period)
        return salary + pension - income_tax


class pre_tax_income(Variable):
    definition_period = YEAR
    label = "Pre-tax income"
    entity = Individu
    value_type = float

    def formula(individu, period):
        salary = individu('salary', period)
        pension = individu('pension', period)
        return salary + pension


class pre_tax_income_decile(Variable):
    value_type = int
    entity = Individu
    label = "Pre-tax income decile"
    definition_period = YEAR

    def formula(individu, period):
        pre_tax_income = individu('pre_tax_income', period)
        labels = np.arange(1, 11)
        weights = 1.0 * np.ones(shape = len(pre_tax_income))
        decile, _ = mark_weighted_percentiles(
            pre_tax_income,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile
