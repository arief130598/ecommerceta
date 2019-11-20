from django.shortcuts import render
import pyodbc
import pandas as pd
import nltk
from sklearn.cluster import KMeans

# Create your views here.


def home(request):
    return render(request, 'home.html')


def search(request):
    box1 = request.POST.get('box1')
    box2 = request.POST.get('box2')
    box3 = request.POST.get('box3')

    if box1 == "men":
        if box2 == 'Clothing':
            print(box2)
        elif box2 == 'Shoes':
            if box3 == '':
                # READ DATA FROM SQL
                conn = pyodbc.connect(
                    r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:ecommerceta.database.windows.net,1433;Database=ecommerceta;Uid=knight;Pwd={Arief-1305};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=1000;')

                SQL_Query = pd.read_sql_query('''select produk, tanggal from ecommercetrends_sepatupria''', conn)

                dataset = pd.DataFrame(SQL_Query)
                dataset = dataset.rename(index=str, columns={"produk": "nama", "tanggal": "tanggal"})

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

                # 4 tf function
                '''def compute_tf(word_dict, l):
                    tf = {}
                    sum_nk = len(l)
                    for word, count in word_dict.items():
                        tf[word] = count / sum_nk
                    return tf'''

                # 5 running tf from data before
                tf = []
                for x, y in enumerate(word_token):
                    # tf.append(compute_tf(word_token[x],nama_token[x]))
                    tf.append(word_token[x].values())

                # data feature extraction save as dataframe
                readyclustering = pd.DataFrame(data=tf)

                kmeans = KMeans(n_clusters=8, max_iter=200).fit(readyclustering)
                clusters = kmeans.fit_predict(readyclustering)

                hasilcluster = []
                for i in clusters:
                    hasilcluster.append(i)

                data = dataset
                data['Assignment'] = hasilcluster

                data = data.sort_values(by=['Assignment'])
                data = data.reset_index(drop=True)

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

        else:
            print(box2)

    return render(request, 'ecommercetrends/search.html')
