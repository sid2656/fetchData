# coding=utf8
import urllib2

def down(url,dir,name):
#         path = "D:\\Download"
#         url = "http://pic2.sc.chinaz.com/files/pic/pic9/201309/apic520.jpg"
#         name ="D:\\download\\1.jpg"
#保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
#         conn = urllib.request.urlopen(url)
    domain=urllib2.Request(url)
#     domain.add_header('Host',host)
#     domain.add_header('User-agent', user_agents[r])
#     domain.add_header('Connection','keep-alive')
#     domain.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
#     domain.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    conn = urllib2.urlopen(domain)
    f = open(dir+name,'wb')
    f.write(conn.read())
    f.close()
