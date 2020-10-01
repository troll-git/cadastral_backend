from django.core.management.base import BaseCommand
from django.utils import timezone
import wget
import os
import zipfile
import pandas as pd

MALOPOLSKA = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_malopolskie.zip"
POZWOLENIA = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/pozwolenia'))
wnioski = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../data/wnioski'))


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
                self.process_file(directory + '/' + file)

    def process_file(self,file):
        print(file)
        data=pd.read_csv(file,nrows=10,delimiter="#")
        print(data.columns)

    def handle(self, *args, **kwargs):
        self.save_data(MALOPOLSKA, POZWOLENIA)
        self.insert_data(POZWOLENIA)
