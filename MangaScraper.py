# region Import
from typing import List, Tuple, Dict

from bs4 import BeautifulSoup
import requests
from collections import defaultdict, Counter
import os
from fpdf import FPDF
from PIL import Image
import cfscrape


# endregion


class MangaScraper:
   def __init__(self, url: str):
      self.source = 'https://blogtruyen.com'
      self.url = url
      self.mangaName = url.split("/")[-1]
      self.subFolder = 'manga'
      self.outputPath = os.path.join(os.getcwd(), self.subFolder, self.mangaName)
      self.chapterLink2chapterName: Dict[str, str] = defaultdict(str)
      self.chapter2image: Dict[Tuple[str, str], List[Tuple[str, str]]] = defaultdict(list)
      self.session = requests.Session()
      # self.scraper = cfscrape.create_scraper(sess=self.session)

   def createMangaFolder(self) -> None:
      if not os.path.exists(self.outputPath):
         os.mkdir(self.outputPath)

   def scrapeChapters(self) -> Dict[str, str]:
      web = self.session.get(url=self.url).text
      soup = BeautifulSoup(markup=web, features='lxml')
      spanTags = soup.find(name='div', attrs={'class': 'list-wrap'}).findAll(name='span', attrs={'class': 'title'})
      for index, spanTag in enumerate(spanTags):
         href = spanTag.find(name='a')['href']
         chapterLink = f'{self.source}{href}'
         # chapterLinkSplited = chapterLink.split("-")
         # chapterName = f'{chapterLinkSplited[-2]}-{chapterLinkSplited[-1]}'
         chapterName = f'chap-{len(spanTags) - index}'
         self.chapterLink2chapterName[chapterLink] = chapterName
      return self.chapterLink2chapterName

   def scrapeImages(self) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
      for chapterLink, chapterName in self.chapterLink2chapterName.items():
         # if chapterName == 'chap-64' or chapterName == 'chap-63':
         print(f'working on {chapterName}')
         chapterWebContent = self.session.get(url=chapterLink).text
         chapterSoup = BeautifulSoup(markup=chapterWebContent, features='lxml')

         for index, imgTag in enumerate(chapterSoup.find(name='article', attrs={'id': 'content'}).findAll(name="img")):
            imageLink = imgTag['src']
            imageName = f'{chapterName}-{index + 1}-{self.mangaName}.jpg'
            self.chapter2image[(chapterLink, chapterName)].append((imageLink, imageName))
      return self.chapter2image

   def saveImages(self) -> None:
      for key, value in self.chapter2image.items():
         chapterLink, chapterName = key
         for imageLink, imageName in value:
            with open(file=os.path.join(self.outputPath, imageName), mode='wb') as writeFile:
               image = self.session.get(url=imageLink).content
               # print(chapterLink, imageLink, imageName)
               # print(image)
               print(f'writing {imageName}')
               writeFile.write(image)

   def createPdf(self, pdfFileName, imagesNames) -> None:
      subFolder = 'pdf'
      outputFolder = os.path.join(os.getcwd(), subFolder)
      if os.path.exists(outputFolder) is False:
         os.mkdir(outputFolder)

      widths = []
      heights = []
      for index, imageName in enumerate(imagesNames):
         imagePath = os.path.join(os.getcwd(), imageName)
         image = Image.open(imagePath)
         width, height = image.size
         widths.append(width)
         heights.append(height)
      widths = Counter(widths)
      heights = Counter(heights)

      mostCommonWidth, _ = widths.most_common(1)[0]
      mostCommonHeight, _ = heights.most_common(1)[0]

      pdf = FPDF(unit="pt", format=[mostCommonWidth, mostCommonHeight])
      for index, imageName in enumerate(imagesNames):
         print(f'working on {imageName}')
         pdf.add_page()
         imagePath = os.path.join(os.getcwd(), imageName)
         page = Image.open(imagePath)

         width, height = page.size
         pdf.image(imagePath, x=(mostCommonWidth - width) / 2, y=(mostCommonHeight - height) / 2)

      outputPdfPath = f'{os.path.join(outputFolder, pdfFileName)}.pdf'
      pdf.output(name=outputPdfPath, dest='F')

   def createPdfs(self) -> None:
      os.chdir(os.path.join(os.getcwd(), self.subFolder, self.mangaName))
      chapterName2imageName: Dict[str, List[str]] = defaultdict(list)
      allFiles = [file
                  for file in os.listdir(os.getcwd())
                  if os.path.isdir(file) is False]
      allFiles.sort(key=lambda fileName: (int(fileName.split('-')[1]), int(fileName.split('-')[2])))

      chapter2image: Dict[str, List[str]] = defaultdict(list)
      for fileName in allFiles:
         fileNameSplited = fileName.split('-')
         chapterName = f'{fileNameSplited[0]}-{fileNameSplited[1]}'
         chapter2image[chapterName].append(fileName)
      for chapterName, imagesNames in chapter2image.items():
         self.createPdf(pdfFileName=chapterName, imagesNames=imagesNames)

   def start(self) -> None:
      self.createMangaFolder()
      self.scrapeChapters()
      self.scrapeImages()
      self.saveImages()
      self.createPdfs()


if __name__ == '__main__':
   mangaScraper = MangaScraper('https://blogtruyen.com/2635/yaiba-remake')
   mangaScraper.start()
