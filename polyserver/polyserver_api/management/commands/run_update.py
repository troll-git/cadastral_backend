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
PODKARPACIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_podkarpackie.zip"
SLASKIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_slaskie.zip"


ZGLOSZENIA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_zgloszenia.zip"

POZWOLENIA = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/pozwolenia'))
WNIOSKI = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/wnioski'))


class Command(BaseCommand):
    help = 'update the database'

    def save_data(self, url, directory):
        self.stdout.write("downloading data")
        print(directory)
        wget.download(url, out=directory)#UNCOMMENT THIS FOR ACTUAL DOWNLOAD!
        for file in os.listdir(directory):
            if file.endswith(".zip"):
                print(file)
                zipf = zipfile.ZipFile(directory + '/' + file)
                zipf.extractall(directory) # UNCOMMENT THIS FOR ACTUAL DOWNLOAD!

    def insert_data_pozwolenia(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                data=self.process_file(directory + '/' + file)
                self.failed=self.send_sql(data)
                save_file_name=directory+'/failed/'+file.split('.')[0]+"_failed.csv"
                #uncomment to save file
                self.failed.to_csv(save_file_name,index=False,sep='#')
                #print(self.failed)

    def insert_data_wnioski(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                data=self.process_file_wnioski(directory + '/' + file)
                print(data)
                self.failed=self.send_sql_wnioski(data)
                save_file_name=directory+'/failed/'+file.split('.')[0]+"_failed.csv"
                #uncomment to save file
                #self.failed.to_csv(save_file_name,index=False,sep='#')
                #print(self.failed)

    def process_file(self,file):
        print(file)
        #add nrows=nr of records
        data=pd.read_csv(file,delimiter="#", error_bad_lines=False)
        data = data.replace({np.nan: None})
        data['identyfikator']=data['jednosta_numer_ew']+'.'+data['obreb_numer'].map(str).apply(self.int_to_4string)+'.'+data['numer_dzialki'].map(str)
        #replace nans with null
        #print(data['identyfikator'])
        return data

    def process_file_wnioski(self,file):
        print(file)
        #add nrows=nr of records
        data=pd.read_csv(file,delimiter="#",nrows=3000, error_bad_lines=False)
        data = data.replace({np.nan: None})
        data['identyfikator']=data['jednostki_numer']+'.'+data['obreb_numer'].map(str).apply(self.int_to_4string)+'.'+data['numer_dzialki'].map(str)
        #replace nans with null
        #print(data['identyfikator'])
        return data


    def send_sql(self,data):
        with connection.cursor() as cursor:
            self.id=0
            self.inwestor=""
            self.failures=[]
            for index,row in data.iterrows():


                numer_urzad = row['numer_urzad']
                numer_decyzji_urzedu = row['numer_decyzji_urzedu']
                numer_dzialki = row['numer_dzialki']
                zamierz_bud = row['nazwa_zamierzenia_bud']
                zam_budow = row['nazwa_zam_budowlanego']
                nazwisko_inwestora = row['nazwisko_inwestora']
                nazwa_inwestor = row['nazwa_inwestor']
                #print(nazwisko_inwestora)
                #print(nazwa_inwestor)
                #print(numer_dzialki)

                cursor.execute("SELECT * FROM polyserver_api_pozwolenia where numer_urzad = %s "
                               "AND numer_decyzji_urzedu =%s"
                               " AND (numer_dzialki=%s OR numer_dzialki ISNULL) "
                               "AND (nazwa_zamierzenia_bud ISNULL OR nazwa_zamierzenia_bud=%s)"
                               " AND (nazwa_zam_budowlanego ISNULL OR nazwa_zam_budowlanego=%s)"
                               " AND (nazwisko_inwestora ISNULL OR nazwisko_inwestora=%s) "
                               "AND (nazwa_inwestor ISNULL OR nazwa_inwestor=%s)",
                    [numer_urzad, numer_decyzji_urzedu, numer_dzialki,zamierz_bud,zam_budow,nazwisko_inwestora,nazwa_inwestor])
                #print(cursor.fetchone())
                #print(bool(cursor.fetchone()))
                if(cursor.fetchone()):
                    print(str(index)+" record existing, skipping")
                else:
                    #print(row)
                    print(str(index)+" insert "+str(self.id))
                    cursor.execute("SELECT MAX(id) FROM polyserver_api_pozwolenia AS maxid")
                    idlist=cursor.fetchone()
                    #print("idmax:"+str(idlist))
                    if (idlist[0]==None):
                        print("no records")
                        self.id = 1
                    else:
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
                        self.failures.append(row)
        return pd.DataFrame(self.failures)
    def send_sql_wnioski(self,data):
        with connection.cursor() as cursor:
            self.id=0
            self.failures=[]
            for index,row in data.iterrows():


                numer_ewidencyjny_system = row['numer_ewidencyjny_system']
                numer_dzialki = row['numer_dzialki']


                cursor.execute("SELECT * FROM polyserver_api_wnioski where numer_ewidencyjny_system = %s "
                               " AND (numer_dzialki=%s OR numer_dzialki ISNULL) ",

                    [numer_ewidencyjny_system,numer_dzialki])
                #print(cursor.fetchone())
                #print(bool(cursor.fetchone()))
                if(cursor.fetchone()):
                    print(str(index)+" record existing, skipping")
                else:
                    #print(row)
                    print(str(index)+" insert "+str(self.id))
                    cursor.execute("SELECT MAX(id) FROM polyserver_api_wnioski AS maxid")
                    idlist=cursor.fetchone()
                    #print("idmax:"+str(idlist))
                    if (idlist[0]==None):
                        print("no records")
                        self.id = 1
                    else:
                        self.id=idlist[0]+1
                    listof=[self.id,row['numer_ewidencyjny_system'], row['numer_ewidencyjny_urzad'], row['data_wplywu_wniosku_do_urzedu'],
                            row['nazwa_organu'], row['wojewodztwo_objekt'], row['obiekt_kod_pocztowy'], row['miasto'], row['terc'],row['cecha'],row['ulica'],
                            row['ulica_dalej'], row['nr_domu'],row['kategoria'],row['nazwa_zam_budowlanego'],
                            row['rodzaj_zam_budowlanego'], row['kubatura'], row['stan'], row['jednostki_numer'],row['obreb_numer'], row['numer_dzialki'],
                            row['identyfikator'],row['numer_arkusza_dzialki'],row['nazwisko_projektanta'],row['imie_projektanta'],row['projektant_numer_uprawnien'],row['projektant_pozostali'],datetime.now()]
                    #temporary solution
                    #print(listof)

                    try:
                        cursor.execute(
                            "INSERT INTO polyserver_api_wnioski VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            listof)
                    except:
                        print("something went wrong")
                        self.failures.append(row)
        return pd.DataFrame(self.failures)
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

    def merge_wnioski_parcels(self):
        start = time.process_time()
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE polyserver_api_wnioskigeom")
            cursor.execute("INSERT INTO polyserver_api_wnioskigeom SELECT wnioski.*,mpoly FROM  polyserver_api_dzialki dzialki INNER JOIN polyserver_api_wnioski wnioski ON wnioski.identyfikator=dzialki.identyfikator")
            cursor.execute("UPDATE polyserver_api_wnioskigeom SET point = ST_PointOnSurface(mpoly)")
        print("Table updated, time elapsed: "+str(round(((time.process_time() - start) * 1000), 2))+" s.")

    def handle(self, *args, **kwargs):
        #self.save_data(MALOPOLSKA, POZWOLENIA)
        #self.save_data(PODKARPACIE, POZWOLENIA)
        #self.save_data(SLASKIE, POZWOLENIA)
        #self.save_data(ZGLOSZENIA,WNIOSKI)

        #self.insert_data_pozwolenia(POZWOLENIA)
        self.insert_data_wnioski(WNIOSKI)

        #self.merge_pozwolenia_parcels()
        self.merge_wnioski_parcels()

