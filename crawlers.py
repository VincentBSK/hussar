__author__ = 'asus'

import urllib2
import socket
from browser_base import BrowserBase
from config import  EPL_URL,SA_URL,LL_URL,EC_URL,DL_URl,GAMELOG_TYPE,CHAT_TYPE

def MatchCrawler(league_idx,start_idx,type_idx):
    if league_idx == 1:
        main_url = LL_URL
    elif league_idx == 3:
        main_url = SA_URL
    elif league_idx == 4:
        main_url = EC_URL
    elif league_idx == 2:
        main_url = DL_URl
    else:
        main_url = EPL_URL

    if type_idx == 1:
        mid_url = CHAT_TYPE
        doc_name = 'chat_results/'
    else:
        mid_url = GAMELOG_TYPE
        doc_name = 'match_results/'

    current_idx = start_idx
    splider=BrowserBase()
    while(True):
        print current_idx
        final_url = main_url + mid_url + str(current_idx)
        try:
            f = splider.openurl(final_url)
            data = f.read()
            with open(doc_name + str(current_idx) + '.xml', "w") as code:
                code.write(data)
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            break
        print current_idx
        current_idx += 1

if __name__ == '__main__':
    # MatchCrawler(0,13114,0)
    MatchCrawler(4,7209,0)
    # MatchCrawler(3,31158,0)
    # MatchCrawler(1,30166,0)



