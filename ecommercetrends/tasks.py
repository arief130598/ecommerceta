# Create your tasks here
from __future__ import absolute_import, unicode_literals

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

from celery import shared_task, current_task

# Library for debugging celery
'''from celery import current_app

current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
'''
from ecommercetrends.models import Ulasan, Produk, Toko


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

    # 4 tf function
    '''def compute_tf(word_dict, l):
        tf = {}
        sum_nk = len(l)
        for word, count in word_dict.items():
            tf[word] = count / sum_nk
        return tf'''

    # 5 running tf from data before
    for x in word_token:
        # tf.append(compute_tf(word_token[x],nama_token[x]))
        tf.append(x.values())

    return tf


def silhoutte(data, kmax):
    sil = []

    # dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
    for k in range(2, kmax):
        kmeans = KMeans(n_clusters=k).fit(data)
        labels = kmeans.labels_
        sil.append(silhouette_score(data, labels, metric='euclidean'))

    return sil


def task(dataset, judul, jumproduk, indexmonth, index3month):
    dataset = dataset.rename(index=str, columns={"produk__nama_produk": "nama", "tanggal": "tanggal"})

    dataset['tanggal'] = pd.to_datetime(dataset['tanggal'])
    dataset['value'] = 1

    dataday = groupingday(dataset)
    day = dataday.get('day')
    maday = movingaverage(day, 7)
    day['tanggal'] = day['tanggal'].dt.strftime('%d %b, %Y')
    tinggihari = tanggaltinggi(day)
    rendahhari = tanggalrendah(day)
    day = day.to_json(orient='records')

    datamonth = dataday.get('tempday')
    month = groupingmonth(datamonth)
    mamonth = movingaverage(month, 3)
    month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
    month = month.reset_index(drop=True)
    tinggibulan = tanggaltinggi(month)
    rendahbulan = tanggalrendah(month)
    month = month.to_json(orient='records')

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

    time.sleep(15)

    if jumproduk is not 1:
        dataset['nama'] = dataset['nama'].str.replace(judul, '')
        dataset['nama'] = dataset['nama'].str.strip()
        dataset.replace('', np.nan, inplace=True)
        dataset = dataset.dropna()

    datasetk = dataset
    datasetk = datasetk.drop_duplicates(subset='nama', keep='first')
    datasetk = datasetk.reset_index(drop=True)
    datasetk['nama'] = datasetk['nama'].str.replace('[^\w\s]', ' ')

    kmax = datasetk.__len__()
    if kmax > 100:
        kmax = 100

    if jumproduk is not 1:
        datasetk = pd.DataFrame(np.repeat(datasetk.values, 5, axis=0))
        datasetk = datasetk.rename(columns={0: 'nama', 1: 'tanggal'})

    readyclustering = pd.DataFrame(feature_extraction(datasetk))

    current_task.update_state(state='PROGRESS', meta={'status': 'Mencari Nilai K'})

    # Finding Best K with silhouette
    sil = silhoutte(readyclustering, kmax)
    k = sil.index(max(sil)) + 2

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering'})

    readyclustering = pd.DataFrame(feature_extraction(dataset))
    kmeans = KMeans(n_clusters=k, max_iter=200).fit(readyclustering)
    clusters = kmeans.labels_

    hasilcluster = [i for i in clusters]

    data = dataset
    data['Assignment'] = hasilcluster

    current_task.update_state(state='PROGRESS', meta={'status': 'Clustering with K-Means Finished'})

    data = data.sort_values(by=['Assignment'])
    data = data.reset_index(drop=True)

    current_task.update_state(state='PROGRESS', meta={'status': 'Finding Total Produk'})

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

    for i, j in enumerate(produk):
        data.loc[data['Assignment'] == i, 'nama'] = j

    produkfix = jumlahulasan(data)

    lastmonth = data.sort_values(by="tanggal", ascending=True).set_index("tanggal").last("1M")
    lastmonth = lastmonth.sort_values(by=['Assignment'])
    lastmonth = lastmonth.reset_index(drop=True)
    lastmonth.index += indexmonth

    last3month = data.sort_values(by="tanggal", ascending=True).set_index("tanggal").last("3M")
    last3month = last3month.sort_values(by=['Assignment'])
    last3month = last3month.reset_index(drop=True)
    last3month.index += index3month

    maxyaxis = 0
    # Mencari data tanggal untuk setiap jenis produk
    listprodukdata = []
    listprodukdatama = []
    tempdaymin = dataday.get('tempdaymin')
    tempdaymax = dataday.get('tempdaymax')

    for i in produkfix.index:
        datatanggal = pd.DataFrame(data['tanggal'].loc[data['Assignment'] == i])
        datatanggal['value'] = 1

        day = datatanggal.groupby(datatanggal['tanggal'].dt.date).sum()
        day = day.reindex(pd.date_range(tempdaymin, tempdaymax), fill_value=0)
        day['tanggal'] = day.index

        month = day.groupby(pd.Grouper(key='tanggal', freq='M')).sum()
        month['tanggal'] = month.index
        month = month.reset_index(drop=True)
        month = month.rename(index=str, columns={"Assignment": "jumlah"})
        month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
        month = month.reset_index(drop=True)
        if month['value'].max() > maxyaxis:
            maxyaxis = month['value'].max()

        movingaveragedatamonth = []
        for k, l in enumerate(month['value']):
            if k >= 5:
                tempaverage = (month['value'][k] + month['value'][k - 5] + month['value'][k - 4] + month['value'][
                    k - 3] + month['value'][k - 2] + month['value'][k - 1]) / 5
                movingaveragedatamonth.append(tempaverage)
            else:
                movingaveragedatamonth.append(0)

        mamonth = pd.DataFrame(movingaveragedatamonth, columns=['value'])
        listprodukdatama.append(mamonth.to_dict(orient='records'))
        listprodukdata.append(month.to_dict(orient='records'))

    produkfix['DataTanggal'] = listprodukdata
    produkfix['DataTanggalMA'] = listprodukdatama

    finaldatatask = {
        'produkfix': produkfix,
        'lastmonth': lastmonth,
        'last3month': last3month,
        'yaxis': maxyaxis
    }

    return finaldatatask


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
        dataset = pd.DataFrame(list(Ulasan.objects.select_related('produk').filter(
            produk__kategori__icontains=kategori
        ).select_related('produk__toko').filter(produk__toko__ecommerce=ecommerce).values(
            'produk__nama_produk', 'tanggal')))

        jumlahterjual = pd.DataFrame(list(Produk.objects.filter(
            kategori__icontains='Sepatu Pria'
        ).select_related('toko').filter(toko__ecommerce='Shopee').values(
            'jumlah_terjual')))
        jumlahterjual = jumlahterjual.sum()
        jumlahterjual = int(jumlahterjual.values)

        jumlahulasantotal = pd.DataFrame(list(Produk.objects.filter(
            kategori__icontains='Sepatu Pria'
        ).select_related('toko').filter(toko__ecommerce='Shopee').values(
            'jumlah_ulasan')))
        jumlahulasantotal = jumlahulasantotal.sum()
        jumlahulasantotal = int(jumlahulasantotal.values)

        dataset = dataset.rename(index=str, columns={"produk__nama_produk": "nama", "tanggal": "tanggal"})
        jumproduk = 1

        datatask = task(dataset, kategori, jumproduk, indexmonth, index3month)

        produkfixdata = datatask.get('produkfix')
        produkfixdata = sortdata(produkfixdata)
        produkfixtinggi = produktinggi(produkfixdata)
        produkfixrendah = produkrendah(produkfixdata)

        lastmonthtemp = datatask.get('lastmonth')
        lastmonthtemp = jumlahulasan(lastmonthtemp)
        lastmonthtinggi = produktinggi(lastmonthtemp)

        last3monthtemp = datatask.get('last3month')
        last3monthtemp = jumlahulasan(last3monthtemp)
        last3monthtinggi = produktinggi(last3monthtemp)

        yaxis = datatask.get('yaxis')
        yaxis = yaxis.astype(str)

        finaldata = {
            'produk': produkfixdata.to_json(orient='records'),
            'produktinggi': produkfixtinggi,
            'produkrendah': produkfixrendah,
            'lastmonth': lastmonthtinggi,
            'last3month': last3monthtinggi,
            'yaxis': yaxis,
        }

        return finaldata

    else:
        loop = katmodel2.split(sep=',')
        jumproduk = -1
        yaxistemp = []

        for m, n in enumerate(loop):
            loop[m] = n.strip()
            if loop[m].__len__() is 0 or loop[m].isspace():
                continue

            data = pd.DataFrame(list(models.SepatuPria.objects.filter(
                Q(produk__icontains=loop[m] + ' ') | Q(produk__icontains=' ' + loop[m] + ' ') | Q(
                    produk__icontains=' ' + loop[m])).filter(tanggal__range=[datestart, dateend]).values('produk',
                                                                                                         'tanggal')))

            if data.__len__() is 0:
                continue
            else:
                statusdata = 1

            datatask = task(data, loop[m], jumproduk, indexmonth, index3month)

            yaxistemp.append(datatask.get('yaxis'))

            datatemp = datatask.get('produkfix')
            datatemp['Produk'] = loop[m] + ' ' + datatemp['Produk']
            produkfixdata = produkfixdata.append(datatemp, sort=False)

            monthtemp = datatask.get('lastmonth')
            monthtemp['nama'] = loop[m] + ' ' + monthtemp['nama']
            lastmonthtemp = lastmonthtemp.append(monthtemp, sort=False)

            month3temp = datatask.get('last3month')
            month3temp['nama'] = loop[m] + ' ' + month3temp['nama']
            last3monthtemp = last3monthtemp.append(month3temp, sort=False)

            indexmonth = indexmonth + lastmonthtemp.__len__()
            index3month = index3month + last3monthtemp.__len__()

        if statusdata is 0:
            return 'FAIL'

        yaxis = max(yaxistemp).astype(str)

        produkfixdata = sortdata(produkfixdata)
        produkfixtinggi = produktinggi(produkfixdata)
        produkfixrendah = produkrendah(produkfixdata)

        lastmonthtinggi = jumlahulasan(lastmonthtemp)
        lastmonthtinggi = produktinggi(lastmonthtinggi)

        last3monthtinggi = jumlahulasan(last3monthtemp)
        last3monthtinggi = produktinggi(last3monthtinggi)

        finaldata = {
            'produk': produkfixdata.to_json(orient='records'),
            'produktinggi': produkfixtinggi,
            'produkrendah': produkfixrendah,
            'lastmonth': lastmonthtinggi,
            'last3month': last3monthtinggi,
            'yaxis': yaxis,
        }

        return finaldata


@shared_task
def totalulasan(katmodel, katmodel2, datestart, dateend):
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

    if katmodel == 'Sepatu Pria':
        if katmodel2 == '':
            dataset = pd.DataFrame(
                list(models.SepatuPria.objects.filter(tanggal__range=[datestart, dateend]).values('produk', 'tanggal')))
            jumproduk = 1
            datatask = task(dataset, katmodel, jumproduk, indexmonth, index3month)

            produkfixdata = datatask.get('produkfix')
            produkfixdata = sortdata(produkfixdata)
            produkfixtinggi = produktinggi(produkfixdata)
            produkfixrendah = produkrendah(produkfixdata)

            lastmonthtemp = datatask.get('lastmonth')
            lastmonthtemp = jumlahulasan(lastmonthtemp)
            lastmonthtinggi = produktinggi(lastmonthtemp)

            last3monthtemp = datatask.get('last3month')
            last3monthtemp = jumlahulasan(last3monthtemp)
            last3monthtinggi = produktinggi(last3monthtemp)

            yaxis = datatask.get('yaxis')
            yaxis = yaxis.astype(str)

            finaldata = {
                'produk': produkfixdata.to_json(orient='records'),
                'produktinggi': produkfixtinggi,
                'produkrendah': produkfixrendah,
                'lastmonth': lastmonthtinggi,
                'last3month': last3monthtinggi,
                'yaxis': yaxis,
            }

            return finaldata

        else:
            loop = katmodel2.split(sep=',')
            jumproduk = -1
            yaxistemp = []

            for m, n in enumerate(loop):
                loop[m] = n.strip()
                if loop[m].__len__() is 0 or loop[m].isspace():
                    continue

                data = pd.DataFrame(list(models.SepatuPria.objects.filter(
                    Q(produk__icontains=loop[m] + ' ') | Q(produk__icontains=' ' + loop[m] + ' ') | Q(
                        produk__icontains=' ' + loop[m])).filter(tanggal__range=[datestart, dateend]).values('produk',
                                                                                                             'tanggal')))

                if data.__len__() is 0:
                    continue
                else:
                    statusdata = 1

                datatask = task(data, loop[m], jumproduk, indexmonth, index3month)

                yaxistemp.append(datatask.get('yaxis'))

                datatemp = datatask.get('produkfix')
                datatemp['Produk'] = loop[m] + ' ' + datatemp['Produk']
                produkfixdata = produkfixdata.append(datatemp, sort=False)

                monthtemp = datatask.get('lastmonth')
                monthtemp['nama'] = loop[m] + ' ' + monthtemp['nama']
                lastmonthtemp = lastmonthtemp.append(monthtemp, sort=False)

                month3temp = datatask.get('last3month')
                month3temp['nama'] = loop[m] + ' ' + month3temp['nama']
                last3monthtemp = last3monthtemp.append(month3temp, sort=False)

                indexmonth = indexmonth + lastmonthtemp.__len__()
                index3month = index3month + last3monthtemp.__len__()

            if statusdata is 0:
                return 'FAIL'

            yaxis = max(yaxistemp).astype(str)

            produkfixdata = sortdata(produkfixdata)
            produkfixtinggi = produktinggi(produkfixdata)
            produkfixrendah = produkrendah(produkfixdata)

            lastmonthtinggi = jumlahulasan(lastmonthtemp)
            lastmonthtinggi = produktinggi(lastmonthtinggi)

            last3monthtinggi = jumlahulasan(last3monthtemp)
            last3monthtinggi = produktinggi(last3monthtinggi)

            finaldata = {
                'produk': produkfixdata.to_json(orient='records'),
                'produktinggi': produkfixtinggi,
                'produkrendah': produkfixrendah,
                'lastmonth': lastmonthtinggi,
                'last3month': last3monthtinggi,
                'yaxis': yaxis,
            }

            return finaldata
