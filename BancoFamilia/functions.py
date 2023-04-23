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

periodos1 = [x.lower() for x in ['Tempo Atividade Não Informado','Menos de 6 meses','De 6 meses a 1 ano','De 1 a 2 anos','De 2 a 3 anos','De 3 a 4 anos','De 4 a 6 anos','De 6 a 8 anos','De 8 a 10 anos','Acima de 10 anos']]
mapa1 = {periodos1[i]:i for i in range(len(periodos1))}
periodos2 = [x.lower() for x in ['Tempo Ramo Atividade Não Informado','Menos de 6 meses','De 6 meses a 1 ano','Até 1 Ano','De 1 a 2 anos','De 2 a 4 anos','De 4 a 6 anos','De 6 a 8 anos','De 8 a 10 anos','Acima de 10 anos']]
mapa2 = {periodos2[i]:i for i in range(len(periodos2))}
periodos3 = [x.lower() for x in ['Tempo Residência Não Informado','Menos de 6 meses','De 6 meses a 1 ano','De 1 a 2 anos','De 2 a 3 anos','De 3 a 4 anos','De 4 a 6 anos','De 6 a 8 anos','De 8 a 10 anos','Acima de 10 anos']]
mapa3 = {periodos3[i]:i for i in range(len(periodos3))}

def numerize_periodos1(serie):
    return serie.apply(lambda x: mapa1[x.lower()]).astype('int64')
def numerize_periodos2(serie):
    return serie.apply(lambda x: mapa2[x.lower()]).astype('int64')
def numerize_periodos3(serie):
    return serie.apply(lambda x: mapa3[x.lower()]).astype('int64')

def numerize(df):
    col_list = list(df.columns)
    df = df.copy()
    for column in col_list:
        if df[column].dtype in ['int64','float64','bool']:
            continue
        elif df[column].dtype == '<M8[ns]':
            del(df[column])
        elif column == 'tempo_atividade':
            df[column] = numerize_periodos1(df[column])
        elif column == 'tempo_atuacao_ramo_atividade':
            df[column] = numerize_periodos2(df[column])
        elif column == 'tempo_de_residancia__anos':
            df[column] = numerize_periodos3(df[column])
        else:
            vals = list(df[column].cat.categories)
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
        elif column == 'tempo_atividade':
            df[column] = numerize_periodos1(df[column])
        elif column == 'tempo_atuacao_ramo_atividade':
            df[column] = numerize_periodos2(df[column])
        elif column == 'tempo_de_residancia__anos':
            df[column] = numerize_periodos3(df[column])
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