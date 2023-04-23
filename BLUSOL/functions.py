import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator

def numerize(df):
    col_list = list(df.columns)
    df = df.copy()
    for column in col_list:
        if df[column].dtype in ['int64','float64','bool']:
            continue
        elif df[column].dtype == '<M8[ns]':
            del(df[column])
        else:
            vals = list(df[column].unique())
            mapa = {vals[i]:i for i in range(len(vals))}
            df[column] = df[column].apply(lambda x: mapa[x]).astype('int64')
    return df

def numerize_dummie(df):
    col_list = list(df.columns)
    df = df.copy()
    for column in col_list:
        if df[column].dtype in ['int64','float64','bool']:
            continue
        elif df[column].dtype == '<M8[ns]':
            del(df[column])
        else:
            df = pd.concat([df.drop(column,axis = 1),pd.get_dummies(df[column])],axis = 1)
    return df

def preprocess(df):
    """Preprocess data for KMeans clustering"""
    df_log = np.log1p(df)
    scaler = StandardScaler()
    scaler.fit(df_log)
    df_norm = scaler.transform(df_log)
    return pd.DataFrame(df_norm,columns = df.columns)

def elbow_plot(df,max_k):
    """Create elbow plot from normalized data"""
    
    sse = {}
    
    for k in range(1, max_k):
        kmeans = KMeans(n_clusters=k, random_state=1)
        kmeans.fit(df)
        sse[k] = kmeans.inertia_
        print('k:',k,end = '\r')
    
    plt.title('Elbow plot for K selection')
    plt.xlabel('k')
    plt.ylabel('SSE')
    sns.pointplot(x=list(sse.keys()),
                 y=list(sse.values()))
    plt.show()

def find_k(df, max_k, increment=0, decrement=0):
    """Find the optimum k clusters"""
    
    sse = {}
    
    for k in range(1, max_k):
        kmeans = KMeans(n_clusters=k, random_state=1)
        kmeans.fit(df.values)
        sse[k] = kmeans.inertia_
        print('k:',k,end = '\r')
    
    kn = KneeLocator(x=list(sse.keys()), 
                 y=list(sse.values()), 
                 curve='convex', 
                 direction='decreasing')
    k = kn.knee + increment - decrement
    return k