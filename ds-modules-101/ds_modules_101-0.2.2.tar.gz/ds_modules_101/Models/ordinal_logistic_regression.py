# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 20:24:42 2015
Author: Josef Perktold
License: BSD-3
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from scipy import stats

from statsmodels.tools.decorators import cache_readonly
from statsmodels.base.model import (
    GenericLikelihoodModel, GenericLikelihoodModelResults)
from statsmodels.compat.pandas import Appender
# for results wrapper:
import statsmodels.regression.linear_model as lm
import statsmodels.base.wrapper as wrap
import statsmodels.api as sm


class OrderedModel(GenericLikelihoodModel):
    """Ordinal Model based on logistic or normal distribution
    The parameterization corresponds to the proportional odds model.
    The mode assumes that the endogenous variable is ordered but that the
    labels have no numeric interpretation besides the ordering.
    The model is based on a latent linear variable, where we observe only a
    discretization.
    y_latent = X beta + u
    The observed variable is defined by the interval
    y = {0 if y_latent <= cut_0
         1 of cut_0 < y_latent <= cut_1
         ...
         K if cut_K < y_latent
    The probability of observing y=k conditional on the explanatory variables
    X is given by
    prob(y = k | x) = Prob(cut_k < y_latent <= cut_k+1)
                    = Prob(cut_k - x beta < u <= cut_k+1 - x beta
                    = F(cut_k+1 - x beta) - F(cut_k - x beta)
    Where F is the cumulative distribution of u which is either the normal
    or the logistic distribution, but can be set to any other continuous
    distribution. We use standardized distributions to avoid identifiability
    problems.
    
    EXAMPLE USAGE:#################
    from ds_modules_101.Models import OrderedModel
    from ds_modules_101.Data import titanic_df

    # get filter for the columns we want
    temp= titanic_df[['Pclass','Sex']].copy()

    # removing nans
    temp = temp[~temp.isna().any(axis=1)].copy()

    # encoding sex column to 0 and 1
    temp['male'] = temp['Sex'].apply(lambda x: x=='male').astype('int')

    # get the responce variable and predictor variables
    y = temp['Pclass']
    X = temp[['male']]

    myModel = OrderedModel(y,X,distr='logit')

    myModel=myModel.fit()
    smy = myModel.summary()
    print(smy)
    print('Log')
    myModel.check_parallel_lines_assumption()
    myModel.summary_extra()
    ###############################
    
    Parameters
    ----------
    endog : array_like
        Endogenous or dependent ordered categorical variable with k levels.
        Labels or values of endog will internally transformed to consecutive
        integers, 0, 1, 2, ...
        pd.Series with ordered Categorical as dtype should be preferred as it
        gives the order relation between the levels.
        If endog is not a pandas Categorical, then categories are
        sorted in lexicographic order (by numpy.unique).
    exog : array_like
        Exogenous, explanatory variables. This should not include an intercept.
        pd.DataFrame are also accepted.
        see Notes about constant when using formulas
    offset : array_like
        Offset is added to the linear prediction with coefficient equal to 1.
    distr : string 'probit' or 'logit', or a distribution instance
        The default is currently 'probit' which uses the normal distribution
        and corresponds to an ordered Probit model. The distribution is
        assumed to have the main methods of scipy.stats distributions, mainly
        cdf, pdf and ppf. The inverse cdf, ppf, is only use to calculate
        starting values.
    Notes
    -----
    Status: experimental, core results are verified, still subclasses
        `GenericLikelihoodModel` which will change in future versions.
    The parameterization of OrderedModel requires that there is no constant in
    the model, neither explicit nor implicit. The constant is equivalent to
    shifting all thresholds and is therefore not separately identified.
    Patsy's formula specification does not allow a design matrix without
    explicit or implicit constant if there are categorical variables (or maybe
    splines) among explanatory variables. As workaround, statsmodels removes an
    explit intercept.
    Consequently, there are two valid cases to get a design matrix without
    intercept when using formulas:
    - specify a model without explicit and implicit intercept which is possible
      if there are only numerical variables in the model.
    - specify a model with an explicit intercept which statsmodels will remove.
    Models with an implicit intercept will be overparameterized, the parameter
    estimates will not be fully identified, cov_params will not be invertible
    and standard errors might contain nans. The computed results will be
    dominated by numerical imprecision coming mainly from convergence tolerance
    and numerical derivatives.
    The model will raise a ValueError if a remaining constant is detected.
    """
    _formula_max_endog = np.inf

    def __init__(self, endog, exog, offset=None, distr='probit', **kwds):

        if distr == 'probit':
            self.distr = stats.norm
        elif distr == 'logit':
            self.distr = stats.logistic
        else:
            self.distr = distr

        if offset is not None:
            offset = np.asarray(offset)

        self.offset = offset

        endog, labels, is_pandas = self._check_inputs(endog, exog)

        super(OrderedModel, self).__init__(endog, exog, **kwds)
        k_levels = None  # initialize
        if not is_pandas:
            if self.endog.ndim == 1:
                unique, index = np.unique(self.endog, return_inverse=True)
                self.endog = index
                labels = unique
            elif self.endog.ndim == 2:
                if not hasattr(self, "design_info"):
                    raise ValueError("2-dim endog not supported")
                # this branch is currently only in support of from_formula
                # we need to initialize k_levels correctly for df_resid
                k_levels = self.endog.shape[1]
                labels = []
                # Note: Doing the following here would break from_formula
                # self.endog = self.endog.argmax(1)

        if self.k_constant > 0:
            raise ValueError("there should not be a constant in the model")

        self._initialize_labels(labels, k_levels=k_levels)

        # adjust df
        self.k_extra = self.k_levels - 1
        self.df_model = self.k_vars + self.k_extra
        self.df_resid = self.nobs - self.df_model

        self.results_class = OrderedResults

    def _check_inputs(self, endog, exog):
        """handle endog that is pandas Categorical
        checks if self.distrib is legal and provides Pandas ordered Categorical
        support for endog.
        Parameters
        ----------
        endog : array_like
            Endogenous, dependent variable, 1-D.
        exog : array_like
            Exogenous, explanatory variables.
            Currently not used.
        Returns
        -------
        endog : array_like or pandas Series
            If the original endog is a pandas ordered Categorical Series,
            then the returned endog are the ``codes``, i.e. integer
            representation of ordere categorical variable
        labels : None or list
            If original endog is pandas ordered Categorical Series, then the
            categories are returned. Otherwise ``labels`` is None.
        is_pandas : bool
            This is True if original endog is a pandas ordered Categorical
            Series and False otherwise.
        """

        if not isinstance(self.distr, stats.rv_continuous):
            import warnings
            msg = (
                f"{self.distr.name} is not a scipy.stats distribution."
            )
            warnings.warn(msg)

        labels = None
        is_pandas = False
        if isinstance(endog, pd.Series):
            if isinstance(endog.dtypes, CategoricalDtype):
                if not endog.dtype.ordered:
                    warnings.warn("the endog has ordered == False, "
                                  "risk of capturing a wrong order for the "
                                  "categories. ordered == True preferred.",
                                  Warning)

                endog_name = endog.name
                labels = endog.values.categories
                endog = endog.cat.codes
                if endog.min() == -1:  # means there is a missing value
                    raise ValueError("missing values in categorical endog are "
                                     "not supported")
                endog.name = endog_name
                is_pandas = True

        return endog, labels, is_pandas

    def _initialize_labels(self, labels, k_levels=None):
        self.labels = labels
        if k_levels is None:
            self.k_levels = len(labels)
        else:
            self.k_levels = k_levels

        if self.exog is not None:
            self.nobs, self.k_vars = self.exog.shape
        else:  # no exog in model
            self.nobs, self.k_vars = self.endog.shape[0], 0

        threshold_names = [str(x) + '/' + str(y)
                           for x, y in zip(labels[:-1], labels[1:])]

        # from GenericLikelihoodModel.fit
        if self.exog is not None:
            # avoid extending several times
            if len(self.exog_names) > self.k_vars:
                raise RuntimeError("something wrong with exog_names, too long")
            self.exog_names.extend(threshold_names)
        else:
            self.data.xnames = threshold_names

    @classmethod
    def from_formula(cls, formula, data, subset=None, drop_cols=None,
                     *args, **kwargs):

        # we want an explicit Intercept in the model that we can remove
        # Removing constant with "0 +" or "- 1" does not work for categ. exog

        endog_name = formula.split("~")[0].strip()
        original_endog = data[endog_name]

        model = super(OrderedModel, cls).from_formula(
            formula, data=data, drop_cols=["Intercept"], *args, **kwargs)

        if model.endog.ndim == 2:
            if not (isinstance(original_endog.dtype, CategoricalDtype)
                    and original_endog.dtype.ordered):
                msg = ("Only ordered pandas Categorical are supported as "
                       "endog in formulas")
                raise ValueError(msg)

            labels = original_endog.values.categories
            model._initialize_labels(labels)
            model.endog = model.endog.argmax(1)
            model.data.ynames = endog_name

        return model

    def cdf(self, x):
        """cdf evaluated at x
        """
        return self.distr.cdf(x)

    def pdf(self, x):
        """pdf evaluated at x
        """
        return self.distr.pdf(x)

    def prob(self, low, upp):
        """interval probability
        Probability that value is in interval (low, upp], computed as
            prob = cdf(upp) - cdf(low)
        Parameters
        ----------
        low : array_like
            lower bound for interval
        upp : array_like
            upper bound for interval
        Returns
        -------
        float or ndarray
            Probability that value falls in interval (low, upp]
        """
        return np.maximum(self.cdf(upp) - self.cdf(low), 0)

    def transform_threshold_params(self, params):
        """transformation of the parameters in the optimization
        Parameters
        ----------
        params : nd_array
            Contains (exog_coef, transformed_thresholds) where exog_coef are
            the coefficient for the explanatory variables in the linear term,
            transformed threshold or cutoff points. The first, lowest threshold
            is unchanged, all other thresholds are in terms of exponentiated
            increments.
        Returns
        -------
        thresh : nd_array
            Thresh are the thresholds or cutoff constants for the intervals.
        """
        th_params = params[-(self.k_levels - 1):]
        thresh = np.concatenate((th_params[:1],
                                 np.exp(th_params[1:]))).cumsum()
        thresh = np.concatenate(([-np.inf], thresh, [np.inf]))
        return thresh

    def transform_reverse_threshold_params(self, params):
        """obtain transformed thresholds from original thresholds or cutoffs
        Parameters
        ----------
        params : ndarray
            Threshold values, cutoff constants for choice intervals, which
            need to be monotonically increasing.
        Returns
        -------
        thresh_params : ndarrray
            Transformed threshold parameter.
            The first, lowest threshold is unchanged, all other thresholds are
            in terms of exponentiated increments.
            Transformed parameters can be any real number without restrictions.
        """
        thresh_params = np.concatenate((params[:1],
                                        np.log(np.diff(params[:-1]))))
        return thresh_params

    def predict(self, params, exog=None, offset=None, which="prob"):
        """predicted probabilities for each level of the ordinal endog.
        Parameters
        ----------
        params : ndarray
            Parameters for the Model, (exog_coef, transformed_thresholds)
        exog : array_like, optional
            Design / exogenous data. Is exog is None, model exog is used.
        offset : array_like, optional
            Offset is added to the linear prediction with coefficient
            equal to 1. If offset is not provided and exog
            is None, uses the model's offset if present.  If not, uses
            0 as the default value.
        which : {"prob", "linpred", "cumprob"}
            Determines which statistic is predicted
            - prob : predicted probabilities to be in c
            - linear : 1-dim linear prediction of the latent variable
            ``x b + offset``
            - cumprob : predicted cumulative propability to be in choice k or
              lower
        Returns
        -------
        predicted probabilities : ndarray
            2-dim predicted probabilites with observations in rows and one
            column for each category or level of the categorical dependent
            variable.
        """
        # note, exog and offset handling is in linpred

        thresh = self.transform_threshold_params(params)
        xb = self._linpred(params, exog=exog, offset=offset)
        if which == "linpred":
            return xb

        xb = xb[:, None]
        low = thresh[:-1] - xb
        upp = thresh[1:] - xb
        if which == "prob":
            prob = self.prob(low, upp)
            return prob
        elif which in ["cum", "cumprob"]:
            cumprob = self.cdf(upp)
            return cumprob
        else:
            raise ValueError("`which` is not available")

    def _linpred(self, params, exog=None, offset=None):
        """linear prediction of latent variable `x b`
        currently only for exog from estimation sample (in-sample)
        Parameters
        ----------
        params : ndarray
            Parameters for the model, (exog_coef, transformed_thresholds)
        exog : array_like, optional
            Design / exogenous data. Is exog is None, model exog is used.
        offset : array_like, optional
            Offset is added to the linear prediction with coefficient
            equal to 1. If offset is not provided and exog
            is None, uses the model's offset if present.  If not, uses
            0 as the default value.
        Returns
        -------
        linear : ndarray
            1-dim linear prediction given by exog times linear params plus
            offset. This is the prediction for the underlying latent variable.
            If exog and offset are None, then the predicted values are zero.
        """
        if exog is None:
            exog = self.exog
            if offset is None:
                offset = self.offset
        else:
            if offset is None:
                offset = 0

        if offset is not None:
            offset = np.asarray(offset)

        if exog is not None:
            linpred = exog.dot(params[:-(self.k_levels - 1)])
        else:  # means self.exog is also None
            linpred = np.zeros(self.nobs)
        if offset is not None:
            linpred += offset
        return linpred

    def _bounds(self, params):
        """integration bounds for the observation specific interval
        This defines the lower and upper bounds for the intervals of the
        choices of all observations.
        The bounds for observation are given by
            a_{k_i-1} - linpred_i, a_k_i - linpred_i
        where
        - k_i is the choice in observation i.
        - a_{k_i-1} and a_k_i are thresholds (cutoffs) for choice k_i
        - linpred_i is the linear prediction for observation i
        Parameters
        ----------
        params : ndarray
            Parameters for the model, (exog_coef, transformed_thresholds)
        Return
        ------
        low : ndarray
            Lower bounds for choice intervals of each observation,
            1-dim with length nobs
        upp : ndarray
            Upper bounds for choice intervals of each observation,
            1-dim with length nobs.
        """
        thresh = self.transform_threshold_params(params)

        thresh_i_low = thresh[self.endog]
        thresh_i_upp = thresh[self.endog + 1]
        xb = self._linpred(params)
        low = thresh_i_low - xb
        upp = thresh_i_upp - xb
        return low, upp

    @Appender(GenericLikelihoodModel.fit.__doc__)
    def loglike(self, params):

        return self.loglikeobs(params).sum()

    @Appender(GenericLikelihoodModel.fit.__doc__)
    def loglikeobs(self, params):

        low, upp = self._bounds(params)
        prob = self.prob(low, upp)
        return np.log(prob + 1e-20)

    def score_obs_(self, params):
        """score, first derivative of loglike for each observations
        This currently only implements the derivative with respect to the
        exog parameters, but not with respect to threshold parameters.
        """
        low, upp = self._bounds(params)

        prob = self.prob(low, upp)
        pdf_upp = self.pdf(upp)
        pdf_low = self.pdf(low)

        # TODO the following doesn't work yet because of the incremental exp
        # parameterization. The following was written base on Greene for the
        # simple non-incremental parameterization.
        # k = self.k_levels - 1
        # idx = self.endog
        # score_factor = np.zeros((self.nobs, k + 1 + 2)) #+2 avoids idx bounds
        #
        # rows = np.arange(self.nobs)
        # shift = 1
        # score_factor[rows, shift + idx-1] = -pdf_low
        # score_factor[rows, shift + idx] = pdf_upp
        # score_factor[:, 0] = pdf_upp - pdf_low
        score_factor = (pdf_upp - pdf_low)[:, None]
        score_factor /= prob[:, None]

        so = np.column_stack((-score_factor[:, :1] * self.exog,
                              score_factor[:, 1:]))
        return so

    @property
    def start_params(self):
        """start parameters for the optimization corresponding to null model
        The threshold are computed from the observed frequencies and
        transformed to the exponential increments parameterization.
        The parameters for explanatory variables are set to zero.
        """
        # start params based on model without exog
        freq = np.bincount(self.endog) / len(self.endog)
        start_ppf = self.distr.ppf(np.clip(freq.cumsum(), 0, 1))
        start_threshold = self.transform_reverse_threshold_params(start_ppf)
        start_params = np.concatenate((np.zeros(self.k_vars), start_threshold))
        return start_params

    @Appender(GenericLikelihoodModel.fit.__doc__)
    def fit(self, start_params=None, method='nm', maxiter=500, full_output=1,
            disp=1, callback=None, retall=0, **kwargs):

        fit_method = super(OrderedModel, self).fit
        mlefit = fit_method(start_params=start_params,
                            method=method, maxiter=maxiter,
                            full_output=full_output,
                            disp=disp, callback=callback, **kwargs)
        # use the proper result class
        ordmlefit = OrderedResults(self, mlefit)

        # TODO: temporary, needs better fix, modelwc adds 1 by default
        ordmlefit.hasconst = 0

        result = OrderedResultsWrapper(ordmlefit)

        return result


class OrderedResults(GenericLikelihoodModelResults):

    def pred_table(self):
        """prediction table
        returns pandas DataFrame
        """
        # todo: add category labels
        categories = np.arange(self.model.k_levels)
        observed = pd.Categorical(self.model.endog,
                                  categories=categories, ordered=True)
        predicted = pd.Categorical(self.predict().argmax(1),
                                   categories=categories, ordered=True)
        table = pd.crosstab(predicted,
                            observed.astype(int),
                            margins=True,
                            dropna=False).T.fillna(0)
        return table

    @cache_readonly
    def llnull(self):
        """
        Value of the loglikelihood of model without explanatory variables
        """
        params_null = self.model.start_params
        return self.model.loglike(params_null)

    # next 3 are copied from discrete
    @cache_readonly
    def prsquared(self):
        """
        McFadden's pseudo-R-squared. `1 - (llf / llnull)`
        """
        return 1 - self.llf/self.llnull

    @cache_readonly
    def llr(self):
        """
        Likelihood ratio chi-squared statistic; `-2*(llnull - llf)`
        """
        return -2*(self.llnull - self.llf)

    @cache_readonly
    def llr_pvalue(self):
        """
        The chi-squared probability of getting a log-likelihood ratio
        statistic greater than llr.  llr has a chi-squared distribution
        with degrees of freedom `df_model`.
        """
        # number of restrictions is number of exog
        return stats.distributions.chi2.sf(self.llr, self.model.k_vars)

    @cache_readonly
    def resid_prob(self):
        """probability residual
        Probability-scale residual is ``P(Y < y) − P(Y > y)`` where `Y` is the
        observed choice and ``y`` is a random variable corresponding to the
        predicted distribution.
        References
        ----------
        Shepherd BE, Li C, Liu Q (2016) Probability-scale residuals for
        continuous, discrete, and censored data.
        The Canadian Jouranl of Statistics. 44:463–476.
        Li C and Shepherd BE (2012) A new residual for ordinal outcomes.
        Biometrika. 99: 473–480
        """
        from statsmodels.stats.diagnostic_gen import prob_larger_ordinal_choice
        endog = self.model.endog
        fitted = self.predict()
        r = prob_larger_ordinal_choice(fitted)[1]
        resid_prob = r[np.arange(endog.shape[0]), endog]
        return resid_prob
    
    def check_parallel_lines_assumption(self):
        myModel = sm.MNLogit(self.endog, sm.add_constant(self.exog))
        myModel = myModel.fit()
        self.llmulti = myModel.llf
        self.evidence_against=stats.distributions.chi2.sf(df=max([1,self.df_model-2]),x=(-2*self.llf)-(-2*myModel.llf))
        self.evidence_against_multinomial_for_ordinal=stats.distributions.chi2.sf(df=max([1,self.df_model-2]),x=(-2*myModel.llf)-(-2*self.llf))
        self.evidence_against_multinomial=myModel.llr_pvalue
        print('Log-Likelihood of null model = {}'.format(myModel.llnull))
        print('Log-Likelihood of full logistic regression model = {}'.format(myModel.llf))
        print('Log-Likelihood of full ordinal logistic regression model = {}'.format(self.llf))
        print('Evidence against null (intercept only) model in favour of multinomial model = {}'.format(self.evidence_against_multinomial))
        print('Evidence against null (intercept only) model in favour of ordinal model = {}'.format(self.llr_pvalue))
        print('Evidence against Multinomial model in favour of proportional odds = {}'.format(self.evidence_against_multinomial_for_ordinal))
        print('Evidence against proportional odds model in favour of Multinomial= {}'.format(self.evidence_against))
        
    def summary_extra(self):
        warn = ''
        s=self.summary()
        t=s.tables[0]

        t[3][2].data='Log-Likelihood Null'.rjust(21)
        t[3][3].data=str(round(self.llnull,15))[:21].rjust(8)
        
        try:    
            t[4][2].data='Log-Likelihood Multinomial'[:21].rjust(21)
            t[4][3].data=str(round(self.llmulti,15))[:21].rjust(8)
            t[5][2].data='Dev. Null vs Multi'[:21].rjust(21)
            t[5][3].data=str(round(self.evidence_against_multinomial,15))[:21].rjust(8)
            t[6][2].data='Dev. Multi | Ordinal'[:21].rjust(21)
            t[6][3].data=(str(round(self.evidence_against_multinomial_for_ordinal,6))+' | '+ str(round(self.evidence_against,6)))[:21].rjust(8)
        except:
            t[4][2].data='Log-Likelihood Multinomial'[:21].rjust(21)
            t[4][3].data=''[:21].rjust(8)
            t[5][2].data='Dev. Null vs Multi'[:21].rjust(21)
            t[5][3].data=''[:21].rjust(8)
            t[6][2].data='Dev. Multi | Ordinal'[:21].rjust(21)
            t[6][3].data=''[:21].rjust(8)
            
            warn = 'Warning: Run check_parallel_lines_assumption() first for deviance against multinomial'



        t[7][2].data='Dev. Null vs Ordinal'[:21].rjust(21)
        t[7][3].data=str(round(self.llr_pvalue,15))[:21].rjust(8)
        s.extra_txt = 'Dev. Null vs Ordinal: Evidence against intercept only model in favour of proportional odds model'
        s.extra_txt = s.extra_txt+'\n'+'Dev. Multinomial | Ordinal: Evidence against multinomial in favour of proportional odds model | Evidence against proportional odds model in favour of multinomial'
        s.extra_txt = s.extra_txt+'\n'+'Dev. Null vs Multinomial: Evidence against intercept only model in favor of Multinomial'
        s.extra_txt = s.extra_txt+'\n'+warn
        
        return s


class OrderedResultsWrapper(lm.RegressionResultsWrapper):
    pass


wrap.populate_wrapper(OrderedResultsWrapper, OrderedResults)