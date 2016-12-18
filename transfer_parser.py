from selenium import webdriver
import sys,os,time
reload(sys)
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def transfer_parse(transfer_url,driver):
    driver.get(transfer_url)
    time.sleep(1)
    transitems = driver.find_elements_by_xpath("//*[@id='content']/div[1]/div[2]/ul")
    for transitem in transitems:
        print transitem.text


class HouseParser(object):
    def __init__(self, house_urls, driver):
        self.total_house = 0
        self.house_nums = []
        for house_url in house_urls:
            driver.get(house_url)
            time.sleep(1)
            self.house_nums.append(self.extract_house_num(driver))

        if len(self.house_nums) > 0:
            self.total_house = sum(self.house_nums)


    def extract_house_num(self,driver):
        house_elements = driver.find_elements_by_xpath("//*[@id='blg_dtl']/tbody/tr[3]/td/table/tbody/tr/td")
        if len(house_elements) > 0:
            house_str = house_elements[-1]
            m = re.findall(r'(\w*[0-9]+)\w*',house_str.text.replace(',',''))
            if len(m) > 0:
                num_str = m[0]
                return int(num_str)
            else:
                return -1

if __name__ == '__main__':
    driver = webdriver.Chrome()

    transfer_parse("http://www.soccernews.com/soccer-transfers/german-bundesliga-transfers/",driver)