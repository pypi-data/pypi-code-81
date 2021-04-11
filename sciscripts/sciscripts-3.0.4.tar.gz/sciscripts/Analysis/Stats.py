#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170612
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from rpy2 import robjects as RObj
from rpy2.robjects import packages as RPkg


## Level 0
def AdjustNaNs(Array):
    NaN = RObj.NA_Real

    for I, A in enumerate(Array):
        if A != A: Array[I] = NaN

    return(Array)


def PearsonRP(A,B):
    r = pearsonr(A, B)
    r = list(r)
    r[0] = round(r[0], 3)
    if r[1] < 0.05:
        r[1] = '%.1e' % r[1] + ' *'
    else:
        r[1] = str(round(r[1], 3))

    return(r)


def PToStars(p, Max=3):
    No = 0
    while p < 0.05 and No <= Max:
        p *=10
        No +=1

    return(No)


def RCheckPackage(Packages):
    RPacksToInstall = [Pack for Pack in Packages if not RPkg.isinstalled(Pack)]
    if len(RPacksToInstall) > 0:
        print(str(RPacksToInstall), 'not installed. Install now?')
        Ans = input('[y/N]: ')

        if Ans.lower() in ['y', 'yes']:
            from rpy2.robjects.vectors import StrVector as RStrVector

            RUtils = RPkg.importr('utils')
            RUtils.chooseCRANmirror(ind=1)

            RUtils.install_packages(RStrVector(RPacksToInstall))

        else: print('Aborted.')

    return(None)


## Level 1
def RPCA(Matrix):
    RCheckPackage(['stats']); Rstats = RPkg.importr('stats')

    RMatrix = RObj.Matrix(Matrix)
    PCA = Rstats.princomp(RMatrix)
    return(PCA)


def RAnOVaOneWay(Data, Factor):
    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    Values = RObj.FloatVector(Data)
    Factor = RObj.FactorVector(Factor)

    Frame = RObj.DataFrame({
        'Values': Values,
        'Factor': Factor,
    })

    RObj.globalenv["Frame"] = Frame
    RObj.globalenv["Values"] = Values
    RObj.globalenv["Factor"] = Factor
    Model = RObj.r('''anova_test(Frame, Values ~ Factor)''')

    return(Model)


def RAnOVaTwoWay(Data, Factor1, Factor2, Id=[]):
    RCheckPackage(['rstatix']); RPkg.importr('rstatix')

    RepeatedMeasures = True if len(Id) else False

    Values = RObj.FloatVector(Data)
    Factors = [RObj.FactorVector(_) for _ in [Factor1, Factor2]]
    Frame = {
        'Values': Values,
        'Factor1': Factors[0],
        'Factor2': Factors[1],
    }

    if RepeatedMeasures:
        Idv = RObj.IntVector(Id)
        RObj.globalenv["Id"] = Idv
        Frame['Id'] = Idv

    Frame = RObj.DataFrame(Frame)

    RObj.globalenv["Frame"] = Frame
    RObj.globalenv["Values"] = Values
    RObj.globalenv["Factor1"] = Factors[0]
    RObj.globalenv["Factor2"] = Factors[1]

    if RepeatedMeasures:
        Model = RObj.r('''anova_test(Frame, dv=Values, wid=Id, within=c(Factor1,Factor2))''')
    else:
        Model = RObj.r('''anova_test(Frame, Values ~ Factor1*Factor2)''')

    return(Model)


def RAnOVaPwr(GroupNo=RObj.NULL, SampleSize=RObj.NULL, Power=RObj.NULL,
           SigLevel=RObj.NULL, EffectSize=RObj.NULL):
    RCheckPackage(['pwr']); Rpwr = RPkg.importr('pwr')

    Results = Rpwr.pwr_anova_test(k=GroupNo, power=Power, sig_level=SigLevel,
                                  f=EffectSize, n=SampleSize)

    print('Running', Results.rx('method')[0][0] + '... ', end='')
    AnOVaResults = {}
    for Key, Value in {'k': 'GroupNo', 'n': 'SampleSize', 'f': 'EffectSize',
                       'power':'Power', 'sig.level': 'SigLevel'}.items():
        AnOVaResults[Value] = Results.rx(Key)[0][0]

    print('Done.')
    return(AnOVaResults)


def RModelToDict(Model):
    Dict = {
        C: np.array(Col.levels)
        if 'Factor' in C and np.array(Col).dtype == np.int32
        else np.array(Col)
        for C,Col in Model.items()
    }

    return(Dict)


def RTTest(DataA, DataB, Paired=True, EqualVar=False, Alt='two.sided', Confidence=0.95):
    RCheckPackage(['rstatix']); RPkg.importr('rstatix')
    Rttest = RObj.r['t.test']
    RCohensD = RObj.r['cohens_d']

    DataA = AdjustNaNs(DataA); DataB = AdjustNaNs(DataB)

    Results = Rttest(RObj.FloatVector(DataA), RObj.FloatVector(DataB),
                     paired=Paired, var_equal=EqualVar, alternative=Alt,
                     conf_level=RObj.FloatVector([Confidence]),
                     na_action=RObj.r['na.omit'])

    TTestResults = {}; Names = list(Results.names)
    for Name in Names:
        TTestResults[Name] = Results.rx(Name)[0][0]

    Values = RObj.FloatVector(np.concatenate((DataA, DataB)))
    Factor = RObj.FactorVector(['A']*len(DataA)+['B']*len(DataB))

    Frame = RObj.DataFrame({
        'Values': Values,
        'Factor': Factor,
    })

    RObj.globalenv["Confidence"] = Confidence
    RObj.globalenv["EqualVar"] = EqualVar
    RObj.globalenv["Factor"] = Factor
    RObj.globalenv["Frame"] = Frame
    RObj.globalenv["Paired"] = Paired
    RObj.globalenv["Values"] = Values
    Model = RObj.r('''cohens_d(Frame, Values ~ Factor, conf.level=Confidence, var.equal=EqualVar, paired=Paired)''')
    TTestResults['CohensD'] = RModelToDict(Model)

    return(TTestResults)


## Level 2
def AnOVa(Data, Factor1, Factor2=[], Id=[], Paired=[True, True]):
    TwoWay = True if len(Factor2) else False
    RepeatedMeasures = True if len(Id) else False
    ColsAnOVa = ['Effect', 'DFn', 'DFd', 'F', 'p', 'p<.05', 'ges', 'p.adj']
    ColsSph = ['Effect', 'W', 'p', 'p<.05']
    ColsSphCorr = ['Effect', 'GGe', 'DF[GG]', 'p[GG]', 'p[GG]<.05', 'HFe', 'DF[HF]', 'p[HF]']
    ColsPWC = [['Factor', '.y.', 'group1', 'group2', 'n1', 'n2']]*2
    ColsPWC = [
        Cols + ['statistic', 'df', 'p', 'p.adj', 'p.adj.signif']
        if Paired[C] else
        Cols + ['p', 'p.signif', 'p.adj', 'p.adj.signif']
        for C,Cols in enumerate(ColsPWC)
    ]

    if TwoWay:
        if RepeatedMeasures:
            Model = RAnOVaTwoWay(Data, Factor1, Factor2, Id)
        else:
            Model = RAnOVaTwoWay(Data, Factor1, Factor2)
    else:
        Model = RAnOVaOneWay(Data, Factor1)

    if RepeatedMeasures:
        FXs = {
            'Factor1': RObj.r('''Frame %>% group_by(Factor2) %>% anova_test(dv=Values, wid=Id, within=Factor1) %>% get_anova_table() %>% adjust_pvalue(method="bonferroni")'''),
            'Factor2': RObj.r('''Frame %>% group_by(Factor1) %>% anova_test(dv=Values, wid=Id, within=Factor2) %>% get_anova_table() %>% adjust_pvalue(method="bonferroni")''')
        }

        Paired = ['TRUE' if _ else 'FALSE' for _ in Paired]
        PWC = {
            'Factor1': RObj.r('''Frame %>% group_by(Factor2) %>% pairwise_t_test(Values~Factor1, paired='''+Paired[0]+r''', p.adjust.method="bonferroni")'''),
            'Factor2': RObj.r('''Frame %>% group_by(Factor1) %>% pairwise_t_test(Values~Factor2, paired='''+Paired[1]+r''', p.adjust.method="bonferroni")''')
        }

        if Model.rclass[1] == 'list':
            Results = {
                'ANOVA': RModelToDict(Model[0]),
                'MauchlySphericity': RModelToDict(Model[1]),
                'SphericityCorrection': RModelToDict(Model[2]),
                'FXFactors': {F: RModelToDict(Fac) for F,Fac in FXs.items()},
                'PWCs': {F: RModelToDict(Fac) for F,Fac in PWC.items()}
            }
        else:
            Results = {
                'ANOVA': RModelToDict(Model),
                'FXFactors': {F: RModelToDict(Fac) for F,Fac in FXs.items()},
                'PWCs': {F: RModelToDict(Fac) for F,Fac in PWC.items()}
            }

    else:
        Results = {'ANOVA': RModelToDict(Model)}

    return(Results)

