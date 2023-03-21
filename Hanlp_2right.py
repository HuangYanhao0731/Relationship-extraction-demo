from hanlp_restful import HanLPClient
# auth不填则匿名，zh中文，mul多语种
HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
txt = open('static/book.txt', 'r', encoding='gbk')
Str = txt.readline()
HanLP.grammatical_error_correction([Str])