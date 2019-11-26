# Create your tasks here
from __future__ import absolute_import, unicode_literals

import json
import time

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

    dataset['tanggal'] = pd.to_datetime(dataset['tanggal'])
    dataset['value'] = 1

    day = dataset.groupby(dataset['tanggal'].dt.date).sum()
    day['tanggal'] = day.index
    day = day.reset_index(drop=True)
    day = day.rename(index=str, columns={"Assignment": "jumlah"})
    day['tanggal'] = pd.to_datetime(day['tanggal'])
    day['tanggal'] = day['tanggal'].dt.strftime('%d %b, %Y')

    tinggihari = day.loc[day['value'].idxmax()]
    tinggihari = {
        'value': int(tinggihari['value']),
        'tanggal': tinggihari['tanggal']
    }
    tinggihari = json.dumps(tinggihari)

    rendahhari = day.loc[day['value'].idxmin()]
    rendahhari = {
        'value': int(rendahhari['value']),
        'tanggal': rendahhari['tanggal']
    }
    rendahhari = json.dumps(rendahhari)

    day = day.to_json(orient='records')

    month = dataset.groupby(pd.Grouper(key='tanggal', freq='M')).sum()
    month['tanggal'] = month.index
    month = month.reset_index(drop=True)
    month = month.rename(index=str, columns={"Assignment": "jumlah"})
    month['tanggal'] = month['tanggal'].dt.strftime('%b, %Y')
    month = month[month['value'] != 0]
    month = month.reset_index(drop=True)

    tinggibulan = month.loc[month['value'].idxmax()]
    tinggibulan = {
        'value': int(tinggibulan['value']),
        'tanggal': tinggibulan['tanggal']
    }
    tinggibulan = json.dumps(tinggibulan)

    rendahbulan = month.loc[month['value'].idxmin()]
    rendahbulan = {
        'value': int(rendahbulan['value']),
        'tanggal': rendahbulan['tanggal']
    }
    rendahbulan = json.dumps(rendahbulan)

    month = month.to_json(orient='records')

    year = dataset.groupby(dataset['tanggal'].dt.year).sum()
    year['tanggal'] = year.index
    year = year.reset_index(drop=True)
    year = year.rename(index=str, columns={"Assignment": "jumlah"})

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

    current_task.update_state(state='PROGRESS', meta={'status': 'Bag of Word', 'day': day, 'month': month, 'year': year,
                                                      'tinggihari': tinggihari, 'tinggibulan': tinggibulan, 'tinggitahun': tinggitahun,
                                                      'rendahhari': rendahhari, 'rendahbulan': rendahbulan, 'rendahtahun': rendahtahun})

    time.sleep(10)
    
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
    jumlah = [0]

    def jumlahulasan(data):
        a = 0
        assignment = data['Assignment'][0]
        for i, j in enumerate(data['Assignment']):
            if i != 0:
                if data['Assignment'][i] == assignment:
                    jumlah[a] += 1
                else:
                    a += 1
                    jumlah.append(1)
                    assignment = data['Assignment'][i]

    jumlahulasan(data)

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

    listprodukdata = []
    for i in produkfix.index:
        datatanggal = pd.DataFrame(data['tanggal'].loc[data['Assignment'] == i])
        datatanggal['value'] = 1
        day = datatanggal.groupby(datatanggal['tanggal'].dt.date).sum()
        day['tanggal'] = day.index
        day = day.reset_index(drop=True)
        day = day.rename(index=str, columns={"Assignment": "jumlah"})
        day['tanggal'] = pd.to_datetime(day['tanggal'])
        day['tanggal'] = day['tanggal'].dt.strftime('%d %b, %Y')
        listprodukdata.append(day.to_json(orient='records'))


    current_task.update_state(state='PROGRESS', meta={'status': 'Jumlah dan Tanggal Produk', 'listproduk': listprodukdata})

    time.sleep(10)

    produktinggi = produkfix.loc[produkfix['Jumlah'].idxmax()]
    produktinggi = {
        'jumlah': int(produktinggi['Jumlah']),
        'nama': produktinggi['Produk']
    }
    produktinggi = json.dumps(produktinggi)

    produkrendah = produkfix.loc[produkfix['Jumlah'].idxmin()]
    produkrendah = {
        'jumlah': int(produkrendah['Jumlah']),
        'nama': produkrendah['Produk']
    }
    produkrendah = json.dumps(produkrendah)

    lastmonth = data.sort_values(by="tanggal", ascending=True).set_index("tanggal").last("1M")
    lastmonth = lastmonth.sort_values(by=['Assignment'])
    lastmonth = lastmonth.reset_index(drop=True)
    jumlah = [0]
    jumlahulasan(lastmonth)
    jumlah = pd.DataFrame(jumlah)

    jumlahtinggi = jumlah.loc[jumlah.idxmax()]
    a = jumlahtinggi[0].index
    a = int(a.values)
    namaproduk = produkfix['Produk'][a]
    jmlproduk = int(jumlahtinggi[0])

    produkmonth = {
        'jumlah': jmlproduk,
        'nama': namaproduk
    }
    produkmonth = json.dumps(produkmonth)

    last3month = data.sort_values(by="tanggal", ascending=True).set_index("tanggal").last("3M")
    last3month = last3month.sort_values(by=['Assignment'])
    last3month = last3month.reset_index(drop=True)
    jumlah = [0]
    jumlahulasan(last3month)
    jumlah = pd.DataFrame(jumlah)

    jumlahtinggi = jumlah.loc[jumlah.idxmax()]
    a = jumlahtinggi[0].index
    a = int(a.values)
    namaproduk = produkfix['Produk'][a]
    jmlproduk = int(jumlahtinggi[0])

    produk3month = {
        'jumlah': jmlproduk,
        'nama': namaproduk
    }
    produk3month = json.dumps(produk3month)

    current_task.update_state(state='PROGRESS', meta={'status': 'Produk Tertinggi dan Terendah',
                                                      'produk3month': produk3month,
                                                      'produkmonth': produkmonth,
                                                      'produktinggi': produktinggi,
                                                      'produkrendah': produkrendah})

    time.sleep(5)

    totalulasan = produkfix.sort_values(by=['Jumlah'], ascending=False)
    totalulasan = totalulasan.reset_index(drop=True)

    return totalulasan.to_json(orient='records')