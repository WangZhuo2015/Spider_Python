__author__ = 'Rachin'

import requests
from bs4 import  BeautifulSoup
import csv
import time
import random
import urllib.request

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from io import StringIO

def get_html(page_number ,ip):
    header = {
        'Host':"www.pss-system.gov.cn",
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        'Accept':"text/html, */*",
        'Accept-Encoding':"gzip, deflate"

    }

    form = {
        'resultPagination.limit':"10",
        'resultPagination.sumLimit':"10",
        'resultPagination.start':str((page_number-1)*10),
        'resultPagination.totalCount':"285894",
        'searchCondition.searchType':"Sino_foreign",
        'searchCondition.dbId': "",
        'searchCondition.strategy':"",
        'searchCondition.literatureSF':"",
        # 'resultPagination.sumLimit':"10,10,10,10,10,10,10,10,10,10,10,10,10",
        'searchCondition.searchExp':"厂",
        'wee.bizlog.modulelevel':"0200101",
        'searchCondition.executableSearchExp':"VDB:(PAVIEW='厂')",
        'searchCondition.searchKeywords':"",
        'searchCondition.searchKeywords':"[厂][+]{0,}"
    }
    url = 'http://www.pss-system.gov.cn/sipopublicsearch/search/showSearchResult-startWa.shtml'
    timeout = random.choice(range(20,40))
    session = requests.session()
    ip = ip.replace('\r','')
    proxies = {
        'http':ip,
        'https':ip
    }
    session.proxies = proxies
    html = session.post(url,data=form,headers=header,timeout=timeout)
    #html = requests.post(url,data=form,headers=header,timeout=timeout)
    #print(html.text)
    return html.text

def get_data(html_text):
    result = []
    soup = BeautifulSoup(html_text)
    for i in range(0,10):
        temp = []
        id = "sameApDiv" + str(i)
        div = soup.find('div',{'id': str(id)})
        if i > 0:
            try:
                td = div.find_all('td',{'valign': "top"})
            except:
                continue
        else:
            td = div.find_all('td',{'valign': "top"})
        application_number = application_date = open_date = name_of_invention = IPC_classification_number = ' '
        applicant = inventor = priority_number = priority_day = agent = agency = appearance_design_of_Luojianuo_classification_number = ' '
        for j in td:
            try:
                contents = j.contents
                if (contents[1].next == "申请号­: "):
                    application_number = j.contents[2]
                elif(contents[1].next == "申请日: "):
                    application_date = j.contents[2]
                elif(contents[1].next == "公开（公告）号­: "):
                    open_number = j.contents[2]
                elif(contents[1].next == "公开（公告）日: "):
                    open_date = j.contents[2]
                elif(contents[1].next == "发明名称: "):
                    name_of_invention = j.contents[2]
                elif(contents[1].next == "IPC分类号: "):
                   IPC_classification_number = j.contents[2]
                elif(contents[1].next == "申请（专利权）人: "):
                    applicant = j.contents[2]
                elif(contents[1].next == "发明人: "):
                    inventor = j.contents[2]
                elif(contents[1].next == "优先权号: "):
                    priority_number = j.contents[2]
                elif(contents[1].next == "优先权日: "):
                    priority_day = j.contents[2]
                elif(contents[1].next == "代理人: "):
                    agent = j.contents[2]
                elif(contents[1].next == "代理机构: "):
                    agency = j.contents[2]
                elif(contents[1].next == "外观设计珞珈诺分类号: "):
                    appearance_design_of_Luojianuo_classification_number = j.contents[2]
                else:
                    continue
            except:
                continue
        temp.extend([application_number,application_date,open_number,open_date,name_of_invention,IPC_classification_number,applicant,inventor,priority_number,priority_day,appearance_design_of_Luojianuo_classification_number,agent,agency])
        #print(temp)
        result.append(temp)
    return result


def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


def write_title(name):
    file_name = name
    with open(file_name, 'a', errors='ignore',newline='') as f:
        f_csv =csv.writer(f)
        f_csv.writerow(["申请号","申请日",'公开（公告）号','公开（公告）日','发明名称','IPC分类号','申请（专利权）人','发明人','优先权号','优先权日','外观设计珞珈诺分类号','代理人','代理机构'])

def get_ips():
    with open('ip.txt', 'r', errors='ignore', newline='') as f:
        ips = f.read()
    return ips


def write_in_text_daili(data):
    with open('ip.txt','a',newline='') as f:
        f.write(data)
        f.write('\r\n')

def get_html_daili():
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }

    res = requests.get('http://www.xicidaili.com/', headers = header)
    #res = requests.get('http://www.xicidaili.com/nn/1', headers = header)
    # print(res.text)

    bs = BeautifulSoup(res.text)
    links = bs.find_all('tr',{'class':'odd'})
    for link in links:
        tds = link.find_all('td')
        td1 = tds[1]
        td2 = tds[2]
        ip = td1.string+':'+td2.string
        # print(ip)
        write_in_text_daili(ip)

def read_txt_daili():
    ips = []
    with open('ip.txt') as f:
        lines = f.readlines()
        for line in lines:
            ip = line.replace('\n','')
            ips.append(ip)
    return ips



if __name__ == '__main__':
    #write_title("专利信息.csv")
    ips_text = get_ips()
    ips = ips_text.split('\n')
    i = random.choice(range(0,ips.__len__()))

    # with open('text.html','r') as f:
    #     html = f.read()
    # result = get_data(html)
    # print(result)

    #for page_number in range(12001,15001):
    for page_number in range(14777,15001):
        print("写入第",page_number,"页数据")
        success = False
        while not success:
            try:
                t = random.choice(range(15,20))
                time.sleep(0.1 * t)
                html_text = get_html(page_number,ips[i])
                result = get_data(html_text)
                write_data(result,"专利信息.csv")
                print("第",page_number,"页写入成功")
                success = True
                #i = random.choice(range(0,ips.__len__()))
            except:
                #if i < ips.__len__()-1:
                if ips.__len__() > 1:
                    ip = ips[i].replace('\r','')
                    print('ip:',ip,'失效')
                    ips.pop(i)
                    i = random.choice(range(0,ips.__len__()))
                else:
                    try:
                        get_html_daili()
                        ips_daili = read_txt_daili()
                        i = 0
                        while i <len(ips_daili):
                            print(ips_daili[i])
                            i += 1
                        ips_text = get_ips()
                        ips = ips_text.split('\n')
                        i = 0
                    except:
                        print("第",page_number,"页写入失败")
                        exit()