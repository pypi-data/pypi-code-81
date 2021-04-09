import pandas as pd
import matplotlib.pyplot as plt


class SlyModel(object):
    def __init__(self, x=None, y=None, text_size=0.2):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        self.accuracy_score = accuracy_score
        self.text_size = text_size
        if x is None and y is None:
            from sklearn import datasets
            self.digits = datasets.load_digits()
            self.x = pd.DataFrame(self.digits.data)
            self.y = self.digits.target
        else:
            self.x = x
            self.y = y

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=self.text_size, random_state=111)

    def KNC(self,):
        from sklearn.neighbors import KNeighborsClassifier
        best_score = 0
        best_k = -1  # 超参数
        # 网格搜索
        k_range = range(1, len(self.x.keys()))
        acc_scores = []
        for k in k_range:
            KNN = KNeighborsClassifier(n_neighbors=k)
            KNN.fit(self.x_train, self.y_train)
            score = KNN.score(self.x_test, self.y_test)
            acc_scores.append(score)
            if score > best_score:
                best_k = k
                best_score = score
        y_predict = KNN.predict(self.x_test)
        accurate_score = self.accuracy_score(self.y_test, y_predict)
        plt.figure()
        plt.rcParams["figure.figsize"] = (15.0, 8.0)
        plt.xlabel("k")
        plt.ylabel("accuracy")
        plt.plot(k_range, acc_scores, marker="o")
        plt.xticks(range(0, len(self.x.keys())+1,
                        round(len(self.x.keys())/10)+1))
        plt.show()
        return {'predict': pd.Series(list(y_predict)), 'accurate_score': accurate_score, 'best_k': best_k, 'best_score': best_score}

    def LR(self):
        from sklearn.linear_model import LinearRegression
        linear_reg = LinearRegression()
        linear_reg.fit(self.x_train, self.y_train)
        coef = linear_reg.coef_
        intercept = linear_reg.intercept_
        R2 = linear_reg.score(self.x_test, self.y_test)
        predict = linear_reg.predict(self.x_train)
        return{'coef': coef, 'intercept': intercept, 'R2': R2, 'predict': predict}

    def LGR(self):
        from sklearn.linear_model import LogisticRegression
        lr_model = LogisticRegression()
        lr_model.fit(self.x_train, self.y_train)
        coef = lr_model.coef_
        intercept = lr_model.intercept_
        R2 = lr_model.score(self.x_test, self.y_test)
        predict = lr_model.predict(self.x_train)
        return{'coef': coef, 'intercept': intercept, 'R2': R2, 'predict': predict}

    def DTC(self, max_depth=2, min_samples_split=10):
        from sklearn.tree import DecisionTreeClassifier
        dt_clf = DecisionTreeClassifier(max_depth=max_depth,
                                        min_samples_split=min_samples_split
                                        )
        dt_clf.fit(self.x_train, self.y_train)
        score = dt_clf.score(self.x_test, self.y_test)
        return score
