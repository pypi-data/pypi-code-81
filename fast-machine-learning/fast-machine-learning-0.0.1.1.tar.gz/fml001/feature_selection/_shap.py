
import shap, numpy as np
from shap.explainers import *
from shap.explainers.other import *
from collections.abc import Iterable
import copy
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 600

flags = dict(
    sk=1,
    xgb=1,
    cat=1,
    lgb=1,
    inte=1,
    
    )

EXPLAINER = [
    Tree,
    GPUTree,
    Linear,
    Permutation,
    Partition,
    Sampling,
    Additive,
    Exact,
    Maple,
    TreeGain,
    TreeMaple,
    LimeTabular,
    Coefficent,
    Random
    ]

try:
    # expliciluy require this experimetal feature if using sklearn.ensembkle.Hist*
    from sklearn.experimental import enable_hist_gradient_boosting  # noqa
    from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
    from sklearn.svm import SVR
    from sklearn.dummy import DummyRegressor
    from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor, \
        ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor, \
        StackingRegressor, VotingRegressor, HistGradientBoostingRegressor
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.linear_model import PassiveAggressiveRegressor, SGDRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
    from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.dummy import DummyClassifier
    from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, \
        ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier, \
        StackingClassifier, VotingClassifier, HistGradientBoostingClassifier
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier, \
        RidgeClassifier, SGDClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
except:
    flags["sk"] = 0


try:
    from catboost import CatBoostRegressor
    from catboost import CatBoostClassifier
except:
    flags["cat"] = 0

try:
    from interpret.glassbox import ExplainableBoostingRegressor
    from interpret.glassbox import ExplainableBoostingClassifier
except:
    flags["inte"] = 0

try:
    from lightgbm import LGBMRegressor
    from lightgbm import LGBMClassifier
except:
    flags["lgb"] = 0

try:
    from xgboost import XGBRegressor
    from xgboost import XGBClassifier
except:
    flags["xgb"] = 0

permutation_list = []
tree_list = []
linear_list = []
additive_list = []
if flags["sk"] == 1:
    permutation_list += [
        KNeighborsClassifier, 
        KNeighborsRegressor, 
        SVC, SVR, 
        DummyClassifier, 
        DummyRegressor,
        AdaBoostClassifier, 
        AdaBoostRegressor, 
        BaggingClassifier, 
        BaggingRegressor, 
        MLPClassifier, 
        MLPRegressor, 
        ]
    tree_list += [
        ExtraTreeClassifier, 
        ExtraTreeRegressor, 
        GradientBoostingClassifier, 
        GradientBoostingRegressor, 
        RandomForestRegressor, 
        RandomForestClassifier, 
        HistGradientBoostingClassifier, 
        HistGradientBoostingRegressor, 
        DecisionTreeClassifier, 
        DecisionTreeRegressor,
        ]
    linear_list += [
        LogisticRegression, 
        PassiveAggressiveClassifier, 
        PassiveAggressiveRegressor, 
        RidgeClassifier, 
        SGDClassifier, 
        SGDRegressor,
        ]
if flags["xgb"] == 1:
    tree_list += [
        XGBClassifier, 
        XGBRegressor
        ]
if flags["lgb"] == 1:
    tree_list += [
        LGBMClassifier, 
        LGBMRegressor
        ]
if flags["inte"] == 1:
    additive_list += [
        ExplainableBoostingClassifier, 
        ExplainableBoostingRegressor
        ]
if flags["cat"] == 1:
    tree_list += [
        CatBoostClassifier, 
        CatBoostRegressor
        ]


class Shap:
    
    def __init__(self):
        self.model = None
        self.X = None
        self.Y = None
        pass
    
    def fit(self, model, X, Y, explainer="auto", feature_names=None, shap_kwargs=dict(), model_kwargs=dict()):
        self.model = model
        self.X = X
        self.Y = Y
        if explainer in EXPLAINER:
            Explainer = explainer
        else:
            Explainer = self.select_explainer()
        
        if feature_names is None:
            self.feature_names = np.array(range(X.shape[1]))
        else:
            self.feature_names = np.array(feature_names).astype(str)
        
        if Explainer != Linear:
            shap_kwargs.update(dict(feature_names=self.feature_names))
        self.explainer = Explainer(model(**model_kwargs).fit(X, Y), X, **shap_kwargs)
        self.shap_values = self.explainer(X)
        self.feature_importance = self.shap_values.abs.mean(0).values
        self.feature_shap = np.array(sorted(enumerate(self.feature_importance), key=lambda x: x[1], reverse=True))
        self.feature_importance = self.feature_shap[:, 1]
        self.feature_index = self.feature_shap[:, 0].astype(int)
        return self
    
    def select_explainer(self):
        
        if self.model in permutation_list:
            if self.X.shape[0] < 100 and self.X.shape[1] < 20:
                Explainer = Exact
            else:
                Explainer = Permutation
        elif self.model in linear_list:
            Explainer = Linear
        elif self.model in tree_list:
            Explainer = Tree
        elif self.model in additive_list:
            Explainer = Additive
        else:
            raise ValueError("No model matches with shap explainers")
        return Explainer
    
    def bar(self, max_display=10, xlabel="SHAP values", textcolor=None, barcolor=None):
        from shap.plots import colors
        from shap.utils._general import format_value
        import seaborn as sns; sns.set()
                
        if isinstance(textcolor, Iterable) and not isinstance(textcolor, str):
            textcolor = textcolor
        elif isinstance(textcolor, str):
            textcolor = [textcolor, textcolor]
        else:
            textcolor = [colors.blue_rgb, colors.red_rgb]
        if isinstance(barcolor, Iterable) and not isinstance(barcolor, str):
            barcolor = barcolor
        elif isinstance(barcolor, str):
            barcolor = [barcolor, barcolor]
        else:
            barcolor = [colors.blue_rgb, colors.red_rgb]
        
        values = self.shap_values.abs.mean(0).values
        feature_names = copy.deepcopy(self.feature_names)
        show_features_index = self.feature_index[:max_display]
        values[show_features_index[-1]] = values[self.feature_index[max_display:]].sum()
        num_cut = len(self.feature_index) - max_display + 1
        # feature_names[show_features_index[-1]] = f"Sum of {num_cut} other features"
        show_values = values[show_features_index]
        show_features = feature_names[show_features_index].tolist()
        show_features[-1] = f"Sum of {num_cut} other features"
        y_pos = np.arange(max_display, 0, -1)
        y_ticklabels = np.array(show_features)
        
        fig, ax = plt.subplots(1, figsize=(8, max_display * 0.5 + 1.5))
        
        negative_values_present = np.sum(show_values < 0) > 0
        if negative_values_present:
            ax.axvline(0, 0, 1, color="#000000", linestyle="-", linewidth=1, zorder=1)
        
        bar_width = 0.7
        ax.barh(
            y_pos, show_values,
            bar_width, align='center',
            color=[barcolor[0] if show_values[j] <= 0 else barcolor[1] for j in range(len(y_pos))],
            edgecolor=(1,1,1,0.8)
        )
        
        xlen = ax.get_xlim()[1] - ax.get_xlim()[0]
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width = bbox.width
        bbox_to_xscale = xlen/width

        for j in range(len(y_pos)):
            if show_values[j] < 0:
                ax.text(
                    show_values[j] - (5/72)*bbox_to_xscale, y_pos[j], format_value(show_values[j], '%+0.02f'),
                    horizontalalignment='right', verticalalignment='center', color=textcolor[0],
                    fontsize=12
                )
            else:
                ax.text(
                    show_values[j] + (5/72)*bbox_to_xscale, y_pos[j], format_value(show_values[j], '%+0.02f'),
                    horizontalalignment='left', verticalalignment='center', color=textcolor[1],
                    fontsize=12
                )
        
        for i in range(max_display):
            ax.axhline(i+1, color="#888888", lw=0.5, dashes=(1, 5), zorder=-1)
        
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('none')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if negative_values_present:
            ax.spines['left'].set_visible(False)
        ax.tick_params('x', labelsize=11)
        
        xmin,xmax = ax.get_xlim()
        ymin,ymax = ax.get_ylim()
        
        if negative_values_present:
            ax.set_xlim(xmin - (xmax-xmin)*0.05, xmax + (xmax-xmin)*0.05)
        else:
            ax.set_xlim(xmin, xmax + (xmax-xmin)*0.05)
        
        ax.set_xlabel(xlabel, fontsize=13)
        
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(y_ticklabels.tolist(), fontsize=13)

if __name__ == "__main__":
    from sklearn.datasets import load_boston, load_breast_cancer
    X, Y = load_breast_cancer(return_X_y=True)
    s = Shap().fit(XGBClassifier, X, Y, feature_names=load_breast_cancer().feature_names)
    s.feature_importance
    s.feature_shap
    s.feature_index
    # shap.plots.bar(s.shap_values)
    s.bar()
    s.shap_values
