# Funciones
    

#Clases para bolsas

def getstockdata(tickers):
    
    import finviz
    import pandas as pd

    sp500 = pd.DataFrame()
    
    for ticker in tickers:
        try:
            stock = finviz.get_stock(ticker)
    
            df = pd.DataFrame.from_dict(stock, orient='index').T
            df["ticker"] = ticker
            sp500 = sp500.append(df)
        except:
            pass
    return sp500


# clustering

def SSE_elbow(df, n_clusters=20, max_iter=500, tol=1e-04, init="random", n_init=200, algorithm='auto'):
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    inertia_values = []
    for i in range(1, n_clusters+1):
        km = KMeans(n_clusters=i, max_iter=max_iter, tol=tol, init=init, n_init=n_init, random_state=1, algorithm=algorithm)
        km.fit_predict(df)
        inertia_values.append(km.inertia_)
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(range(1, n_clusters+1), inertia_values, color='red')
    plt.xlabel('No. of Clusters', fontsize=15)
    plt.ylabel('SSE / Inertia', fontsize=15)
    plt.title('SSE / Inertia vs No. Of Clusters', fontsize=15)
    plt.grid()
    plt.show()