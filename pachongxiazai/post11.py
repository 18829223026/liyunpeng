from urllib import request,parse
from chardet import detect
from fake_useragent import UserAgent
import gzip,hashlib,time,random
md5=hashlib.md5()
url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
kwd=input('请输入您要翻译的字符串:')
e='fanyideskweb'
t=int(time.time()*1000)+random.randint(1,100)
sgin=e+kwd+str(t)+'6x(ZHw]mwzX#u0V7@yfwK'
md5.update(sgin.encode('utf8'))
sgin=md5.hexdigest()
data={
      'action':'FY_BY_REALTIME',
      'client':e,
      'doctype':'json',
      'from':'	AUTO',
      'i':kwd,
      'keyfrom':'fanyi.web',
      'salt	':str(t),
      'sign	':sgin,
      'smartresult':'dict',
      'to':'AUTO',
      'typoResult':'false',
      'version':'2.1',
      }
data=parse.urlencode(data).encode('utf8')
headers={
      'Accept':'application/json, text/javascript, */*; q=0.01',
      'Accept-Encoding':'gzip, deflate',
      'Accept-Language':'zh-CN,zh;q=0.9',
      'Connection':'keep-alive',
      'Content-Length':'202',
      'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie':'OUTFOX_SEARCH_USER_ID=373083181@113.140.126.191; OUTFOX_SEARCH_USER_ID_NCOO=790790376.1356496; P_INFO=m18829223026_3@163.com|1523437318|0|other|00&99|sxi&1523433002&other#sxi&610600#10#0#0|188026&1|mail163&unireg|18829223026@163.com; _ntes_nnid=a46b6d0a98f8160f7f59a62fa3120c8e,1526917943128; fanyi-ad-id=48707; fanyi-ad-closed=1; JSESSIONID=aaamq90UXbSmTghKSRXww; ___rl__test__cookies=1536284358747',
      'Host':'fanyi.youdao.com',
      'Origin':'http://fanyi.youdao.com',
      'Referer':'http://fanyi.youdao.com/?keyfrom=fanyi.logo',
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'X-Requested-With':'XMLHttpRequest',
}
req=request.Request(url=url,data=data)
rep=request.urlopen(req)
data=rep.read()
html=data.decode(detect(data)['encoding'],errors='ignore')
print(html)
