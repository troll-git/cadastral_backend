import wget
import os
import zipfile
malopolska = "http://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_malopolskie.zip"
pozwolenia = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/pozwolenia'))
wnioski = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/wnioski'))

def unzipFiles(directory):
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            print(file)
            zipf=zipfile.ZipFile(directory+'/'+file)
            zipf.extractall(directory)

print('downloading data')
#wget.download(malopolska,out=pozwolenia)

unzipFiles(pozwolenia)

