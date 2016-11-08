# -*- coding:UTF-8 -*-
import urllib
import re
import xml.dom.minidom as xml_parse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CitySearch:
    @staticmethod
    def getHtml(url):
        fo = open("foo.txt", "wb")
        page = urllib.urlopen(url)
        html = page.read()
        exp1 = re.compile("(?isu)<tr[^>]*>(.*?)</tr>")
        exp2 = re.compile("(?isu)<td[^>]*>(.*?)</td>")
        for row in exp1.findall(html):
            for col in exp2.findall(row):
                fo.write(col)
                fo.write(u'|')
            fo.write(u'\n')
        fo.close()
        return html

    @staticmethod
    def get_city_code(city):
        fo = open("foo.txt","r")
        for line in fo:
            items = line.split("|")
            if city in items[3]:
                return items[0]
        return None


if __name__ == '__main__':
    html = CitySearch.get_city_code(u'上海')
