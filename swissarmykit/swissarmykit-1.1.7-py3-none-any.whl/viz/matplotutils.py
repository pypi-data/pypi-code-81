import matplotlib.pyplot as plt

class MatplotUtils:

    def __init__(self, style='ggplot'):
        plt.style.use(style)

    @staticmethod
    def matshow(mat, title='matrix show', x='X-axis', y='Y-axis', axis_off=False):
        plt.matshow(mat)
        plt.colorbar()

        if axis_off:
            plt.axis('off')

        plt.title(title)
        plt.xlabel(y)
        plt.ylabel(x)
        plt.show()

    @staticmethod
    def imshow(im, title='Image info', **kwargs):
        plt.title(title)
        plt.imshow(im, **kwargs)
        plt.show()

    def scatter_plot(self, x, y, size=10, x_label='x', y_label='y', color='b'):
        plt.scatter(x, y, s=size, color=color)
        self.set_labels(x_label, y_label)

    def plot(self, x, y, x_label='x', y_label='y', color='r'):
        plt.plot(x, y, color=color)
        self.set_labels(x_label, y_label)

    def ploty(self, y, x_label='x', y_label='y'):
        plt.plot(y)
        self.set_labels(x_label, y_label)

    def set_labels(self, x_label, y_label):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    @staticmethod
    def print_available_style():
        print(plt.style.available)

    @staticmethod
    def use_ggplot():
        plt.style.use('ggplot')

    def __str__(self):
        return 'Math Plot Utils'