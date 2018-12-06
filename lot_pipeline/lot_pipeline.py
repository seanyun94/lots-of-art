import os, sys
import luigi
from bs4 import BeautifulSoup
from selenium import webdriver

class PullLotURLsFromSale(luigi.Task):

	sale_url = luigi.Parameter()

	def requires(self):
		return []

	def output(self):
		if not os.path.exists('data/'):
			os.mkdir('data/')

		sales_url_split = self.sale_url.strip().split('/')
		sale_name = sale_url_split[3][:-5]
		return luigi.LocalTarget("data/{}_lot_urls.csv".format(sale_name))

	def run(self):
		driver = webdriver.Chrome()
		driver.get(sale_url)

		load_all_link = driver.find_element_by_id('loadAllUpcomingPast')
		load_all_link.click()

		soup_lots = BeautifulSoup(driver.page_source)

		lots_container = soup_lot.find(id='ResultContainer')
		with open(self.output(), 'w') as out_file:
			for li in lots_container.findall('li'):
				lot_href = li.find('a', class='cta-image')['href']
				info_container = li.find('span', class='infoContainer')
				lot_no = info_container.p.text.strip().split()[1]
				print >> out_file, lot_no, lot_href


class CacheLotHTMLFromUrl(luigi.Task):
	''' Pull the HTML doc from a url to lot information and cache it
    '''
    sale_url = luigi.Parameter()

    def output(self):
    	sales_url_split = self.lot_urls.strip().split('/')
		self.sale_name = sale_url_split[3].split('.')[0]
    	return luigi.LocalTarget("data/html/flag_{}".format(sale_name))

    def requires():
    	return PullLotURLsFromSale(self.sale_url)

    def run(self):
    	driver = webdriver.Chrome()
    	driver.get(lot_url)

    	if not os.path.exists('data/html/'):
    		os.mkdir('data/html')

    	elif if not os.path.exists("data/html/{}/".format(self.sale_name)):
    		os.mkdir("data/html/{}/".format(self.sale_name))

    	with open("data/{}_lot_urls.csv".format(self.sale_name), 'r') as f:
    		for line in f:
    			line_split = line.strip().split(',')
    			soup = BeautifulSoup(line_split[1])
    			with open("data/html/{0}/lot_{1}.html".format(self.sale_name, line_split[0]), 'w') as html_file:
    				html_file.write(str(soup))

    	with open(self.output(), 'w') as flag_file:
        	flag_file.write(' ')

class PullLotDataFromHtml(luigi.Task):

	lot_no = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget("data/{}_lot_info.csv".format(sale_name))

	def requires(self):
		#Get sale names from lot_urls, return Cache task as requirement
		return [CacheLotHTMLFromUrl(sale_name) for sale_name in sales]
	def run(self):
		pass




if __name__ = "__main__":
	luigi.run()