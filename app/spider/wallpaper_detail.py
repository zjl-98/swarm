"""
 Created by zjl on 2020/9/26 22:24
"""
import re
import requests
from lxml import etree

__author__ = 'zjl'


class WallpaperDetail:
    def __init__(self, wid):
        self.detail = []
        detail_url = 'http://desk.zol.com.cn/bizhi/' + wid + '.html'
        # 主页请求头
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        response = requests.get(url=detail_url, headers=header)
        self.desk_lxml = etree.HTML(response.text)

        self.detail = self.detail_spider(self.desk_lxml, wid)

    @staticmethod
    def detail_spider(desk_lxml, wid):
        # 专题标题
        title = desk_lxml.xpath("//h3/a/text()")[0]

        # 正则表达式匹配专题的图片展示数
        img_count_search = re.compile(r"/(\d+)）")
        img_count_xpath = desk_lxml.xpath("//h3/span/text()")[1]
        img_count = re.search(img_count_search, img_count_xpath).group(1)

        # 获取支持的屏幕分辨率
        resolving = ''
        for item in desk_lxml.xpath('//dd[@id="tagfbl"]/a')[0:-1]:
            result = item.xpath('./@id')[0]
            resolving += result + ','

        return {
            'title': title,
            'index': wid,
            'count': int(img_count),
            'resolving': resolving
        }

    def img_spider(self, save_id):
        count = 0
        img_list = []
        for item in self.desk_lxml.xpath('//ul[@id="showImg"]/li'):
            # 小图片链接
            small_img_url = item.xpath('./a/img/@src')[0] if item.xpath('./a/img/@src') else \
                            item.xpath('./a/img/@srcs')[0]
            # 大图片链接下标
            max_index_search = re.compile('_(.*?)_(.*?).html')
            max_index_xpath = self.desk_lxml.xpath('//dd[@id="tagfbl"]/a[1]/@href')[0]
            max_index_1 = re.search(max_index_search, max_index_xpath).group(1)
            max_index_2 = re.search(max_index_search, max_index_xpath).group(2)
            max_index_1 = int(max_index_1) + count
            max_index = '_' + str(max_index_1) + '_' + max_index_2
            count += 1

            info = {
                'wid': int(save_id),
                'min_url': small_img_url,
                'max_index': max_index
            }
            img_list.append(info)

        return img_list


if __name__ == '__main__':
    detail = WallpaperDetail('466_4194_2')
    print(detail.detail)
    result = detail.img_spider(1)
    print(result)


    # http://desk.zol.com.cn/showpic/1366x768_4195_249.html
#     http://xiazai.zol.com.cn/search?wd=%E7%BE%8E%E5%A5%B3&type=5&order=2&page=1
#         try:
#             # 专题标题
#             li_title = li_item.xpath("./a/text()")[0]
#             # 专题独立页面url
#             li_url = li_item.xpath("./a/@href")[0]
#             # 拼接合成专题url
#             desk_url = index_url + li_url
#
#             # 发起专题页面内容请求
#             desk_response = requests.get(url=desk_url, headers=header)
#             # 将请求回来的数据lxml化，方便使用xpath获取数据
#             desk_lxml = etree.HTML(desk_response.text)
#
#             # 正则表达式匹配专题的图片展示数
#             img_index_search = re.compile(r"/(\d+)）")
#             img_index_xpath = desk_lxml.xpath("//h3/span/text()")[1]
#             img_index = re.search(img_index_search, img_index_xpath).group(1)
#
#             # 正则表达式匹配专题url的独特数字
#             img_url_index_search = re.compile(r"_(.*?)_(.*?).html")
#             img_url = index_url + desk_lxml.xpath("//dd[@id='tagfbl']/a[@id='1366x768']/@href")[0]
#             img_url_index_1 = re.search(img_url_index_search, img_url).group(1)
#             img_url_index_2 = re.search(img_url_index_search, img_url).group(2)
#
#             # 调用is_exits判断目录是否存在，不存在则创建目录，存在则不做另外操作
#             is_exits("C:\\Users\\zjl\\Desktop\\资料\\py_learn\\handle_desk.zol\\wallpaper\\" + li_title + "\\")
#
#             # 根据每个专题的图片数定义循环次数
#             for index in range(int(img_index)):
#                 # 根据获取到的内容拼接每个图片独立的页面url
#                 img_install_html_url = 'http://desk.zol.com.cn/showpic/1366x768_' + str(int(img_url_index_1) + index) + '_' + img_url_index_2 + '.html'
#                 # 防止拼接的图片页面url
#                 try:
#                     # 请求每个图片的独立页面
#                     img_install_html_response = requests.get(url=img_install_html_url, headers=header)
#                     # 将请求回来的数据lxml化，方便使用xpath获取数据
#                     img_install_lxml = etree.HTML(img_install_html_response.text)
#                     # 获取到页面中提高的图片下载url
#                     img_install_url = img_install_lxml.xpath("//body/img[1]/@src")[0]
#                     # 请求图片下载url
#                     img_install_url_response = requests.get(url=img_install_url, headers=header)
#                     # 实现图片下载操作，并进行归类
#                     with open('./wallpaper/' + li_title + '/' + str(int(img_url_index_1) + index) + '.jpg', 'wb') as f:
#                         f.write(img_install_url_response.content)
#                     print("排行版专题：" + side_title + "\n")
#                     print("图片专题：" + li_title + "\n")
#                     print("图片url：" + img_install_url + "\n")
#                     print("下载成功~~~~~~~~")
#                     print("---------------------------------------------------------")
#                 except:
#                     print(side_title + "---->" + li_title + "中请求的图片页面url->" + img_install_html_url + "不存在")
#                     print("---------------------------------------------------------")
#                     print("---------------------------------------------------------")
#                     continue
#         except Exception as e:
#             print(e)
