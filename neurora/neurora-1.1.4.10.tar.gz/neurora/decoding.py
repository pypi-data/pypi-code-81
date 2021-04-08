# -*- coding: utf-8 -*-

' a module for classification-based neural decoding '

__author__ = 'Zitong Lu'

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

np.seterr(divide='ignore', invalid='ignore')


' a function for time-by-time decoding for EEG-like data '

def decoding(data, labels, n=2, navg=5, time_win=5, time_step=5, iter=10, test_size=0.3, smooth=True, p=0.05, cbpt=True, plotrlt=True):

    """
    Conduct time-by-time decoding for EEG-like data

    Parameters
    ----------
    data : array
        The neural data.
        The shape of data must be [n_subs, n_trials, n_chls, n_ts]. n_subs, n_trials, n_chls and n_ts represent the
        number of subjects, the number of trails, the number of channels and the number of time-points.
    labels : array
        The labels of each trials.
        The shape of labels must be [n_subs, n_trials]. n_subs and n_trials represent the number of subjects and the
        number of trials.
    n : int. Default is 2.
        The number of categories for classification.
    navg : int. Default is 5.
        The number of trials used to average.
    time_win : int. Default is 5.
        Set a time-window for decoding for different time-points.
        If time_win=5, that means each decoding process based on 5 time-points.
    time_step : int. Default is 5.
        The time step size for each time of decoding.
    iter : int. Default is 10.
        The times for iteration.
    test_size : float. Default is 0.3.
        The proportion of the test set.
        test_size should be between 0.0 and 1.0.
    smooth : boolean True or False. Default is True.
        Smooth the decoding result or not.
    p : float. Default is 1.
        The threshold of p-values.
    cbpt : boolean True or False. Default is True.
        Conduct cluster-based permutation test or not.
    plotrlt : bool True or False.
        Plot the RSA result automatically or not.

    Returns
    -------
    accuracies : array
        The time-by-time decoding accuracies.
        The shape of accuracies is [n_subs, int((n_ts-time_win)/time_step)+1].
    """

    if np.shape(data)[0] != np.shape(labels)[0]:

        return "Invalid input!"

    nsubs, ntrials, nchls, nts = np.shape(data)

    ncategories = np.zeros([nsubs], dtype=int)

    labels = np.array(labels)

    for sub in range(nsubs):

        sublabels_set = set(labels[sub].tolist())
        ncategories[sub] = len(sublabels_set)

    if len(set(ncategories.tolist())) != 1:

        return "Invalid input!"

    if n != ncategories[0]:

        return "Invalid input!"

    categories = list(sublabels_set)

    newnts = int((nts-time_win)/time_step)+1

    avgt_data = np.zeros([nsubs, ntrials, nchls, newnts])

    for t in range(avgt_data):

        avgt_data[:, :, :, t] = np.average(data[:, :, :, t*time_step:t*time_step+time_win], axis=3)

    acc = np.zeros([nsubs, newnts])

    for sub in range(nsubs):

        ns = np.zeros([n], dtype=int)

        for i in range(ntrials):
            for j in range(n):
                if labels[sub, i] == categories[j]:
                    ns[j] = ns[j] + 1

        minn = int(np.min(ns)/navg)

        subacc = np.zeros([iter, newnts])

        for i in range(iter):

            datai = np.zeros([n, minn*navg, nchls, newnts])
            labelsi = np.zeros([n, minn], dtype=int)


            for j in range(n):
                labelsi[j] = j

            randomindex = np.random.permutation(np.array(range(ntrials)))

            m = np.zeros([n], dtype=int)

            for j in range(ntrials):
                for k in range(n):

                    if labels[sub, randomindex[j]] == categories[k] and m[k] < minn*navg:
                        datai[k, m[k]] = avgt_data[sub, randomindex[j]]
                        m[k] = m[k] + 1

            avg_datai = np.zeros([n, minn, nchls, nts])

            for j in range(minn):

                avg_datai[:, j] = np.average(datai[:, minn*navg:minn*navg+navg], axis=1)

            x = np.reshape(avg_datai, [n*minn, nchls, nts])
            y = np.reshape(n*minn)

            for t in range(nts):

                state = np.random.randint(0, 100)
                xt = x[:, :, t]
                x_train, x_test, y_train, y_test = train_test_split(xt, y, test_size=test_size, random_state=state)
                svm = SVC(kernel='linear')
                svm.fit(x_train, y_train)
                subacc[i, t] = svm.score(x_test, y_test)

        acc[sub] = np.average(subacc, axis=0)

    return acc


' a function for cross-temporal decoding for EEG-like data '

def crosstemporal_decoding(data, labels, n=2, navg=5, time_win=5, time_step=5, iter=10, test_size=0.3, smooth=True,
                           p=0.05, cbpt=True, plotrlt=True):

    """
    Conduct time-by-time decoding for EEG-like data

    Parameters
    ----------
    data : array
        The neural data.
        The shape of data must be [n_subs, n_trials, n_chls, n_ts]. n_subs, n_trials, n_chls and n_ts represent the
        number of subjects, the number of trails, the number of channels and the number of time-points.
    labels : array
        The labels of each trials.
        The shape of labels must be [n_subs, n_trials]. n_subs and n_trials represent the number of subjects and the
        number of trials.
    n : int. Default is 2.
        The number of categories for classification.
    navg : int. Default is 5.
        The number of trials used to average.
    time_win : int. Default is 5.
        Set a time-window for decoding for different time-points.
        If time_win=5, that means each decoding process based on 5 time-points.
    time_step : int. Default is 5.
        The time step size for each time of decoding.
    iter : int. Default is 10.
        The times for iteration.
    test_size : float. Default is 0.3.
        The proportion of the test set.
        test_size should be between 0.0 and 1.0.
    smooth : boolean True or False. Default is True.
        Smooth the decoding result or not.
    p : float. Default is 1.
        The threshold of p-values.
    cbpt : boolean True or False. Default is True.
        Conduct cluster-based permutation test or not.
    plotrlt : bool True or False.
        Plot the RSA result automatically or not.

    Returns
    -------
    accuracies : array
        The cross-temporal decoding accuracies.
        The shape of accuracies is [n_subs, int((n_ts-time_win)/time_step)+1].
    """

    if np.shape(data)[0] != np.shape(labels)[0]:

        return "Invalid input!"

    nsubs, ntrials, nchls, nts = np.shape(data)

    ncategories = np.zeros([nsubs], dtype=int)

    labels = np.array(labels)

    for sub in range(nsubs):

        sublabels_set = set(labels[sub].tolist())
        ncategories[sub] = len(sublabels_set)

    if len(set(ncategories.tolist())) != 1:

        return "Invalid input!"

    if n != ncategories[0]:

        return "Invalid input!"

    categories = list(sublabels_set)

    newnts = int((nts-time_win)/time_step)+1

    avgt_data = np.zeros([nsubs, ntrials, nchls, newnts])

    for t in range(avgt_data):

        avgt_data[:, :, :, t] = np.average(data[:, :, :, t*time_step:t*time_step+time_win], axis=3)

    acc = np.zeros([nsubs, newnts, newnts])

    for sub in range(nsubs):

        ns = np.zeros([n], dtype=int)

        for i in range(ntrials):
            for j in range(n):
                if labels[sub, i] == categories[j]:
                    ns[j] = ns[j] + 1

        minn = int(np.min(ns)/navg)

        subacc = np.zeros([iter, newnts, newnts])

        for i in range(iter):

            datai = np.zeros([n, minn*navg, nchls, newnts])
            labelsi = np.zeros([n, minn], dtype=int)


            for j in range(n):
                labelsi[j] = j

            randomindex = np.random.permutation(np.array(range(ntrials)))

            m = np.zeros([n], dtype=int)

            for j in range(ntrials):
                for k in range(n):

                    if labels[sub, randomindex[j]] == categories[k] and m[k] < minn*navg:
                        datai[k, m[k]] = avgt_data[sub, randomindex[j]]
                        m[k] = m[k] + 1

            avg_datai = np.zeros([n, minn, nchls, nts])

            for j in range(minn):

                avg_datai[:, j] = np.average(datai[:, minn*navg:minn*navg+navg], axis=1)

            x = np.reshape(avg_datai, [n*minn, nchls, nts])
            y = np.reshape(n*minn)

            for t in range(nts):

                state = np.random.randint(0, 100)
                xt = x[:, :, t]
                x_train, x_test, y_train, y_test = train_test_split(xt, y, test_size=test_size, random_state=state)
                svm = SVC(kernel='linear')
                svm.fit(x_train, y_train)
                subacc[i, t, t] = svm.score(x_test, y_test)
                for tt in range(nts - 1):
                    if tt < t:
                        xtt = x[:, :, tt]
                        x_train, x_testt, y_train, y_test = train_test_split(xtt, labels, test_size=test_size,
                                                                             random_state=state)
                        subacc[i, t, tt] = svm.score(x_testt, y_test)
                    if tt >= t:
                        xtt = x[:, :, tt + 1]
                        x_train, x_testt, y_train, y_test = train_test_split(xtt, labels, test_size=test_size,
                                                                             random_state=state)
                        subacc[i, t, tt + 1] = svm.score(x_testt, y_test)

        acc[sub] = np.average(subacc, axis=0)

    return acc


def unidirectional_transfer_decoding(data1, labels1, data2, labels2, navg=5, time_win=5, time_step=5, cbpt=True):

    """
    Conduct time-by-time decoding for EEG-like data

    Parameters
    ----------
    data : array
        The neural data.
        The shape of data must be [n_subs, n_chls, n_ts]. n_subs, n_chls, n_ts represent the number of subjects, the
        number of channels and the number of time-points.

    Returns
    -------
    accuracies : array
        The time-by-time decoding accuracies.
    """

def bidirectional_transfer_decoding(data1, labels1, data2, labels2, navg=5, time_win=5, time_step=5, cbpt=True):

    """
    Conduct time-by-time decoding for EEG-like data

    Parameters
    ----------
    data : array
        The neural data.
        The shape of data must be [n_subs, n_chls, n_ts]. n_subs, n_chls, n_ts represent the number of subjects, the
        number of channels and the number of time-points.

    Returns
    -------
    accuracies : array
        The time-by-time decoding accuracies.
    """



#data = np.random.rand(1, 5, 1, 1)
#labels = [[1, 2, 1, 1, 3]]
#decoding(data, labels, n=3, navg=1)

