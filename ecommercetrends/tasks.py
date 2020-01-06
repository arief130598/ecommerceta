# Create your tasks here
from __future__ import absolute_import, unicode_literals
from ecommercetrends.models import Ulasan, Produk, Toko

import json
import time
import pandas as pd
import nltk
from django.db.models import Q
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import re

from celery import shared_task, current_task

# Library for debugging celery
from celery import current_app

current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


def jumlahulasan(datajumlah):
    tempnama = datajumlah['nama'][0]
    tempjumlah = 0
    jumlah = []
    nama = []
    for j, i in enumerate(datajumlah['nama']):
        if i == tempnama:
            tempjumlah = tempjumlah + 1
        else:
            jumlah.append(tempjumlah)
            nama.append(tempnama)
            tempjumlah = 1
            tempnama = i

        if (datajumlah.__len__() - 1) == j:
            jumlah.append(tempjumlah)
            nama.append(tempnama)

    produk = pd.DataFrame({'Produk': nama, 'Jumlah': jumlah})
    return produk


def sortdata(data):
    data = data.sort_values(by=['Jumlah'], ascending=False)
    data = data.reset_index(drop=True)
    return data


def produktinggi(data):
    produktinggidata = data.loc[data['Jumlah'].astype('float64').idxmax()]
    produktinggidata = {
        'jumlah': int(produktinggidata['Jumlah']),
        'nama': produktinggidata['Produk']
    }
    produktinggidata = json.dumps(produktinggidata)
    return produktinggidata


def produkrendah(data):
    produkrendahdata = data.loc[data['Jumlah'].astype('float64').idxmin()]
    produkrendahdata = {
        'jumlah': int(produkrendahdata['Jumlah']),
        'nama': produkrendahdata['Produk']
    }
    produkrendahdata = json.dumps(produkrendahdata)
    return produkrendahdata


def tanggaltinggi(data):
    tanggaltinggi = data.loc[data['value'].idxmax()]
    tanggaltinggi = {
        'value': int(tanggaltinggi['value']),
        'tanggal': tanggaltinggi['tanggal']
    }
    tanggaltinggi = json.dumps(tanggaltinggi)
    return tanggaltinggi


def tanggalrendah(data):
    tanggalrendah = data.loc[data['value'].idxmin()]
    tanggalrendah = {
        'value': int(tanggalrendah['value']),
        'tanggal': tanggalrendah['tanggal']
    }
    tanggalrendah = json.dumps(tanggalrendah)
    return tanggalrendah


def movingaverage(data, n):
    movingaveragedata = []
    for k, l in enumerate(data['value']):
        if k >= n - 1:
            tempaverage = 0
            for o in range(0, n):
                tempaverage += data['value'][k - o]
            tempaverage = tempaverage / n
            movingaveragedata.append(tempaverage)
        else:
            movingaveragedata.append(0)
    ma = pd.DataFrame(movingaveragedata, columns=['value'])
    ma = ma.to_json(orient='records')
    return ma


def groupingday(data):
    day = data.groupby(data['tanggal'].dt.date).sum()
    day = day.reindex(pd.date_range(day.index.min(), day.index.max()), fill_value=0)
    tempdaymin = day.index.min()
    tempdaymax = day.index.max()
    day['tanggal'] = day.index
    tempday = day
    day = day.reset_index(drop=True)
    day['tanggal'] = pd.to_datetime(day['tanggal'])
    return {'day': day,
            'tempday': tempday,
            'tempdaymin': tempdaymin,
            'tempdaymax': tempdaymax
            }


def groupingmonth(data):
    month = data.groupby(pd.Grouper(key='tanggal', freq='M')).sum()
    month['tanggal'] = month.index
    month = month.reset_index(drop=True)
    return month


def groupingyear(data):
    year = data.groupby(data['tanggal'].dt.year).sum()
    year['tanggal'] = year.index
    year = year.reset_index(drop=True)
    return year


# Standar Bag of Word
'''def feature_extraction(dataset):
    tf = []
    # 0 tokenize
    nama_token = [i.split() for i in dataset['nama']]

    # 1 bag of word
    listword = []
    for x in dataset['nama']:
        tokens = nltk.word_tokenize(x)
        listword += tokens

    worddict = dict.fromkeys(listword, 0)

    # 2 create data with 0 value same with sum of data
    word_token = [dict.fromkeys(worddict, 0) for x in dataset['nama']]

    # 3 add = 1 for word same in nama_token
    for x, y in enumerate(nama_token):
        for word in nama_token[x]:
            word_token[x][word] += 1

    # 4 running tf from data before
    for x in word_token:
        # tf.append(compute_tf(word_token[x],nama_token[x]))
        tf.append(x.values())

    return tf'''


def feature_extraction(dataset):
    tf = []
    for x, y in enumerate(dataset['nama']):
        dataset['nama'][x] = re.sub(r'\b\w{1,2}\b', '', dataset['nama'][x])
        dataset['nama'][x] = re.sub(' +', ' ', dataset['nama'][x])

    # 0 tokenize
    nama_token = [i.split() for i in dataset['nama']]

    # 1 bag of word
    listword = []
    for x in dataset['nama']:
        tokens = nltk.word_tokenize(x)
        listword += tokens

    teks = [' '.join(listword)]
    v = TfidfVectorizer()
    x = v.fit_transform(teks)
    df1 = pd.DataFrame(x.toarray(), columns=v.get_feature_names())
    test = df1.melt(var_name="Produk")
    test.set_index('Produk', inplace=True)

    worddict = dict.fromkeys(listword, 0)

    # 2 create data with 0 value same with sum of data
    word_token = [dict.fromkeys(worddict, 0) for x in dataset['nama']]

    # 3 add = 1 for word same in nama_token
    for x, y in enumerate(nama_token):
        for word in nama_token[x]:
            print(word)
            word_token[x][word] += test.loc[word.lower()].values[0]

    # 4 Append to one data
    for x in word_token:
        # tf.append(compute_tf(word_token[x],nama_token[x]))
        tf.append(x.values())

    return tf


def silhoutte(init, data, kmax):
    sil = []

    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2, kmax):
        kmeans = KMeans(n_clusters=k).fit(data)
        labels = kmeans.labels_
        sil.append(silhouette_score(data, labels, metric='euclidean'))

    return sil


def clusteringdata(dataset, datafull, keyword, indexmonth, index3month, dataday):
    # If search is category not specific product
    if keyword is not None:
        dataset['nama'] = dataset['nama'].str.replace(keyword, '')
        dataset['nama'] = dataset['nama'].str.strip()
        dataset.replace('', np.nan, inplace=True)
        dataset = dataset.dropna()
        dataset.reset_index(drop=True)

    ''' # set kmax for finding k, maximum is 100 cluster
    kmax = datasetk.__len__()
    if kmax > 100:
        kmax = 100
        init = 30
    else:
        init = 2

    # if not category and specific product, duplicate them to 5 so the data will make their own cluster
    if keyword is not None:
        datasetk = pd.DataFrame(np.repeat(datasetk.values, 5, axis=0))
        datasetk = datasetk.rename(columns={0: 'nama', 1: 'tanggal'})

    # Feature Extraction for finding K
    readyclustering = pd.DataFrame(feature_extraction(datasetk))

    current_task.update_state(state='PROGRESS', meta={'status': 'Mencari Nilai K'})

    # Finding Best K with silhouette
    sil = silhoutte(init, readyclustering, kmax)
    k = sil.index(max(sil)) + init'''

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering'})

    # Perform k-Means clustering with k from Silhouette Method
    readyclustering = pd.DataFrame(feature_extraction(dataset))
    kmeans = KMeans(n_clusters=30).fit(readyclustering)
    clusters = kmeans.labels_

    # Create new column dataframe to labeling for every product
    hasilcluster = [i for i in clusters]
    data = dataset
    data['Assignment'] = hasilcluster

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering with K-Means Finished'})

    data = data.sort_values(by=['Assignment'])
    data = data.reset_index(drop=True)

    current_task.update_state(state='PROGRESS', meta={'status': 'Finding Total Produk'})

    # Mencari nama produk dengan mengetahui kata apa yang sering muncul di setiap produk
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

    tempdaymin = dataday.get('tempdaymin')
    tempdaymax = dataday.get('tempdaymax')

    trendataproduk = []
    trenmaproduk = []
    jumlahterjualproduk = []
    jumlahulasanproduk = []
    jumlahulasanproduk1bulan = []
    jumlahulasanproduk3bulan = []
    ymaxdata = []
    for i, j in enumerate(produk):
        temptanggalutama = []
        tempdata = data.loc[data['Assignment'] == i]
        tempjumlahterjual = tempdata['produk__jumlah_terjual'].sum()
        tempjumlahulasan = tempdata['produk__jumlah_ulasan'].sum()
        for k, l in enumerate(tempdata['produk__urlproduk']):
            temptanggal = datafull.loc[datafull['produk__urlproduk'] == l]
            temptanggalutama += temptanggal['tanggal'].to_list()
        temptanggalutama = pd.DataFrame({'tanggal': temptanggalutama})
        temptanggalutama = temptanggalutama.reset_index(drop=True)
        temptanggalutama['value'] = 1
        temptanggalutama = groupingday(temptanggalutama)
        temptanggalutama = temptanggalutama.get('day')
        temptanggalutama.index = temptanggalutama['tanggal']
        day = temptanggalutama.reindex(pd.bdate_range(tempdaymin, tempdaymax), fill_value=0)
        day['tanggal'] = day.index
        day = day.reset_index(drop=True)
        for o, p in enumerate(temptanggalutama['tanggal']):
            temptanggalutama['tanggal'][o] = temptanggalutama['tanggal'][o].tz_localize(None)
        day = pd.concat([temptanggalutama, day], axis=0)
        day = day.reset_index(drop=True)
        month = groupingmonth(day)
        bulan3 = month['value'][month.__len__() - 1] + month['value'][month.__len__() - 2] + month['value'][
            month.__len__() - 3]
        bulan1 = month['value'][month.__len__() - 1]
        ma = movingaverage(month, 3)
        jumlahulasanproduk1bulan.append(bulan1)
        jumlahulasanproduk3bulan.append(bulan3)
        ymaxdata.append(month)
        trendataproduk.append(month.to_json(orient='records'))
        trenmaproduk.append(ma)
        jumlahterjualproduk.append(tempjumlahterjual)
        jumlahulasanproduk.append(tempjumlahulasan)

    clusterfinish = pd.DataFrame({'trendataproduk': trendataproduk,
                                  'trenmaproduk': trenmaproduk,
                                  'jumlahterjualproduk': jumlahterjualproduk,
                                  'jumlahulasanproduk': jumlahulasanproduk,
                                  'jumlahulasan3bulan:': jumlahulasanproduk3bulan,
                                  'jumlahulasan1bulan': jumlahulasanproduk1bulan,
                                  'nama': produk})

    clusterfinish = clusterfinish.sort_values(by='jumlahterjualproduk')
    yaxis = 0
    for i in ymaxdata:
        if yaxis < max(i['value']):
            yaxis = max(i['value'])

    return {'clusterfinish': clusterfinish, 'yaxis': yaxis}


def trenulasan(dataset, judul):
    jumlahterjual = int(dataset['produk__jumlah_terjual'].sum())
    jumlahulasan = int(dataset['produk__jumlah_ulasan'].sum())
    dataset['tanggal'] = pd.to_datetime(dataset['tanggal'])
    dataset['value'] = 1

    # Grouping data by day and finding the highest review and lowest review and calculate Moving Average
    dataday = groupingday(dataset)
    day = dataday.get('day')
    maday = movingaverage(day, 7)
    day['tanggal'] = day['tanggal'].dt.strftime('%d %b, %Y')
    tinggihari = tanggaltinggi(day)
    rendahhari = tanggalrendah(day)
    day = day.to_json(orient='records')

    # Grouping data by month and finding the highest review and lowest review and calculate Moving Average
    datamonth = dataday.get('tempday')
    month = groupingmonth(datamonth)
    mamonth = movingaverage(month, 3)
    month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
    month = month.reset_index(drop=True)
    tinggibulan = tanggaltinggi(month)
    rendahbulan = tanggalrendah(month)
    month = month.to_json(orient='records')

    # Grouping data by year and finding the highest review and lowest review and calculate Moving Average
    datayear = dataday.get('tempday')
    year = groupingyear(datayear)
    mayear = movingaverage(year, 3)
    tinggitahun = year.loc[year['value'].idxmax()]
    tinggitahun = {
        'value': int(tinggitahun['value']),
        'tanggal': int(tinggitahun['tanggal'])
    }
    tinggitahun = json.dumps(tinggitahun)

    rendahtahun = year.loc[year['value'].idxmin()]
    rendahtahun = {
        'value': int(rendahtahun['value']),
        'tanggal': int(rendahtahun['tanggal'])
    }
    rendahtahun = json.dumps(rendahtahun)
    year = year.to_json(orient='records')

    # Update status
    current_task.update_state(state='PROGRESS',
                              meta={'status': 'Bag of Word', 'day': day, 'month': month, 'year': year,
                                    'tinggihari': tinggihari, 'tinggibulan': tinggibulan,
                                    'tinggitahun': tinggitahun,
                                    'rendahhari': rendahhari, 'rendahbulan': rendahbulan,
                                    'rendahtahun': rendahtahun,
                                    'judul': judul,
                                    'maday': maday,
                                    'mamonth': mamonth,
                                    'mayear': mayear})

    return dataday


@shared_task
def tasksearch(ecommerce, datestart, dateend, kategori, keyword):
    current_task.update_state(state='PROGRESS', meta={'status': 'Get Data From Database'})

    produkfixdata = pd.DataFrame(columns={'Produk', 'Jumlah', 'DataTanggal'})
    lastmonthtemp = pd.DataFrame(columns={'nama', 'Assignment'})
    last3monthtemp = pd.DataFrame(columns={'nama', 'Assignment'})

    if datestart.__len__() == 0:
        datestart = '2000-01-01'
        datestart = datetime.strptime(datestart, '%Y-%m-%d')
    if dateend.__len__() == 0:
        dateend = '2020-12-12'
        dateend = datetime.strptime(dateend, '%Y-%m-%d')

    indexmonth = 0
    index3month = 0
    statusdata = 0

    if keyword.__len__() == 0:
        dataset = pd.DataFrame(list(Ulasan.objects.filter(
            tanggal__range=[datestart, dateend]
        ).select_related('produk').filter(
            produk__kategori__icontains=kategori
        ).select_related('produk__toko').filter(
            produk__toko__ecommerce=ecommerce
        ).values(
            'produk__urlproduk', 'produk__nama_produk', 'produk__jumlah_terjual', 'produk__jumlah_ulasan', 'tanggal'
        )))

        datacluster = dataset
        dataday = trenulasan(dataset, kategori)
        time.sleep(10)

        datacluster.drop_duplicates(subset='produk__urlproduk', inplace=True)
        datacluster = datacluster.reset_index(drop=True)
        datacluster = datacluster.rename(index=str, columns={"produk__nama_produk": "nama"})
        keyword = None
        datatask = clusteringdata(datacluster, dataset, keyword, indexmonth, index3month, dataday)
        produkfinal = datatask.get('clusterfinish')
        last3month = produkfinal['jumlahulasan3bulan'].idxmax(axis=1)
        last1month = produkfinal['jumlahulasan1bulan'].idxmax(axis=1)

        finaldata = {
            'produk': produkfinal.to_json(orient='records'),
            'yaxis': datatask.get('yaxis'),
        }

        return finaldata
