from hanlp_restful import HanLPClient
# auth不填则匿名，zh中文，mul多语种
HanLP = HanLPClient('https://www.hanlp.com/api', auth='MjA5OEBiYnMuaGFubHAuY29tOlpRcktyN3A4R2ZDM3FGQ1g=', language='zh')

txt = open('static/book.txt', 'r', encoding='gbk')
Str = txt.readline()
(HanLP.parse(Str, tasks='ner/pku')).pretty_print()
# pku词性划分
# doc = (HanLP.parse(Str, tasks='pos/ontonotes'))

# fo = open('static/book_ontonotes.txt', 'w+', encoding='gbk')
# fo.write(str(doc))
# fo.close()

