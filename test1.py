#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import os
   
def parser_apks(download_num,_root_url):
    res_parser={}
    page_num=1 #设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    while download_num:
         #获取排行榜页面的网页内容
        wbdata = requests.get("http://app.mi.com/topList?page="+str(page_num)).text
        print("开始爬取第"+str(page_num)+"页")
        #解析页面内容获取 应用下载的 界面连接
        soup=BeautifulSoup(wbdata,"html.parser")
        links=soup.body.contents[5].find_all("a",href=re.compile("/details?"), class_ ="", alt="")
        for link in links:
            detail_link=urllib.parse.urljoin(_root_url, str(link["href"]))#拼接 结果为http://app.mi.com/details?id=com.xunmeng.pinduoduo
            package_name=detail_link.split("=")[1]
            #在下载页面中获取 apk下载的地址
            download_page=requests.get(detail_link).text
            soup1=BeautifulSoup(download_page,"html.parser")
            download_link=soup1.find(class_="download")["href"]
            download_url=urllib.parse.urljoin(_root_url, str(download_link))
            #解析后会有重复的结果，下面通过判断去重
            if package_name not in res_parser.keys():
                res_parser[package_name]=download_url
                download_num=download_num-1
            if download_num==0:
                break
        if download_num >0:
            page_num=page_num+1   
    print("爬取apk数量为: "+str(len(res_parser)))
    return res_parser 

def craw_apks(download_num,root_url, save_path="/Users/sweetdream/Desktop/hello/"):
    res_dic=parser_apks(download_num,root_url)
    print(res_dic)
    for apk in res_dic.keys():
        print("正在下载应用: "+apk)
        urllib.request.urlretrieve(res_dic[apk],save_path+apk+".apk")
        print("下载完成")
    print("%d个应用下载完成" % download_num)


if __name__=="__main__":
    """root_url = str(input("请输入下载网址："))
                download_num = input('请输入下载数目:')
                if root_url or download_num==0:
                    pass
                else:
                    download_num = 2
                    root_url = "http://app.mi.com"
                         
                craw_apks(download_num,root_url)"""

    os.system("git add hello.py")
    os.system("git commit -m 'test os.system'")
    os.system("git push origin master")