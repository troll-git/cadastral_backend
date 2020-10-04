from django.core.management.base import BaseCommand
from django.utils import timezone
import wget
import os
import zipfile
import pandas as pd
import numpy as np
from django.db import connection
from datetime import datetime
import time

MALOPOLSKA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_malopolskie.zip"
ZGLOSZENIA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_zgloszenia.zip"

POZWOLENIA = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/pozwolenia'))
WNIOSKI = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/wnioski'))


class Command(BaseCommand):
    help = 'update the database'

    def save_data(self, url, directory):
        self.stdout.write("downloading data")
        print(directory)
        #wget.download(url, out=directory)#UNCOMMENT THIS FOR ACTUAL DOWNLOAD!
        for file in os.listdir(directory):
            if file.endswith(".zip"):
                print(file)
                zipf = zipfile.ZipFile(directory + '/' + file)
                #zipf.extractall(directory) # UNCOMMENT THIS FOR ACTUAL DOWNLOAD!

    def insert_data(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                data=self.process_file(directory + '/' + file)
                #self.send_sql(data)

    def process_file(self,file):
        print(file)
        data=pd.read_csv(file,delimiter="#",error_bad_lines=False)
        data = data.replace({np.nan: None})
        data['identyfikator']=data['jednosta_numer_ew']+'.'+data['obreb_numer'].map(str).apply(self.int_to_4string)+'.'+data['numer_dzialki'].map(str)
        #replace nans with null
        print(data['identyfikator'])
        return data


    def send_sql(self,data):
        with connection.cursor() as cursor:
            self.id=0
            self.inwestor=""
            for index,row in data.iterrows():
                numer_urzad = row['numer_urzad']
                numer_decyzji_urzedu = row['numer_decyzji_urzedu']
                numer_dzialki = row['numer_dzialki']

                cursor.execute("SELECT * FROM polyserver_api_pozwolenia where numer_urzad = %s AND numer_decyzji_urzedu =%s AND numer_dzialki=%s",
                    [numer_urzad, numer_decyzji_urzedu, numer_dzialki])
                if(bool(cursor.fetchall())):
                    print("record existing, skipping")
                else:
                    print("insert "+str(self.id))
                    cursor.execute("SELECT id FROM polyserver_api_pozwolenia ORDER BY id DESC ")
                    idlist=cursor.fetchone()
                    if (idlist==None):
                        #print("no records")
                        self.id = 1
                    else:
                        #print(idlist)
                        self.id=idlist[0]+1
                    if(row['nazwa_inwestor']):
                        self.inwestor = row['nazwa_inwestor'][:75]
                    listof=[self.id,row['numer_urzad'], row['nazwa_organu'], row['adres_organu'], row['data_wplywu_wniosku'],
                            row['numer_decyzji_urzedu'],row['data_wydania_decyzji'], row['nazwisko_inwestora'],row['imie_inwestora'],
                            row['nazwa_inwestor'], row['wojewodztwo'], row['miasto'], row['terc'],row['cecha'],row['ulica'],
                            row['ulica_dalej'], row['nr_domu'],row['rodzaj_inwestycji'], row['kategoria'],row['nazwa_zamierzenia_bud'],
                            row['nazwa_zam_budowlanego'], row['kubatura'], row['projektant_nazwisko'],row['projektant_imie'],
                            row['projektant_numer_uprawnien'], row['jednosta_numer_ew'],row['obreb_numer'], row['numer_dzialki'],
                            row['identyfikator'],row['numer_arkusza_dzialki'],row['jednostka_stara_numeracja_z_wniosku'],
                            row['stara_numeracja_obreb_z_wnioskiu'],row['stara_numeracja_dzialka_z_wniosku'],datetime.now()]
                    #temporary solution
                    try:
                        pass
                        cursor.execute("INSERT INTO polyserver_api_pozwolenia VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",listof )
                    except:
                        print("something went wrong")
    def int_to_4string(self,number):
        zeros=""
        if(type(number)==str):
            number=number.split(".")[0]
        nr_of_zeros=4-len(str(number))
        for i in range(nr_of_zeros):
            zeros += "0"
        return (zeros + str(number))
    def merge_pozwolenia_parcels(self):
        start = time.process_time()
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE polyserver_api_pozwoleniageom")
            cursor.execute("INSERT INTO polyserver_api_pozwoleniageom SELECT pozwolenia.*,area,mpoly FROM  polyserver_api_dzialki dzialki INNER JOIN polyserver_api_pozwolenia pozwolenia ON pozwolenia.identyfikator=dzialki.identyfikator")
            cursor.execute("UPDATE polyserver_api_pozwoleniageom SET point = ST_PointOnSurface(mpoly)")
        print("Table updated, time elapsed: "+str(round(((time.process_time() - start) * 1000), 2))+" s.")

    def handle(self, *args, **kwargs):
        #self.save_data(MALOPOLSKA, POZWOLENIA)
        #self.save_data(ZGLOSZENIA,WNIOSKI)
        #self.insert_data(POZWOLENIA)
        self.merge_pozwolenia_parcels()

