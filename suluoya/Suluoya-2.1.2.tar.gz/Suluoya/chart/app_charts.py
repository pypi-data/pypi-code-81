import pandas as pd
import numpy as np
# pip install chart_studio
# http://mtw.so/65fCUd


class app_charts(object):

    def __init__(self, theme='white'):
        '''theme:solor, pearl, white
        '''
        import cufflinks as cf
        self.cf = cf
        self.cf.set_config_file(offline=True)
        self.theme = theme

    def bar(self, df=pd.DataFrame(np.random.rand(12, 4), columns=['a', 'b', 'c', 'd']),
            mode='stack',
            sort=False):
        '''mode --> group/stack/overlay
           sort --> TrueSort bars in descending order
        '''
        df.iplot(kind='bar', barmode=mode, theme=self.theme, sortbars=sort)

    def histogram(self, df=pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b'])):
        # df=self.cf.datagen.histogram(3)
        df.iplot(kind='histogram', theme=self.theme)

    def box(self, df=pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b'])):
        # df=self.cf.datagen.box(20)
        df.iplot(kind='box', theme=self.theme)

    def scatter(self, df=pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b']),
                data=None, xlabel='x', ylabel='y',
                mode='markers', size=5):
        '''mode:lines
                markers
                lines+markers
                lines+text
                markers+text
                lines+markers+text
            data=np.random.rand(100,2) --> try 1 try
        '''
        if data is None:
            df.iplot(kind='scatter',
                     mode=mode,
                     size=size, theme=self.theme)
        else:
            x = [i[0] for i in data]
            y = [i[1] for i in data]
            df = pd.DataFrame({xlabel: x, ylabel: y})
            df.iplot(x=xlabel, y=ylabel, xTitle=xlabel,
                     yTitle=ylabel, mode='markers')

    def line(self, df=pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b']),
             subplots=False,
             share_xaxis=False):
        if subplots:
            df.iplot(subplots=True, shape=(len(df.columns), 1), shared_xaxes=share_xaxis,
                     vertical_spacing=.02, fill=True, theme=self.theme)
        else:
            df.iplot(kind='line', theme=self.theme)

    def scatter3d(self, df=pd.DataFrame({'x': np.random.rand(9),
                                         'y': np.random.rand(9),
                                         'z': np.random.rand(9),
                                         'text': range(1, 10),
                                         'categories': ['c1', 'c2', 'c3', 'c1', 'c2', 'c3', 'c1', 'c2', 'c3']
                                         })
                  ):
        columns = df.columns
        df.iplot(kind='scatter3d', x=columns[0], y=columns[1], z=columns[2],
                 text=columns[3], categories=columns[4], theme=self.theme)

    # 散点矩阵图
    def scatter_matrix(self, df=pd.DataFrame(np.random.randn(100, 3), columns=['a', 'b', 'c', ])):
        df.scatter_matrix(theme=self.theme)

    def pie(self, df=pd.DataFrame([['a', 0.2], ['b', 0.5], ['c', 0.3]], columns=['class', 'weight'])):
        columns = df.columns
        df.iplot(kind='pie', labels=columns[0],
                 values=columns[1], theme=self.theme)

    def Help(self, df=pd.DataFrame()):
        help(df.iplot())


if __name__ == '__main__':
    ac = app_charts()
    ac.scatter(data=np.random.rand(10, 2))
