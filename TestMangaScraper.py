import unittest

from MangaScraper import MangaScraper


class TestmangaScraper(unittest.TestCase):
   def setUp(self) -> None:
      url = 'https://blogtruyen.com/2635/yaiba-remake'
      self.mangaScraper = MangaScraper(url)

   def tearDown(self) -> None:
      pass

   def test_add(self):
      self.assertEqual(self.mangaScraper.add(5, 3), 8)


if __name__ == '__main__':
   unittest.main()
