import os, sys
import luigi
from bs4 import BeautifulSoup
from selenium import webdriver

class PullLotURLsFromSale(luigi.Task):

	sale_url = luigi.Parameter()

	def requires(self):
		return []

	def output(self):
		sales_url_split = self.sale_url.strip().split('/')
		sale_name = sale_url_split[3][:-5]
		return luigi.LocalTarget("data/{}/lot_urls.csv".format(sale_name))

	def run(self):
		driver = webdriver.Chrome()
		driver.implicily_wait(30)
		driver.get(sale_url)

		load_all_link = driver.find_element_by_id('loadAllUpcomingPast')
		load_all_link.click()

		soup_lots = BeautifulSoup(driver.page_source)

		lots_container = soup_lot.find(id='ResultContainer')
		for li in lots_container.findall('li'):
			lot_href = li.find('a', class='cta-image').href
			info_container = li.find('span', class='infoContainer')
			lot_no = info_container.p.text.strip().split()[1]
			print >> out_file, lot_no, lot_href


class CacheLotHTMLFromUrl(luigi.Task):
	''' Pull the HTML doc from a url to lot information and cache it
    '''
    sale_url = luigi.Parameter()
    lot_urls = luigi.Parameter()

    def output(self):
    	sales_url_split = self.sale_url.strip().split('/')
		sale_name = sale_url_split[3][:-5]
    	return luigi.LocalTarget("data/html/".format(sale_name))

    def requires():
    	pass 

    def run(self):
    	pass

class PullLotDataFromHtml(luigi.Task):

	sale_url = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget("data/{}_lot_info.csv".format(sale_name))

	def requires(self):
		return [CacheLotHTMLFromUrl(sale_url) for sale_url in 


if __name__ = "__main__":
	luigi.run()