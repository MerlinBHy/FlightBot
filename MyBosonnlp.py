# -*- coding:UTF-8 -*-

from __future__ import print_function, unicode_literals
import json
import datetime
import requests
from bosonnlp import BosonNLP
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


class MyBosonnlp:
    appkey = "K08ZGK-o.10455.nEdxL3yYLAWC"
    nlp = BosonNLP(appkey)
    '''
    命名实体识别接口
    ner(contents, sensitivity=None, segmented=False)
    paramters：contents (string or sequence of string) – 需要做命名实体识别的文本或者文本序列。
    sensitivity (int 默认为 3) – 准确率与召回率之间的平衡， 设置成 1 能找到更多的实体，设置成 5 能以更高的精度寻找实体。
    segmented (boolean 默认为 False) – 输入是否为分词结果

    JSON 格式的实体识别引擎返回的结果。

    key	type	说明
    word	list	分词结果
    tag	list	词性标注结果
    entity	list	命名实体结果
    其中命名实体结果为一个三元组： (s, t, entity_type) ，表示 word[s:t] 的内容为类型 entity_type 的实体。
    '''

    def get_ner(self, text):
        result = self.nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            yield (''.join(words[entity[0]:entity[1]]), entity[2])

    '''
    依存语法分析
    '''

    def get_depparser(self, text):
        result = self.nlp.depparser(text)
        return result

    '''
    关键词提取
    '''

    def get_keywords(self, text, k):
        result = self.nlp.extract_keywords(text, top_k=k)
        return result

    '''
    分词与词性标注
    JSON 格式的分词与词性标注结果。
    Parameters:
    contents (string or sequence of string) – 需要做分词与词性标注的文本或者文本序列。
    space_mode (int（整型）, 0-3有效) – 空格保留选项
    oov_level (int（整型）, 0-4有效) – 枚举强度选项
    t2s (int（整型）, 0-1有效) – 繁简转换选项，繁转简或不转换
    special_char_conv (int（整型）, 0-1有效) – 特殊字符转化选项，针对回车、Tab等特殊字符转化或者不转
    key	type	说明
    word	list	分词结果
    tag	list	词性标注结果
    '''
    def get_alltags(self,text):
        result = self.nlp.tag(text,space_mode=0, oov_level=3, t2s=0, special_char_conv=0)
        for d in result:
            yield (' '.join(['%s/%s' % it for it in zip(d['word'], d['tag'])]))

    '''
    时间转换
    时间格式类型	type标记	数据格式
    说明
    时间点(timestamp)	timestamp	string
    时间点，ISO8601格式的时间
    字符串
    时间量(timedelta)	timedelta	string
    时间量，格式为”x
    day,HH:MM:SS”或”HH:MM:SS”
    的字符串
    时间区间(timespan)	timespan_0	list
    表示时间点组成的时间区间结
    果，格式为[timestamp,
    timestamp]表示时间区间的起
    始和结束时间
    时间区间(timespan)	timespan_1	list
    时间区间结果，格式为
    [timedelta, timedelta]，表
    示时间区间的起始和结束时间
    N/A	“”	string
    不能识别，返回空字符串

    '''
    def get_time(self,time):
        return self.nlp.convert_time(time,datetime.datetime.today())

if __name__ == '__main__':
    for item in MyBosonnlp().get_ner("上海到北京15年11月2日"):
        print(item[0].encode("utf-8"))
        print(item[1].encode("utf-8"))

    result = MyBosonnlp().nlp.convert_time(
        "15年11月23日",
        datetime.datetime.today())
    #result = datetime.datetime.strptime(result["timestamp"], '%Y-%m-%d %H:%M:%S')


    print(result)