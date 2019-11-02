#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


nomeDoDocumento = "teste gympass.txt"


# In[3]:


def CreateDataFrame(nomeArquivo):
    file = open(nomeArquivo, "r") 
    data = []
    for line in file: 
        data.append(line)
    df = pd.DataFrame(columns=["Hora", 'PilotoID', 'Piloto_Name', 'N_volta', 'time_volta', 'Vm'])
    for i in range(len(data)):
        df.loc[i] = data[i].replace('\t',' ').replace('â€“',' ').split()
    return df


# In[4]:


def convertTimeVolta(time):
    a = float(time.split(':')[0])
    b = float(time.split(':')[1])
    return (a*60+b)


# In[5]:


def Convert_DF_Types(df):
    df["Hora"] = pd.to_datetime(df['Hora'])
    df["time_volta"] = df["time_volta"].apply(convertTimeVolta)
    df["Vm"] = df["Vm"].apply(lambda x: float(x.replace(",", ".")))
    df["PilotoID"] = df["PilotoID"].apply(int)
    df["N_volta"] = df["N_volta"].apply(int)
    return df


# In[6]:


def vencedorPrint(df):
    indexWinner = df[df["Hora"]==df[df["N_volta"]==4]["Hora"].min()].index
    #print(indexWinner)
    if indexWinner.size:
        idWinner = df.iloc[indexWinner]['PilotoID'].values[0]
        nameWinner = df.iloc[indexWinner]['Piloto_Name'].values[0]
        tempoWinner = df[df.PilotoID==idWinner]["time_volta"].sum()
        print ("O pilito vencedor e' o {} e seu ID e' {}".format(nameWinner, idWinner))
        print ("O piloto vencedor completou 4 voltas em {} segundos".format(tempoWinner))
    else:
        print("Ninguem completou 4 voltas necessarias para finalizar a corrida")
    return indexWinner


# In[7]:


def TempoAcumulado(df):
    #Vamos criar uma coluna com o tempo acumulado
    tempo_acul = []
    for i in range(len(df)):
        tempo_acul.append(sum(df[(df['N_volta']<= df.iloc[i]['N_volta']) & (df["PilotoID"]==df.iloc[i]["PilotoID"])]['time_volta']))
    df["tempo_acumulado"] = tempo_acul
    return df


# In[8]:


#para a classificacao geral vamos analisar qual distancia percorreu cada piloto no momento do termino da corrida
def CalcularPosicoes(df, comprimentoDaVolta):
    #Agora vamos filtar a tabela pelo tempo total acumulado do primeiro lugar, que representa o termino da prova,
    #pegando apenas as linhas com tempo acumulado maior que o tempo da prova
    #Em seguida vamos restringir para a primeira volta completada do piloto apos o termino, para calcular, atraves da velocidade
    #media a distancia percorrida ate o momento de termino da prova
    indexWinner = df[df["Hora"]==df[df["N_volta"]==4]["Hora"].min()].index
    tempo_acul_Winner = df.iloc[indexWinner]['tempo_acumulado'].values[0]
    dfPosTermino = df[(df["tempo_acumulado"] > tempo_acul_Winner)]
    dfPosTermino = dfPosTermino.sort_values(by= 'tempo_acumulado').drop_duplicates(subset='PilotoID', keep='first')
    dist_pre_termino = []
    for i in range(len(dfPosTermino)):
        dist_pre_termino.append((tempo_acul_Winner - (dfPosTermino.iloc[i]['tempo_acumulado'] -  dfPosTermino.iloc[i]['time_volta'])) * dfPosTermino.iloc[i]['Vm'] + (dfPosTermino.iloc[i]['N_volta']-1) * comprimentoDaVolta)
    dfPosTermino['Dist_Pre_Termino'] = dist_pre_termino
    dfPosTermino = dfPosTermino.sort_values(by='Dist_Pre_Termino', ascending=False)
    return dfPosTermino


# In[9]:


df = CreateDataFrame(nomeDoDocumento)


# In[10]:


df = Convert_DF_Types(df)


# In[11]:


#definindo a distancia da volta como a media do produto da velocidade media com o tempo da volta 
distancia_da_volta = df["time_volta"].mean() * df["Vm"].mean()


# In[12]:


index = vencedorPrint(df)


# In[13]:


df = TempoAcumulado(df)


# In[14]:


df2 = CalcularPosicoes(df, distancia_da_volta)


# In[15]:


#Print da classificacao


# In[16]:


for i in range(len(df2)):
    print('O pilotou que ficou na posicao {} foi o {}, que possui o ID {}, que completou {} voltas no tempo de prova que foi {}'.format(i+2, df2.iloc[i]['Piloto_Name'], df2.iloc[i]['PilotoID'], df2.iloc[i]['N_volta']-1,df.iloc[index]['tempo_acumulado'].values[0]))


# In[17]:


#BONUS


# In[18]:


#Melhor volta Individual


# In[19]:

print("A melhor volta individual de cada piloto foi:")
print(df.groupby("Piloto_Name")['time_volta'].min())


# In[20]:


#Melhor volta corrida


# In[21]:


print("A melhor volta da corrida foi do piloto {} e durou {} segundos".format(df[df["time_volta"]==df["time_volta"].min()]["Piloto_Name"].values[0],df["time_volta"].min()))


# In[22]:


#Velocidade Media dos pilotos considerando as voltas completadas apos o termino da corrida


# In[23]:

print("A velocidade media dos pilotos foi:")
print(df.groupby("Piloto_Name")['Vm'].mean())


# In[24]:


#Quanto tempo os outros pilotos chegaram apos o vencedor


# In[25]:


for i in range(len(df2)):    
    if (df2.iloc[i]["N_volta"] == 4):
        print("O piloto {} chegou {} segundos apos o primeiro colocado".format(df2.iloc[i]['Piloto_Name'], round(df2.iloc[i]['tempo_acumulado'] - df.iloc[index]['tempo_acumulado'].values[0], 2)))
    else:
        print("O piloto {} nao completou 4 voltas na corrida".format(df2.iloc[i]['Piloto_Name']))


# In[ ]:




