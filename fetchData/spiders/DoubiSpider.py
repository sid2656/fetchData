# coding=utf8
from scrapy.spider import BaseSpider
from scrapy.selector.lxmlsel import HtmlXPathSelector
import DownUtil
import ConfigFileUtil
import MongoDbUtil
from scrapy.http import Request
from distutils.tests.setuptools_build_ext import if_dl
from django.core.paginator import Page
import re

class DoubiSpider(BaseSpider):
    name = 'itlun'
    #scrapy需要的参数
    allowed_domains=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "allowed_domains").split(';')
    start_urls=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "start_urls").split(';')
    
    #自己爬的网站的具体参数
    charSet=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "charSet")
    splitStr=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "splitStr")
    dirPath=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "dirPath")
    pageUrlStart=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "pageUrlStart")
    pageUrlxPath=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "pageUrlxPath")
    imgUrlStart=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "imgUrlStart")
    imgxPath=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "imgxPath")
    axPath=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "axPath")
    titlexPath=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "titlexPath")
    modle=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "modle")
    modle_error=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "modle_error")
    error_url=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "error_url")
    erro_image=ConfigFileUtil.ReadWriteConfFile.getSectionValue(name, "erro_image")
    urls=[]
    finishUrls=[]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        data = {}
        data['key']=response.url
        data['s']=1
        if(MongoDbUtil.MongoDbConnect.count(self.modle,data)==0):
            print '-------------------------------------------',response.url
            self.parseAllA(response.url,hxs)
            try:
                MongoDbUtil.MongoDbConnect.update(self.modle,data)
                self.finishUrls.append(response.url)
            except Exception as e:
                print response.url,":", e
                data = {}
                data['key']=response.url
                data['type']=self.error_url
                data['e']=e
                MongoDbUtil.MongoDbConnect.save(self.modle_error,data)
        data = {}
        data['s']=0
        urls = MongoDbUtil.MongoDbConnect.list(self.modle,data)
        try:
            yield Request(urls[0]['key'], callback=self.parse)
        except Exception as e:
            print "yield Request :", e
            
    def parseAllA(self,url,hxs):
        sites = hxs.xpath(self.axPath)
        items=[]
        for site in sites:
            pagePath = site.select(self.pageUrlxPath).extract()
            title = site.select(self.titlexPath).extract()
            imgPath = site.select(self.imgxPath).extract()
            if len(title)>0 and len(imgPath)>0:
                imgPath = imgPath[0].encode(self.charSet)
                try:
                    title = title[0].encode(self.charSet)
                    srcs = imgPath.split(self.splitStr)
                    imageType = srcs[len(srcs)-1]
                    dr = re.compile(r'<[^>]+>',re.S)
                    title = dr.sub('',title)
                    if imgPath.startswith(self.imgUrlStart):
                            DownUtil.down(imgPath,self.dirPath,title+self.splitStr+imageType)
                            print 'sidlang title:',title
                except Exception as e:
                    print title," title :", e
#                     data = {}
#                     data['type']=self.error_url
#                     data['e']=e
#                     MongoDbUtil.MongoDbConnect.saveError(self.modle_error,data)
                    continue;
            if len(pagePath)>0:
                pagePath = pagePath[0].encode(self.charSet)
                currentUrl = self.start_urls[0]+pagePath
                try:
                    if (pagePath.startswith(self.pageUrlStart) and currentUrl not in self.finishUrls):
                        data = {}
                        data['key']=currentUrl
                        data['s']=0
                        MongoDbUtil.MongoDbConnect.save(self.modle,data)
                        self.finishUrls.append(currentUrl)
                except Exception as e:
                    print data," pagePath :", e
#                     data = {}
#                     data['type']=self.error_url
#                     data['e']=e
#                     MongoDbUtil.MongoDbConnect.saveError(self.modle_error,data)
                    continue;
        return items
                

    
    def parsePage(self,url,hxs):
        sites = hxs.xpath(self.pageUrlxPath).extract()
        items=[]
        for site in sites:
            print site
            src = site.encode(self.charSet)
            currentUrl = self.start_urls[0]+src
            if (src.startswith(self.pageUrlStart) and currentUrl not in self.targetUrls):
                data = {}
                data['key']=currentUrl
                data['s']=0
                try:
                    MongoDbUtil.MongoDbConnect.save(self.modle,data)
                    items.append(currentUrl)
                    self.targetUrls.append(currentUrl)
                except Exception as e:
                    print data,":", e
                    continue;
        return items
    
    
    def parseImg(self,hxs):
        sites = hxs.xpath(self.imgxPath).extract()
        items=[]
        for site in sites:
            src = site.encode(self.charSet)
            if src.startswith(self.imgUrlStart):
                data = {}
                data['key']=src
                data['s']=0
                MongoDbUtil.MongoDbConnect.save('images',data)
                print src #save mongo
                srcs = src.split(self.splitStr)
                name = srcs[len(srcs)-1]
                DownUtil.down(site,self.dirPath,name)