import pandas as pd
import string
import numpy as np
import pkg_resources
import seaborn as sns
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class wording:
    
    def __init__(self):
        self.df_lema = self.load_lema()
        self.df_stopwords = self.load_stopwords()
        self.tfidf = pd.DataFrame()
        self.positive_words = self.load_positive_words()
        self.negative_words = self.load_negative_words()
        
    def load_file(self, file='none', type='txt', header=False, sep=',', column='None'):
        if file == 'none':
            raise ValueError('No Filename was provided, need one')
        
        if type == 'excel':
            df = pd.read_excel(file)
            if column != 'None':
                df = df[column]
                df.rename(column={column: 'word'}, inplace=True)
            else:
                raise TypeError("An xlsx file column was not selected")

        if type == 'csv':
            if header:
                header=0
            else:
                header=None
            df = pd.read_csv(file, header=header, sep=sep)
            if column != 'None':
                df = pd.DataFrame({'word': df[column]})
            else:
                raise TypeError("An csv file column was not selected")
           
        if type == 'txt':
            f = open(file, "r")
            df = f.read()
            df = pd.DataFrame(df.split('\n'))
            df.columns = ['word']
        self.colection = df.copy()
        
    def load_lema(self):
        resource_package = __name__
        file = '/'.join(('config', 'lematizer.csv'))
        file_path = pkg_resources.resource_filename(resource_package, file)
        df_lema = pd.read_csv(file_path, sep=',')
        df_lema.columns = ['word','lema']
        return(df_lema)

    def load_positive_words(self):
        resource_package = __name__
        file = '/'.join(('config', 'positive.csv'))
        file_path = pkg_resources.resource_filename(resource_package, file)
        df_pw = pd.read_csv(file_path)
        df_pw.columns = ['word']
        return(df_pw)

    def load_negative_words(self):
        resource_package = __name__
        file = '/'.join(('config', 'negative.csv'))
        file_path = pkg_resources.resource_filename(resource_package, file)
        df_pw = pd.read_csv(file_path)
        df_pw.columns = ['word']
        return(df_pw)
    
    def load_stopwords(self):
        resource_package = __name__
        file = '/'.join(('config', 'stopwords.csv'))
        file_path = pkg_resources.resource_filename(resource_package, file)
        df_sw = pd.read_csv(file_path, sep=';', header=None)
        df_sw.columns = ['stopword']
        return(df_sw)
    
    def del_stopwords(self, text, stopwords=True):
        output = list()
        text = self.del_punck(text)
        text = text.lower()
        for word in text.split(' '):
            if stopwords:
                if len(word) > 3:
                    result = ''.join([str(x) for x in self.df_stopwords[self.df_stopwords['stopword'] == word]['stopword']])
                    if len(result) == 0:
                        output.append(word)
            else:
                output.append(word)
        return(output)
    
    def del_punck(self, text):
        punck = ",.;/<>:?[]{}+_)(*&$#@!)1234567890\n\t\r"
        for c in punck:
            text = text.replace(c,'')
        text = text.replace('&quot', '')
        return(text)
    
    def get_lema(self, text, lemmatizer=True):
        output = list()
        for word in text:
            if lemmatizer:
                w_lema = ''.join(self.df_lema[self.df_lema['lema'] == word]['word'].unique())
                if len(w_lema) == 0:
                    output.append(word)
                else:
                    output.append(w_lema)
            else:
                output.append(word)
        return(output)
    
    def build_tf(self, df, stopwords=True, lemmatizer=True):
        frame_tfidf = pd.DataFrame()
        for i in range(df.shape[0]):
            frame_aux = pd.DataFrame()
            line = ''.join(df.loc[i])
            text = self.del_stopwords(line, stopwords=stopwords)
            text = self.get_lema(text, lemmatizer=lemmatizer)
            frame_aux['word'] = text
            frame_aux['doc'] = 'doc-' + str(i)
            frame_tfidf = frame_tfidf.append(frame_aux)
        frame_tfidf['count'] = 1
        return(frame_tfidf[['doc','word','count']])    

    def build_tf_idf(self, stopwords=True, lemmatizer=True):
        df = self.colection.copy()
        f = self.build_tf(df, stopwords=stopwords, lemmatizer=lemmatizer)
        n = df.shape[0]
        f = f.groupby(by=['doc','word']).count().reset_index()
        f.rename(columns={'count':'f'},inplace=True)
        f['tf'] = np.log2(f['f'])
        f['idf'] = 0    
        idf = f.groupby(by=['word']).count().reset_index()[['word','tf']]
        idf.rename(columns={'tf':'idf'}, inplace=True)    
        idf['log'] = np.log2(1+ (n/idf['idf']))
        for i in range(f.shape[0]):
            w = ''.join(f.loc[i:i,'word'])
            f.loc[i:i,'idf'] = float(idf[idf['word'] == w]['log'])    
        f['tf_idf'] = f['tf'] * f['idf']
        self.tfidf = f.copy()
        self.set_sign()

    def set_sign(self):
        self.tfidf['sign'] = ''
        for i in range(self.tfidf.shape[0]):
            word = self.tfidf.loc[i,'word']
            p = self.positive_words[self.positive_words['word'] == word]
            n = self.negative_words[self.negative_words['word'] == word]
            if len(p) == 0 and len(n) > 0:
                self.tfidf.loc[i,'sign'] = 'negative'
            elif len(p) == 0 and len(n) == 0:
                self.tfidf.loc[i,'sign'] = 'neutral'
            elif len(p) > 0 and len(n) == 0:
                self.tfidf.loc[i,'sign'] = 'positive'
            elif len(p) > 0 and len(n) > 0:
                self.tfidf.loc[i,'sign'] = 'ambiguous'  
                
    def sentimental_graf(self):
        bar = pd.DataFrame(self.tfidf['sign'].value_counts()).reset_index()
        bar.columns = ['Sentimental','frequency']
        sns.barplot(x='Sentimental', y='frequency', data=bar)
    
    def word_cloud(self, picture='none'):
        resource_package = __name__
        file = '/'.join(('config', 'cloud.jpeg'))
        file_path = pkg_resources.resource_filename(resource_package, file)
        if picture == 'none':
            mask = np.array(Image.open(file_path))
        else:
            mask = np.array(Image.open(picture))
        tuples = [tuple(x) for x in self.tfidf[['word','tf_idf']].values]
        wc = WordCloud(background_color="white", max_words=1000, mask=mask).generate_from_frequencies(frequencies=dict(tuples))
        plt.figure(figsize=(15,15))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()        
        
    def look2word(self, word):
        return(self.colection[self.colection['word'].str.contains(word)])
        
