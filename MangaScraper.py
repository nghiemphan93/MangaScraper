# region Import
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import os
from fpdf import FPDF
from PIL import Image


# endregion


class MangaScraper:
   def __init__(self, url: str, outputFolder='./'):
      self.url = url
      self.mangaName = url.split("/")[-1]
      self.outputFolder = outputFolder
      self.outputPath = os.path.join(self.outputFolder, self.mangaName)
      # self.session      = requests.Session()
      # self.web          = self.session.get(url=url).text
      self.web = requests.get(url=url).text
      self.soup = BeautifulSoup(markup=self.web, features='lxml')

   def createMangaFolder(self) -> None:
      if not os.path.exists(self.outputPath):
         os.mkdir(self.outputPath)

   def add(self, a, b) -> int:
      return a + b


mangaScraper = MangaScraper('http://blogtruyen.com/2635/yaiba-remake')

'''
if not os.path.exists(mangaName):
   os.mkdir(mangaName)

for chapterAnchor in soup.find(name='table', class_='table-chapter').findAll(name="a"):
   chapterLink = chapterAnchor['href']
   chapterWebContent = requests.get(url=chapterLink).text
   chapterSoup = BeautifulSoup(markup=chapterWebContent, features='lxml')
   print(f'working on {chapterLink}')

   for mediaItem in chapterSoup.findAll(name='div', class_='mediaItem'):
      imageLink = mediaItem.img['src']
      imageName = imageLink.split('/')[-1]
      imageNameSplited = imageName.split('-')
      imageNameSplited[0], imageNameSplited[1], imageNameSplited[2] = imageNameSplited[1], imageNameSplited[2], \
                                                                      imageNameSplited[0]
      imageName = '-'.join(imageNameSplited)

      with open(file=f'{mangaName}/{imageName}', mode='wb') as writeFile:
         image = requests.get(url=imageLink).content
         print(f'writing {imageName}')
         writeFile.write(image)


def makePdf(pdfFileName, imageNames, folder='./', subFolder='pdf'):
   outputFolder = os.path.join(folder, subFolder)
   if os.path.exists(outputFolder) is False:
      os.mkdir(outputFolder)

   # cover = Image.open(os.path.join(folder, imageNames[0]))
   # width, height = cover.size
   # 735x1200 applies for just this manga
   pdf = FPDF(unit="pt", format=[735, 1200])
   for index, image in enumerate(imageNames):
      pdf.add_page()
      imagePath = os.path.join(folder, image)
      pdf.image(imagePath, 0, 0)

   outputPdfPath = f'{os.path.join(outputFolder, pdfFileName)}.pdf'

   pdf.output(name=outputPdfPath, dest='F')


# folder = ''
folder = ''
pdf = FPDF()

chapter2files = defaultdict(list)
allFiles = [file for file in os.listdir(folder)
            if os.path.isdir(file) is False]
allFiles.sort(key=lambda fileName: (int(fileName.split('-')[1]), int(fileName.split('-')[2])))

for fileName in allFiles:
   fileNameSplited = fileName.split('-')
   chapterName = f'{fileNameSplited[0]}-{fileNameSplited[1]}'
   chapter2files[chapterName].append(fileName)

counter = 0
for chapter, files in chapter2files.items():
   print(f'working on {chapter} {counter / len(chapter2files.items()) * 100:.2f}% completed')
   makePdf(pdfFileName=chapter, imageNames=files, folder=folder)
   counter += 1

'''
