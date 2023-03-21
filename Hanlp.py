from hanlp_restful import HanLPClient

# auth不填则匿名，zh中文，mul多语种
HanLP = HanLPClient('https://www.hanlp.com/api', auth='MjA5OEBiYnMuaGFubHAuY29tOlpRcktyN3A4R2ZDM3FGQ1g=', language='zh')
txt = open('static/book1.txt', 'r', encoding='gbk')
Str = txt.readline()
# doc = Document()
# HanLP.parse(Str, tasks='ner/pku').pretty_print()

# 语义角色标注
doc = HanLP.parse(Str, tasks=['srl'])

# fo = open('static/book1_demo.txt', 'w+', encoding='gbk')
# # doc.pretty_print()
# fo.write(str(doc))
# fo.close()
print(doc)

for i, pas in enumerate(doc['srl'][0]):
    print(f'第{i+1}个谓词论元结构：')
    for form, role, begin, end in pas:
        print(f'{form} = {role} at [{begin}, {end})')

