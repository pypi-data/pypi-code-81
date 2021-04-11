import numpy as np


def find_centers(A: np.array, k: int = 1) -> np.array:
    """
    :param A: nx(d+1) data array. A=X|y
    :param k: how many centers
    :return: centers kxd
    e.g.
        from wizzi_utils import misc_tools as mt
        import matplotlib.pyplot as plt
        A = np.zeros((4, 2))  # A square with origin 0
        A[0] = [-1, -1]
        A[1] = [-1, 1]
        A[2] = [1, -1]
        A[3] = [1, 1]
        print(mt.to_str(A, title='A'))
        centers = find_centers(A, k=1)
        print(mt.to_str(centers, title='centers'))
        X, y = mt.de_augment_numpy(A)
        X_c, y_c = mt.de_augment_numpy(centers)
        plt.scatter(X, y, color='g', marker='.', label='A')
        plt.scatter(X_c, y_c, color='r', marker='.', label='k==1')
        plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5, edgecolor='black')
        plt.show()
    """
    from sklearn.cluster import KMeans
    k_means_obj = KMeans(n_clusters=k)
    k_means_obj.fit(A)
    centers = k_means_obj.cluster_centers_
    return centers


def main():
    return


if __name__ == '__main__':
    main()
