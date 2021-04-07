from wordcloud import WordCloud, STOPWORDS
from swissarmykit.utils.fileutils import FileUtils
import matplotlib.pyplot as plt


class TagCloud:

    def __init__(self):
        pass

    @staticmethod
    def wordcloud(text='', path=None, max_font_size=None, stop_words=None, more_stopwords=None, title='', as_dict=False, limit=-1):
        '''

        :param text:
        :param path: File path
        :param max_font_size: ex: 40
        :return:
        '''
        if path:
            text = FileUtils.load_html_file(path)

        stopwords = None
        if isinstance(stop_words, set):
            stopwords = stop_words
        elif stop_words:
            stopwords = STOPWORDS

        if more_stopwords:
            if not stopwords: stopwords = STOPWORDS
            if isinstance(more_stopwords, set):
                stopwords = stopwords.union(more_stopwords)

        print(stopwords)

        wordcloud = WordCloud(max_font_size=max_font_size, stopwords=stopwords).generate(text)
        if as_dict:
            data = {}
            count = 0
            for k, v in wordcloud.words_.items():
                count += 1
                data[k] = round(v*1000)
                if limit != -1 and count > limit:
                    break

            return data

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title)
        plt.axis("off")
        plt.show()

    @staticmethod
    def tagcloud_js_value(text, delimiter=',', limit=-1):
        if isinstance(text, str):
            text = [text]

        counts = {}
        for t in text:
            lst = [_.strip() for _ in t.split(delimiter)]
            for i in lst:
                counts[i] = counts.get(i, 0) + 1

        if limit != -1:
            sorted_x = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
            new_counts = {}
            for k in sorted_x[:limit]:
                new_counts[k[0]] = counts.get(k[0])
            return dict(sorted(new_counts.items()))

        return counts

if __name__ == '__main__':
    w = TagCloud()
    print(w.wordcloud(path='/Users/will/Desktop/code/ai_/ztest/option.html', as_dict=True))

    # lower max_font_size
    # w.word_cloud(path='C:/Users/Will/Desktop/code/ai_/ztest/artistfound.html', max_font_size=40)
    # w.plot_wordcloud(path='C:/Users/Will/Desktop/code/ai_/ztest/artistfound.html', max_font_size=40, title='test')

    # print(w.tagcloud_js_value(['Test, Test, Cloud, Genre', 'Test', 'Cloud']))


