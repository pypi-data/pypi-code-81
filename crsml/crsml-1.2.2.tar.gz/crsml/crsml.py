from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,recall_score,f1_score,average_precision_score,roc_auc_score,accuracy_score,confusion_matrix
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import scikitplot as skplt
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import matplotlib as mpl

def run_random_forest(X_data,Y_data,test_size=0.0,model_path="rmf.pkl",n_estimators=100,random_state=0):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    if test_size==0:
        clf.fit(X_data, Y_data)
        pickle.dump(clf, open(model_path, 'wb'))
        print(accuracy_score(Y_data,clf.predict(X_data)))
    else:
        X_train,X_test,y_train,y_test=train_test_split(X_data,Y_data,test_size=test_size)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open(model_path, 'wb'))

        y_pred=clf.predict(X_test)
        print(y_pred)
        print(accuracy_score(y_test,y_pred))
        print(precision_score(y_test,y_pred))
        print(recall_score(y_test,y_pred))
        print(f1_score(y_test,y_pred))
        print(average_precision_score(y_test,y_pred))
        print(roc_auc_score(y_test,y_pred))
        print(confusion_matrix(y_test,y_pred))

def search_best_random_forest(X_data,Y_data,cv=5,model_path="",params={}):
    clf = RandomForestClassifier(random_state=0)

    if len(params)==0:
        parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    else:
        n_estimators=params.get("n_estimators")
        max_depth=params.get("max_depth")
        if n_estimators and max_depth and isinstance(n_estimators, list) and isinstance(max_depth, list):
            parameters = {'n_estimators': n_estimators, 'max_depth': max_depth}
        else:
            print("------params参数错误------")
            parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    gsearch = GridSearchCV(estimator=clf, param_grid=parameters, scoring='accuracy', cv=cv)
    gsearch.fit(X_data, Y_data)
    print("gsearch.best_params_", gsearch.best_params_)
    print("gsearch.best_score_", gsearch.best_score_)
    print("gsearch.best_estimator_", gsearch.best_estimator_)

    x_data = ['d' + str(f['max_depth']) + 'n' + str(f['n_estimators']) for f in gsearch.cv_results_['params']]
    y_data = gsearch.cv_results_['mean_test_score']
    draw_linear_plot(x_data,y_data,fig_size=(20,8),font_size=15)

    gsearch.best_estimator_.fit(X_data, Y_data)
    if model_path:
        pickle.dump(clf, open(model_path, 'wb'))
    else:
        pickle.dump(clf, open(f"best_rmf_n_estimators_{gsearch.best_params_.get('n_estimators')}_max_depth_{gsearch.best_params_.get('max_depth')}.pkl", 'wb'))
    return gsearch

def evaluate_random_forest(X_data,Y_data,cv=5,n_estimators=100,max_depth=20):
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=0)
    scores = cross_val_score(clf, X_data, Y_data, cv=cv, scoring='accuracy')
    print(scores)
    print(sum(scores)/cv)

def draw_analyse_plot(X_data,Y_data,model=None,figsize=(16,8),feature_names=None,):
    draw_pca_2d_projection(X_data,Y_data)

    # draw_histogram_plot(normal_data, mal_data, labels)
    if model:
        draw_feature_importances(model,feature_names=feature_names,figsize=figsize)
        draw_learning_curve(model, X_data, Y_data,cv=5,figsize=figsize)


def draw_confusion_matrix(y, predictions, normalize=False, title=None,figsize=(16,8)):
    skplt.metrics.plot_confusion_matrix(y,predictions,normalize=normalize,title=title,figsize=figsize)
    plt.show()

def draw_roc(y, prediction_probas,title='ROC Curves',figsize=(16,8)):
    skplt.metrics.plot_roc(y, prediction_probas,title=title,figsize=figsize)
    plt.show()

def draw_precision_recall_curve(y, prediction_probas,title='Precision-Recall Curve',curves=('micro', 'each_class'),figsize=(16,8)):
    skplt.metrics.plot_precision_recall_curve(y, prediction_probas,title=title,curves=curves,figsize=figsize)
    plt.show()

def draw_learning_curve(clf, X, y,title='Learning Curve', cv=None,figsize=(16,8)):
    skplt.classifiers.plot_learning_curve(clf, X, y,title=title, cv=cv,figsize=figsize)
    plt.show()

def draw_feature_importances(clf,title='Feature Importance',feature_names=None, max_num_features=200,order='descending',figsize=(16,8)):
    skplt.classifiers.plot_feature_importances(clf, title=title,feature_names=feature_names, max_num_features=max_num_features,order=order,figsize=figsize)
    plt.show()

def draw_pca_2d_projection(X, y, title='PCA 2-D Projection',figsize=(16,8)):
    pca = PCA(random_state=1)
    pca.fit(X)
    skplt.decomposition.plot_pca_2d_projection(pca, X, y,title=title,figsize=figsize)
    plt.show()

def draw_histogram_plot(normal_data,mal_data,labels,bar_width=0.35,names=('正常', '恶意'),title="正常与恶意对比",y_label='数值',font_size=13,font_sans='Arial Unicode MS',fig_size=(20, 6),bar_color=('#0072BC','#ED1C24'),legend_loc='up'):
    x = np.arange(len(labels))

    mpl.rcParams['font.size'] = font_size
    mpl.rcParams['figure.figsize'] = fig_size
    mpl.rcParams['font.sans-serif'] = [font_sans]
    mpl.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width / 2, normal_data, bar_width, label=names[0], color=bar_color[0])
    rects2 = ax.bar(x + bar_width / 2, mal_data, bar_width, label=names[1], color=bar_color[1])
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    if legend_loc=='up':
        ax.legend(loc=1)
    else:
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fancybox=True, ncol=5)

    fig.tight_layout()
    plt.show()

def draw_linear_plot(x_data=None,y_data=None,data_lst=None,xlim=None,ylim=None,labels=['正常','恶意'],title='',x_label='',y_label='',font_size=13,font_sans='Arial Unicode MS',fig_size=(10, 5),legend_loc='up'):
    plt.figure(figsize=fig_size)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.rcParams['font.size'] = font_size
    plt.rcParams['font.sans-serif'] = [font_sans]
    plt.rcParams['axes.unicode_minus'] = False

    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    if x_data and y_data:
        plt.plot(x_data, y_data)

    if data_lst:
        size=max([len(f) for f in data_lst])
        for index,data in enumerate(data_lst):
            plt.plot(range(size), data, label=labels[index])

    if legend_loc=='up':
        plt.legend(loc=1)
    else:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fancybox=True, ncol=5)
    plt.show()

def draw_scatter_plot(lst,labels=['正常','恶意'], dot_size=20, dot_color=None, dot_marker=None, title='',x_label='',y_label='',font_size=13,font_sans='Arial Unicode MS',fig_size=(10, 5),legend_loc='up'):
    plt.figure(figsize=fig_size)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.rcParams['font.size'] = font_size
    plt.rcParams['font.sans-serif'] = [font_sans]
    plt.rcParams['axes.unicode_minus'] = False

    size=max([len(f) for f in lst])
    for index,data in enumerate(lst):
        plt.scatter(range(size), data, label=labels[index], s=dot_size, c=dot_color,marker=dot_marker)

    if legend_loc=='up':
        plt.legend(loc=1)
    else:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fancybox=True, ncol=5)
    plt.show()

def draw_pie_plot(data,lables,fig_size=(6, 3),font_size=8,font_sans='Arial Unicode MS',title='',legend_title=''):
    plt.rcParams['font.size'] = font_size
    plt.rcParams['font.sans-serif'] = [font_sans]
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(aspect="equal"))
    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({})".format(pct, absolute)
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),textprops=dict(color="w"))
    print(autotexts)
    ax.legend(wedges, lables,
              title=title,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=font_size, weight="bold")
    ax.set_title(legend_title)
    plt.show()

def draw_barh_plot(data,lables,x_label='', y_label='', title='',fig_size=(6, 3),font_size=8,font_sans='Arial Unicode MS',avgline=False):
    plt.rcParams['font.size'] = font_size
    plt.rcParams['font.sans-serif'] = [font_sans]
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=fig_size)
    ax.barh(lables, data)
    ax.set(xlim=None, xlabel=x_label, ylabel=y_label, title=title)
    if avgline:
        ax.axvline(calu_mean(data), ls='--', color='r')
    plt.show()

def calu_mean(lst,round_num=2):
    arr_mean = np.mean(lst)
    return round(arr_mean,round_num)

def calu_var(lst,round_num=2):
    arr_var = np.var(lst)
    return round(arr_var,round_num)

def calu_std(lst, ddof=0,round_num=2):
    arr_std = np.std(lst, ddof=ddof)
    return round(arr_std,round_num)
