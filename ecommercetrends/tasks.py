# Create your tasks here
from __future__ import absolute_import, unicode_literals

import string

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
'''from celery import current_app

current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True'''


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


'''# Standar Bag of Word
def feature_extraction(dataset):
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


def feature_extraction(datasetcluster):
    tf = []
    for x, y in enumerate(datasetcluster['nama']):
        datasetcluster['nama'][x] = datasetcluster['nama'][x].translate(
            str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    for x, y in enumerate(datasetcluster['nama']):
        datasetcluster['nama'][x] = datasetcluster['nama'][x].translate(
            str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

    for x, y in enumerate(datasetcluster['nama']):
        datasetcluster['nama'][x] = re.sub(r'\b\w{1,2}\b', '', datasetcluster['nama'][x])
        datasetcluster['nama'][x] = re.sub(' +', ' ', datasetcluster['nama'][x])

    # 0 tokenize
    nama_token = [i.split() for i in datasetcluster['nama']]

    # 1 bag of word
    listword = []
    for x in datasetcluster['nama']:
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
    word_token = [dict.fromkeys(worddict, 0) for x in datasetcluster['nama']]

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


def clusteringdata(dataset, datafull, keyword, kategori, dataday):
    # If search is category not specific product
    if keyword is not None:
        # set kmax for finding k, maximum is 100 cluster
        kmax = dataset.__len__()
        if kmax > 50:
            kmax = 50
            init = 10
        else:
            init = 2

        dataset['nama'] = dataset['nama'].str.replace(keyword, '')
        dataset['nama'] = dataset['nama'].str.strip()
        dataset.replace('', np.nan, inplace=True)
        dataset = dataset.dropna()
        dataset.reset_index(drop=True)

        # Feature Extraction for finding K
        readyclustering = pd.DataFrame(feature_extraction(dataset))

        # if not category and specific product, duplicate them to 5 so the data will make their own cluster
        readyclustering = pd.DataFrame(np.repeat(readyclustering.values, 5, axis=0))

        current_task.update_state(state='PROGRESS', meta={'status': 'Mencari Nilai K'})

        # Finding Best K with silhouette
        sil = silhoutte(init, readyclustering, kmax)
        k = sil.index(max(sil)) + init
    elif kategori == 'sepatu pria':
        k = 40
    elif kategori == 'Laptop':
        k = 30
    else:
        k = 20

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering'})
    # Feature Extraction for finding K
    readyclustering = pd.DataFrame(feature_extraction(dataset))
    # Perform k-Means clustering with k from Silhouette Method
    kmeans = KMeans(n_clusters=k).fit(readyclustering)
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
        month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
        trendataproduk.append(month.to_json(orient='records'))
        trenmaproduk.append(ma)
        jumlahterjualproduk.append(tempjumlahterjual)
        jumlahulasanproduk.append(tempjumlahulasan)

    clusterfinish = pd.DataFrame({'trendataproduk': trendataproduk,
                                  'trenmaproduk': trenmaproduk,
                                  'jumlahterjualproduk': jumlahterjualproduk,
                                  'jumlahulasanproduk': jumlahulasanproduk,
                                  'jumlahulasan3bulan': jumlahulasanproduk3bulan,
                                  'jumlahulasan1bulan': jumlahulasanproduk1bulan,
                                  'nama': produk})

    clusterfinish = clusterfinish.sort_values(by='jumlahterjualproduk', ascending=False)
    clusterfinish = clusterfinish.reset_index(drop=True)
    yaxis = 0
    for i in ymaxdata:
        if yaxis < max(i['value']):
            yaxis = max(i['value'])

    return {'clusterfinish': clusterfinish, 'yaxis': yaxis}


def trenulasan(dataset, judul, jumlahterjual, jumlahulasan):
    dataset['tanggal'] = pd.to_datetime(dataset['tanggal'])
    dataset['value'] = 1

    # Grouping data by day and finding the highest review and lowest review and calculate Moving Average
    dataday = groupingday(dataset)
    day = dataday.get('day')
    maday = movingaverage(day, 7)
    day['tanggal'] = day['tanggal'].dt.strftime('%d %b, %Y')
    tinggihari = tanggaltinggi(day)
    rendahhari = tanggalrendah(day)
    del day['produk__jumlah_terjual']
    del day['produk__jumlah_ulasan']
    day = day.to_json(orient='records')

    # Grouping data by month and finding the highest review and lowest review and calculate Moving Average
    datamonth = dataday.get('tempday')
    month = groupingmonth(datamonth)
    mamonth = movingaverage(month, 3)
    month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
    month = month.reset_index(drop=True)
    tinggibulan = tanggaltinggi(month)
    rendahbulan = tanggalrendah(month)
    del month['produk__jumlah_terjual']
    del month['produk__jumlah_ulasan']
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
    del year['produk__jumlah_terjual']
    del year['produk__jumlah_ulasan']
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
                                    'mayear': mayear,
                                    'jumlahterjual': jumlahterjual,
                                    'jumlahulasan': jumlahulasan})

    return dataday


@shared_task
def tasksearch(ecommerce, datestart, dateend, kategori, keyword):
    current_task.update_state(state='PROGRESS', meta={'status': 'Get Data From Database'})
    produkfinal = pd.DataFrame()

    if datestart.__len__() == 0:
        datestart = '2000-01-01'
        datestart = datetime.strptime(datestart, '%Y-%m-%d')
    if dateend.__len__() == 0:
        dateend = '2020-12-12'
        dateend = datetime.strptime(dateend, '%Y-%m-%d')

    statusdata = 0
    y = 0

    if keyword.__len__() == 0:
        keyword = None
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
        datacluster.drop_duplicates(subset='produk__urlproduk', inplace=True)
        datacluster = datacluster.reset_index(drop=True)
        datacluster = datacluster.rename(index=str, columns={"produk__nama_produk": "nama"})
        jumlahterjual = int(datacluster['produk__jumlah_terjual'].sum())
        jumlahulasan = int(datacluster['produk__jumlah_ulasan'].sum())
        dataday = trenulasan(dataset, kategori, jumlahterjual, jumlahulasan)
        time.sleep(10)
        datatask = clusteringdata(datacluster, dataset, keyword, kategori, dataday)
        produkfinal = datatask.get('clusterfinish')
        namaproduk = produkfinal['nama'].to_json(orient='records')
        dataproduk = produkfinal['trendataproduk'].to_json(orient='records')
        datamaproduk = produkfinal['trenmaproduk'].to_json(orient='records')
        jumlahterjual = produkfinal['jumlahterjualproduk'].to_json(orient='records')
        jumlahulasan = produkfinal['jumlahulasanproduk'].to_json(orient='records')
        jumlahulasan3bulan = produkfinal['jumlahulasan3bulan'].to_json(orient='records')
        jumlahulasan1bulan = produkfinal['jumlahulasan1bulan'].to_json(orient='records')

        bulan3tertinggi = produkfinal.loc[produkfinal['jumlahulasan3bulan'] == max(produkfinal['jumlahulasan3bulan'])]
        bulan3tertinggi = bulan3tertinggi.reset_index(drop=True)
        bulan1tertinggi = produkfinal.loc[produkfinal['jumlahulasan1bulan'] == max(produkfinal['jumlahulasan1bulan'])]
        bulan1tertinggi = bulan1tertinggi.reset_index(drop=True)

        tertinggi = {
            'nama': produkfinal['nama'][0],
            'jumlah': int(produkfinal['jumlahulasanproduk'][0]),
        }
        terendah = {
            'nama': produkfinal['nama'][produkfinal.__len__() - 1],
            'jumlah': int(produkfinal['jumlahulasanproduk'][produkfinal.__len__() - 1]),
        }
        terakhir3 = {
            'nama': bulan3tertinggi['nama'][0],
            'jumlah': int(bulan3tertinggi['jumlahulasan3bulan'][0]),
        }
        terakhir1 = {
            'nama': bulan1tertinggi['nama'][0],
            'jumlah': int(bulan1tertinggi['jumlahulasan1bulan'][0]),
        }

        tertinggi = json.dumps(tertinggi)
        terendah = json.dumps(terendah)
        terakhir3 = json.dumps(terakhir3)
        terakhir1 = json.dumps(terakhir1)

        finaldata = {
            'namaproduk': namaproduk,
            'dataproduk': dataproduk,
            'datamaproduk': datamaproduk,
            'jumlahterjual': jumlahterjual,
            'jumlahulasan': jumlahulasan,
            'jumlahulasan3bulan': jumlahulasan3bulan,
            'jumlahulasan1bulan': jumlahulasan1bulan,
            'tertinggi': tertinggi,
            'terendah': terendah,
            'terakhir1': terakhir1,
            'terakhir3': terakhir3,
            'yaxis': datatask.get('yaxis'),
        }

        return finaldata
    else:
        totalkeyword = keyword.split(sep=',')
        for m, n in enumerate(totalkeyword):
            totalkeyword[m] = n.strip()
            if totalkeyword[m].__len__() is 0 or totalkeyword[m].isspace():
                continue

            dataset = pd.DataFrame(list(Ulasan.objects.filter(
                tanggal__range=[datestart, dateend]
            ).select_related('produk').filter(
                Q(
                    produk__nama_produk__icontains=totalkeyword[m] + ' '
                ) | Q(
                    produk__nama_produk__icontains=' ' + totalkeyword[m] + ' '
                ) | Q(
                    produk__nama_produk__icontains=' ' + totalkeyword[m]
                ),
                produk__kategori__icontains=kategori
            ).select_related('produk__toko').filter(
                produk__toko__ecommerce=ecommerce
            ).values(
                'produk__urlproduk', 'produk__nama_produk', 'produk__jumlah_terjual', 'produk__jumlah_ulasan', 'tanggal'
            )))

            if dataset.__len__() is 0:
                continue
            else:
                statusdata = 1

            datacluster = dataset
            datacluster.drop_duplicates(subset='produk__urlproduk', inplace=True)
            datacluster = datacluster.reset_index(drop=True)
            datacluster = datacluster.rename(index=str, columns={"produk__nama_produk": "nama"})
            jumlahterjual = int(datacluster['produk__jumlah_terjual'].sum())
            jumlahulasan = int(datacluster['produk__jumlah_ulasan'].sum())
            dataday = trenulasan(dataset, totalkeyword[m], jumlahterjual, jumlahulasan)
            time.sleep(10)
            datatask = clusteringdata(datacluster, dataset, totalkeyword[m], kategori, dataday)
            if m == 0:
                produkfinal = datatask.get('clusterfinish')
                produkfinal['nama'] = totalkeyword[m] + ' ' + produkfinal['nama']
            else:
                produktemp = datatask.get('clusterfinish')
                produktemp['nama'] = totalkeyword[m] + ' ' + produktemp['nama']
                produkfinal = produkfinal.append(produktemp, ignore_index= True)

            if y < datatask.get('yaxis'):
                y = datatask.get('yaxis')

        if statusdata is 0:
            return 'FAIL'

        produkfinal = produkfinal.sort_values(by='jumlahterjualproduk', ascending=False)
        produkfinal = produkfinal.reset_index(drop=True)

        namaproduk = produkfinal['nama'].to_json(orient='records')
        dataproduk = produkfinal['trendataproduk'].to_json(orient='records')
        datamaproduk = produkfinal['trenmaproduk'].to_json(orient='records')
        jumlahterjual = produkfinal['jumlahterjualproduk'].to_json(orient='records')
        jumlahulasan = produkfinal['jumlahulasanproduk'].to_json(orient='records')
        jumlahulasan3bulan = produkfinal['jumlahulasan3bulan'].to_json(orient='records')
        jumlahulasan1bulan = produkfinal['jumlahulasan1bulan'].to_json(orient='records')

        bulan3tertinggi = produkfinal.loc[produkfinal['jumlahulasan3bulan'] == max(produkfinal['jumlahulasan3bulan'])]
        bulan3tertinggi = bulan3tertinggi.reset_index(drop=True)
        bulan1tertinggi = produkfinal.loc[produkfinal['jumlahulasan1bulan'] == max(produkfinal['jumlahulasan1bulan'])]
        bulan1tertinggi = bulan1tertinggi.reset_index(drop=True)

        tertinggi = {
            'nama': produkfinal['nama'][0],
            'jumlah': int(produkfinal['jumlahulasanproduk'][0]),
        }
        terendah = {
            'nama': produkfinal['nama'][produkfinal.__len__() - 1],
            'jumlah': int(produkfinal['jumlahulasanproduk'][produkfinal.__len__() - 1]),
        }
        terakhir3 = {
            'nama': bulan3tertinggi['nama'][0],
            'jumlah': int(bulan3tertinggi['jumlahulasan3bulan'][0]),
        }
        terakhir1 = {
            'nama': bulan1tertinggi['nama'][0],
            'jumlah': int(bulan1tertinggi['jumlahulasan1bulan'][0]),
        }

        tertinggi = json.dumps(tertinggi)
        terendah = json.dumps(terendah)
        terakhir3 = json.dumps(terakhir3)
        terakhir1 = json.dumps(terakhir1)

        finaldata = {
            'namaproduk': namaproduk,
            'dataproduk': dataproduk,
            'datamaproduk': datamaproduk,
            'jumlahterjual': jumlahterjual,
            'jumlahulasan': jumlahulasan,
            'jumlahulasan3bulan': jumlahulasan3bulan,
            'jumlahulasan1bulan': jumlahulasan1bulan,
            'tertinggi': tertinggi,
            'terendah': terendah,
            'terakhir1': terakhir1,
            'terakhir3': terakhir3,
            'yaxis': y,
        }

        return finaldata
