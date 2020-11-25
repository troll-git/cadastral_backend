from django.core.management.base import BaseCommand
from django.utils import timezone
import wget
import os
import shutil
import zipfile
import pandas as pd
import numpy as np
from django.db import connection
from datetime import datetime
import time
import csv

MALOPOLSKA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_malopolskie.zip"
PODKARPACIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_podkarpackie.zip"
SLASKIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_slaskie.zip"
DOLNOSLASKIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_dolnoslaskie.zip"
OPOLSKIE = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_opolskie.zip"


ZGLOSZENIA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_zgloszenia.zip"

POZWOLENIA = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/pozwolenia'))
WNIOSKI = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/wnioski'))

REMOVE_DUPLICATES_POZWOLENIA="""DELETE FROM polyserver_api_pozwolenia
WHERE id IN
    (SELECT id
    FROM 
        (SELECT id,
         ROW_NUMBER() OVER( PARTITION BY numer_urzad,nazwa_organu,adres_organu,data_wplywu_wniosku,numer_decyzji_urzedu,
data_wydania_decyzji,nazwisko_inwestora,imie_inwestora,nazwa_inwestor,wojewodztwo,miasto,cecha,ulica,ulica_dalej,nr_domu,rodzaj_inwestycji,kategoria,nazwa_zamierzenia_bud,nazwa_zam_budowlanego,
kubatura,projektant_nazwisko,projektant_imie,projektant_numer_uprawnien,jednostka_numer_ew,
numer_dzialki,identyfikator,numer_arkusza_dzialki,jednostka_stara_numeracja_z_wniosku,stara_numeracja_obreb_z_wniosku,
stara_numeracja_dzialka_z_wniosku
        ORDER BY  id ) AS row_num
        FROM polyserver_api_pozwolenia ) t
        WHERE t.row_num > 1 );"""

REMOVE_DUPLICATES_WNIOSKI="""DELETE FROM polyserver_api_wnioski
WHERE id IN
    (SELECT id
    FROM 
        (SELECT id,
         ROW_NUMBER() OVER( PARTITION BY identyfikator,
  numer_ewidencyjny_system,
  data_wplywu_wniosku_do_urzedu
        ORDER BY  id ) AS row_num
        FROM polyserver_api_wnioski ) t
        WHERE t.row_num > 1 );
"""

class Command(BaseCommand):
    help = 'update the database'

    def clear_dir(self,directory):
        try:
            shutil.rmtree(directory)
            os.mkdir(directory)
            os.mkdir(directory)
            
        except:
            print("directory empty")
            os.mkdir(directory+'/failed')

               
        

    def save_data(self, url, directory):
        self.stdout.write("downloading data")
        print(directory)
        wget.download(url, out=directory)#UNCOMMENT THIS FOR ACTUAL DOWNLOAD!
    
    def unzip_folder(self,directory):
        for file in os.listdir(directory):
            if file.endswith(".zip"):
                print(file)
                zipf = zipfile.ZipFile(directory + '/' + file)
                zipf.extractall(directory) # UNCOMMENT THIS FOR ACTUAL UNZIP!

    def insert_data_pozwolenia(self, directory,chunk_rows):
        skipped=0
        failed=0
        updated=0
        failures = pd.DataFrame()
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                full_file=os.path.join(directory,file)
                data=pd.read_csv(full_file,delimiter="#",error_bad_lines=False,low_memory=False,lineterminator='\n',chunksize=chunk_rows)
                for chunk in data:
                    chunk = chunk.replace({np.nan: None})
                    chunk['identyfikator']=chunk['jednosta_numer_ew']+'.'+chunk['obreb_numer'].map(str).apply(self.int_to_4string)+'.'+chunk['numer_dzialki'].map(str)
                    [failures_log,skip,fail,update]=self.send_sql(chunk)
                    skipped =skip+skipped
                    failed +=fail
                    updated +=update
                    failures = failures.append(failures_log)
                save_file_name=directory+'/failed/'+file.split('.')[0]+"_failed.csv"
                failures.to_csv(save_file_name,index=False,sep='#')
        return [updated,skipped,failed]

    def insert_data_wnioski(self, directory,chunk_rows):
        skipped=0
        failed=0
        updated=0
        failures = pd.DataFrame()
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                full_file=os.path.join(directory,file)
                data=pd.read_csv(full_file,delimiter="#",error_bad_lines=False,low_memory=False,lineterminator='\n',chunksize=chunk_rows)
                for chunk in data:
                    chunk = chunk.replace({np.nan: None})
                    chunk['identyfikator']=chunk['jednostki_numer']+'.'+chunk['obreb_numer'].map(str).apply(self.int_to_4string)+'.'+chunk['numer_dzialki'].map(str)
                    [failures_log,skip,fail,update]=self.send_sql_wnioski(chunk)
                    skipped =skip+skipped
                    failed +=fail
                    updated +=update
                    failures = failures.append(failures_log)
                save_file_name=directory+'/failed/'+file.split('.')[0]+"_failed.csv"
                failures.to_csv(save_file_name,index=False,sep='#')
        return [updated,skipped,failed]

    def send_sql(self,data):
        with connection.cursor() as cursor:
            self.id=0
            self.inwestor=""
            self.failures=[]

            #for update data
            self.failed=0
            self.skipped=0
            self.updated=0
            # truncate table
            cursor.execute("TRUNCATE TABLE polyserver_api_pozwoleniaupload")
            for index,row in data.iterrows():
                numer_urzad = row['numer_urzad']
                numer_decyzji_urzedu = row['numer_decyzji_urzedu']
                numer_dzialki = row['numer_dzialki']
                zamierz_bud = row['nazwa_zamierzenia_bud']
                zam_budow = row['nazwa_zam_budowlanego']
                nazwisko_inwestora = row['nazwisko_inwestora']
                nazwa_inwestor = row['nazwa_inwestor']

                if(row['nazwa_inwestor']):
                    self.inwestor = row['nazwa_inwestor'][:75]
                listof=[row['numer_urzad'], row['nazwa_organu'], row['adres_organu'], row['data_wplywu_wniosku'],
                            row['numer_decyzji_urzedu'],row['data_wydania_decyzji'], row['nazwisko_inwestora'],row['imie_inwestora'],
                            row['nazwa_inwestor'], row['wojewodztwo'], row['miasto'], row['terc'],row['cecha'],row['ulica'],
                            row['ulica_dalej'], row['nr_domu'],row['rodzaj_inwestycji'], row['kategoria'],row['nazwa_zamierzenia_bud'],
                            row['nazwa_zam_budowlanego'], row['kubatura'], row['projektant_nazwisko'],row['projektant_imie'],
                            row['projektant_numer_uprawnien'], row['jednosta_numer_ew'],row['obreb_numer'], row['numer_dzialki'],
                            row['identyfikator'],row['numer_arkusza_dzialki'],row['jednostka_stara_numeracja_z_wniosku'],
                            row['stara_numeracja_obreb_z_wnioskiu'],row['stara_numeracja_dzialka_z_wniosku'],datetime.now()]
                #print(listof)    #temporary solution
                try:
                    cursor.execute("INSERT INTO polyserver_api_pozwolenia VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",listof )
                    self.updated +=1
                    print("insert "+str(self.updated)+ " from "+str(len(data.index)))
                except:
                    print("something went wrong")
                    self.failures.append(row)
                    self.failed +=1
            cursor.execute(REMOVE_DUPLICATES_POZWOLENIA)
            self.updated=cursor.rowcount
            print("removed:" +str(self.updated)+" duplicates.")
            self.skipped = len(data.index)-self.updated-self.failed
            
        return [pd.DataFrame(self.failures),self.skipped,self.failed,self.updated]
    def send_sql_wnioski(self,data):
        self.id=0
        self.failures=[]
            #for update data
        self.failed=0
        self.skipped=0
        
        with connection.cursor() as cursor:
            self.updated_rec=0            
            # truncate table
            cursor.execute("TRUNCATE TABLE polyserver_api_wnioskiupload")
            for index,row in data.iterrows():
                numer_ewidencyjny_system = row['numer_ewidencyjny_system']
                numer_dzialki = row['numer_dzialki']
                listof=[row['numer_ewidencyjny_system'], row['numer_ewidencyjny_urzad'], row['data_wplywu_wniosku_do_urzedu'],
                            row['nazwa_organu'], row['wojewodztwo_objekt'], row['obiekt_kod_pocztowy'], row['miasto'], row['terc'],row['cecha'],row['ulica'],
                            row['ulica_dalej'], row['nr_domu'],row['kategoria'],row['nazwa_zam_budowlanego'],
                            row['rodzaj_zam_budowlanego'], row['kubatura'], row['stan'], row['jednostki_numer'],row['obreb_numer'], row['numer_dzialki'],
                            row['identyfikator'],row['numer_arkusza_dzialki'],row['nazwisko_projektanta'],row['imie_projektanta'],row['projektant_numer_uprawnien'],row['projektant_pozostali'],datetime.now()]
                    #temporary solution
                try:
                    cursor.execute(
                        "INSERT INTO polyserver_api_wnioski VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",listof)
                    self.updated_rec +=1
                    print("insert "+str(self.updated_rec)+ " from "+str(len(data.index)))
                except:
                    print("something went wrong")
                    self.failed +=1
                    self.failures.append(row)
            cursor.execute(REMOVE_DUPLICATES_WNIOSKI)
            self.updated=cursor.rowcount
            print("removed:" +str(self.updated)+" duplicates.")
            self.skipped = len(data.index)-self.updated_rec-self.failed
        return [pd.DataFrame(self.failures),self.skipped,self.failed,self.updated_rec]
    def int_to_4string(self,number):
        zeros=""
        if(type(number)==str):
            number=number.split(".")[0]
        nr_of_zeros=4-len(str(number))
        for i in range(nr_of_zeros):
            zeros += "0"
        return (zeros + str(number))
    def merge_pozwolenia_parcels(self):
        print("Merging pozwolenia table with geometries")
        start = time.process_time()
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE polyserver_api_pozwoleniageom")
            cursor.execute("INSERT INTO polyserver_api_pozwoleniageom SELECT pozwolenia.*,area,mpoly FROM  polyserver_api_dzialki dzialki INNER JOIN polyserver_api_pozwolenia pozwolenia ON pozwolenia.identyfikator=dzialki.identyfikator")
            cursor.execute("UPDATE polyserver_api_pozwoleniageom SET point = ST_PointOnSurface(mpoly)")
            cursor.execute("UPDATE polyserver_api_pozwoleniageom SET point_wkt = ST_AsText(point)")
        print("Table updated, time elapsed: "+str(round(((time.process_time() - start) * 1000), 2))+" s.")

    def merge_wnioski_parcels(self):
        print("Merging wnioski table with geometries")
        start = time.process_time()
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE polyserver_api_wnioskigeom")
            cursor.execute("INSERT INTO polyserver_api_wnioskigeom SELECT wnioski.*,mpoly FROM  polyserver_api_dzialki dzialki INNER JOIN polyserver_api_wnioski wnioski ON wnioski.identyfikator=dzialki.identyfikator")
            cursor.execute("UPDATE polyserver_api_wnioskigeom SET point = ST_PointOnSurface(mpoly)")
            cursor.execute("UPDATE polyserver_api_wnioskigeom SET point_wkt = ST_AsText(point)")
        print("Table updated, time elapsed: "+str(round(((time.process_time() - start) * 1000), 2))+" s.")

    def update_data(self,pozwolenia_update,wnioski_update):
        print(pozwolenia_update)
        print(wnioski_update)
        dzialki=0
        pozwolenia=0
        pozwolenia_geom=0


        listof=[datetime.now(),pozwolenia_update[0],pozwolenia_update[1],pozwolenia_update[2],wnioski_update[0],wnioski_update[1],wnioski_update[2]]
        with connection.cursor() as cursor:
            #cursor.execute("SELECT nextval 'polyserver_api_update."id"'")

            cursor.execute("INSERT INTO polyserver_api_update VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s)",listof)


    def handle(self, *args, **kwargs):

        #clear directories
        
        
        #download pozwolenia data from GUNB
        #self.clear_dir(POZWOLENIA)
        #self.save_data(MALOPOLSKA, POZWOLENIA)
        #self.save_data(PODKARPACIE, POZWOLENIA)
        #self.save_data(SLASKIE, POZWOLENIA)
        #self.save_data(DOLNOSLASKIE, POZWOLENIA)
        #self.save_data(OPOLSKIE,POZWOLENIA)
        #self.unzip_folder(POZWOLENIA)

        #download wnioski
        #self.clear_dir(WNIOSKI)
        #self.save_data(ZGLOSZENIA,WNIOSKI)
        #self.unzip_folder(WNIOSKI)



        #self.update_data(self.insert_data_pozwolenia(POZWOLENIA,50000),self.insert_data_wnioski(WNIOSKI,50000))
        #self.merge_pozwolenia_parcels()
        self.merge_wnioski_parcels()

