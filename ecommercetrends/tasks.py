# Create your tasks here
from __future__ import absolute_import, unicode_literals

import pandas as pd
import nltk
from sklearn.cluster import KMeans
from celery import shared_task, current_task

from ecommercetrends.models import SepatuPria


@shared_task
def totalulasan(k, katmodel, katmodel2):

    dataset = None

    current_task.update_state(state='PROGRESS', meta={'status': 'Get Data From Database'})

    if katmodel == 'Sepatu Pria':
        if katmodel2 == '':
            dataset = pd.DataFrame(list(SepatuPria.objects.values('produk', 'tanggal')))

    dataset = dataset.rename(index=str, columns={"produk": "nama", "tanggal": "tanggal"})

    current_task.update_state(state='PROGRESS', meta={'status': 'Bag of Word'})

    # 0 tokenize
    nama_token = []
    for x, y in enumerate(dataset['nama']):
        nama_token.append(dataset['nama'][x].split())

    # 1 bag of word
    listword = []
    for x, y in enumerate(dataset['nama']):
        tokens = nltk.word_tokenize(dataset['nama'][x])
        listword += tokens

    worddict = dict.fromkeys(listword, 0)

    # 2 create data with 0 value same with sum of data
    word_token = []
    for x in dataset['nama']:
        word_token.append(dict.fromkeys(worddict, 0))

    # 3 add = 1 for word same in nama_token
    for x, y in enumerate(nama_token):
        for word in nama_token[x]:
            word_token[x][word] += 1

    # 4 running tf from data before
    tf = []
    for x, y in enumerate(word_token):
        tf.append(word_token[x].values())

    # data feature extraction save as dataframe
    readyclustering = pd.DataFrame(data=tf)

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering'})

    kmeans = KMeans(n_clusters=k, max_iter=200).fit(readyclustering)
    clusters = kmeans.fit_predict(readyclustering)

    hasilcluster = []
    for i in clusters:
        hasilcluster.append(i)

    data = dataset
    data['Assignment'] = hasilcluster

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering with K-Means Finished'})

    data = data.sort_values(by=['Assignment'])
    data = data.reset_index(drop=True)

    current_task.update_state(state='PROGRESS', meta={'status': 'Finding Total Produk'})

    # Menjumlah tiap assignment
    a = 0
    jumlah = [1]
    assignment = data['Assignment'][0]
    for i, j in enumerate(data['Assignment']):
        if i != 0:
            if data['Assignment'][i] == assignment:
                jumlah[a] += 1
            else:
                a += 1
                jumlah.append(1)
                assignment = data['Assignment'][i]

    # Mencari nama produk
    nama_token = []
    listword = []
    produk = []
    assignment = data['Assignment'][0]
    for i, j in enumerate(data['Assignment']):
        nama_token.append(data['nama'][i].split())
        tokens = nltk.word_tokenize(data['nama'][i])
        listword += tokens

        if i != len(data['Assignment']) - 1 and data['Assignment'][i + 1] != data['Assignment'][i]:
            worddict = dict.fromkeys(listword, 0)
            for z, y in enumerate(nama_token):
                for word in nama_token[z]:
                    worddict[word] += 1
            maxv = max(worddict.values())
            produk.append([k for k, v in worddict.items() if v == maxv])

            listword.clear()
            nama_token.clear()
        elif i == len(data['Assignment']) - 1:
            worddict = dict.fromkeys(listword, 0)
            for z, y in enumerate(nama_token):
                for word in nama_token[z]:
                    worddict[word] += 1
            maxv = max(worddict.values())
            produk.append([k for k, v in worddict.items() if v == maxv])

            listword.clear()
            nama_token.clear()

    for i, j in enumerate(produk):
        if not isinstance(produk[i], str):
            produk[i] = ' '.join(produk[i])
    # convert to dataframe and sort
    produkfix = pd.DataFrame({'Produk': produk, 'Jumlah': jumlah})
    produkfix = produkfix.reset_index(drop=True)

    totalulasan = produkfix.sort_values(by=['Jumlah'], ascending=False)
    totalulasan = totalulasan.reset_index(drop=True)
    return totalulasan.to_json(orient='records')
