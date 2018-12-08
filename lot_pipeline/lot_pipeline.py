import os, sys, csv
from urllib import request
import luigi
from bs4 import BeautifulSoup
from selenium import webdriver
from lot_data import LotData

class PullLotURLsFromSale(luigi.Task):

    sale_url = luigi.Parameter()

    def requires(self):
        return []

    def output(self):
        if not os.path.exists('data/'):
            os.mkdir('data/')

        sale_url_split = self.sale_url.strip().split('/')

        # Sale url ends in .aspx
        sale_name = sale_url_split[3][:-5]
        return luigi.LocalTarget("data/{}_lot_urls.csv".format(sale_name))

    def run(self):
        driver = webdriver.Chrome()
        driver.get(self.sale_url)

        load_all_link = driver.find_element_by_class_name('load-all')
        load_all_link.click()

        soup_lot = BeautifulSoup(driver.page_source)

        lots_container = soup_lot.find(id='ResultContainer')

        driver.close()

        with self.output().open('w') as out_file:
            for li in lots_container.children:
                if li == '\n':
                    continue
                lot_href = li.find('a', {'class':'cta-image'})['href']
                info_container = li.find('span', {'class':'infoContainer'})
                lot_no = info_container.p.text.strip().split()[1]
                out_file.write("{0}, {1}\n".format(lot_no, lot_href))

class CacheLotHTMLFromUrl(luigi.Task):
    ''' Pull the HTML doc from a url to lot information and cache it
    '''
    sale_url = luigi.Parameter()

    def output(self):
        sale_url_split = self.sale_url.strip().split('/')
        self.sale_name = sale_url_split[3].split('.')[0]
        return luigi.LocalTarget("data/html/flag_{}".format(self.sale_name))

    def requires(self):
        return PullLotURLsFromSale(self.sale_url)

    def run(self):

        if not os.path.exists('data/html/'):
            os.mkdir('data/html')

        elif not os.path.exists("data/html/{}/".format(self.sale_name)):
            os.mkdir("data/html/{}/".format(self.sale_name))

        with open("data/{}_lot_urls.csv".format(self.sale_name), 'r') as f:
            for line in f:
                line_split = line.strip().split(',')
                lot_url = line_split[1]
        
                response = request.urlopen(lot_url)
                lot_html = response.read()

                soup = BeautifulSoup(lot_html)
                with open("data/html/{0}/lot_{1}.html".format(self.sale_name, line_split[0]), 'w') as html_file:
                    html_file.write(soup.find(id = "MainContent").prettify())

        with self.output().open('w') as flag_file:
            flag_file.write('Finished writing html files!')

class PullLotDataFromHtml(luigi.Task):

    sale_url = luigi.Parameter()

    def output(self):
        sale_url_split = self.sale_url.strip().split('/')
        self.sale_name = sale_url_split[3].split('.')[0]
        return luigi.LocalTarget("data/{}_lot_info.csv".format(self.sale_name))

    def requires(self):
        #Get sale names from lot_urls, return Cache task as requirement
        return CacheLotHTMLFromUrl(self.sale_url)
    def run(self):
        lot_html_dir = "data/html/{}/".format(self.sale_name)
        with self.output().open('w') as lot_csv:
            writer = csv.writer(lot_csv)
            for lot_html in os.listdir(lot_html_dir):
                    with open(lot_html_dir + lot_html, 'r') as html_file:
                        lot_info = LotData(html_file)
                        writer.writerow(lot_info.lot_data_as_list())

if __name__ == "__main__":
    luigi.build([PullLotDataFromHtml(sale_url="https://www.christies.com/impressionist-and-modern-art-27255.aspx")], local_scheduler=True)
