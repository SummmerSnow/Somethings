import re
import urllib.parse
import urllib.request
from Py4Js import Py4Js
import time
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import re


def open_url(url):    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)    
    data = response.read().decode('utf-8')    
    return data    


def translate(content, tk):
    if len(content) > 4891:    
        print("翻译的长度超过限制！！！")    
        return     
        
    content = urllib.parse.quote(content)

    # English -》 Chinese
    # url = "http://translate.google.cn/translate_a/single?client=t" \
    # "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
    # "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
    # "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)

    # Chinese -》 English
    url = "http://translate.google.cn/translate_a/t?client=t&" \
          "sl=zh-CN&tl=en&hl=zh-CN&v=1.0&source=is&tk=%s&q=%s" % (tk, content)

    result = open_url(url)
    if "\\\"" in result:
        return result.replace("\\\"", "")
    else:
        return result.replace("\"", "")


def translate_google():
    js = Py4Js()     # seems google encode the send context in someway, sp py4js is a js to parse the secret
    while 1:    
        content = input("输入待翻译内容：")
        if content == 'q!':    
            break
        tk = js.getTk(content)
        print(translate(content, tk))


# read from and write to file
def translation_bing_result(file_name):
    c_clean = open("D:\data\ec.txt.test.plain.bing.translation.result.txt", "a", encoding="utf8")
    index = 0
    with open(file_name, encoding='utf8') as lines:
        for line in lines:
            try:
                temp_result = translation_bing(line)
                temp_result = temp_result.replace("\n", "")
                print(temp_result)
                index += 1
                c_clean.write(temp_result + '\n')
            except:
                index += 1
                print(index)
                continue


def translation_bing(content):

    translator_api = "https://www.bing.com/translator/api/Translate/TranslateArray?from=en&to=zh-CHS"
    custom_headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.bing.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Referer': 'https://www.bing.com/translator',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',

    }
    cookies = {}
    cookies[
        "Cookie"] = "srcLang=zh-CHS; destLang=en; smru_list=zh-CHS; " \
                    "dmru_list=af%2Cen; destDia=en-US; sourceDia=zh-CN; " \
                    "mtstkn=xcx8q3pT5A58A6lkzTIoJcZ0HJ3OZNakxZbwWwaIvP87s78Z4uPe0QDAT4AY8bxV; " \
                    "SRCHUID=V=2&GUID=4EDEFC3483F448D193C7A87E55EE3EED; " \
                    "MUIDB=0B50BE23F06E648A1946B41DF18F6551;" \
                    " MicrosoftApplicationsTelemetryDeviceId=f5751594-c3b1-acdd-87d3-b69e63c0b265; " \
                    "MicrosoftApplicationsTelemetryFirstLaunchTime=1489402862314; " \
                    "srcLang=-; destLang=en; smru_list=; dmru_list=af%2Cen; " \
                    "sourceDia=zh-CN; destDia=en-US; MUID=0B50BE23F06E648A1946B41DF18F6551; " \
                    "SRCHD=AF=EDGEAR; SRCHUSR=DOB=20170307; " \
                    "BFB=E=170406&V=Kuj4BmuqueNsEi9etUJfM6svX/vqdn6lp9n4LeaA+uw=; " \
                    "BFBUSR=BAWV=1&BAWSSO=1; SRCHHPGUSR=CW=1107&CH=850&DPR=1.100000023841858&UTC=480;" \
                    " RwBf=s=70&o=16; TID=ARCuNog7l7LEVnM5WF0G5AavJqENsRphgwJZhV4uu0jUKPNqunNHmodpuwTweplC8kY+ybHnK0EtwBvvPrd149Yo; _" \
                    "EDGE_S=SID=1CEC84BE78D4611B036E8EF8793560FD; _" \
                    "SS=SID=1CEC84BE78D4611B036E8EF8793560FD&HV=1489548202&bIm=915934; " \
                    "WLS=C=&N=&TS=63625145372"

    payload = [{"id": 655101193, "text": content}]
    translator = requests.post(url=translator_api, data=json.dumps(payload),
                               cookies=cookies, headers=custom_headers, verify=False)
    translator.encoding = "utf-8"
    html = json.loads(translator.text)
    return html['items'][0]['text']


# input word, and then will be translated into another language
# don't need to figure which language out
def translation_youdao():
    while True:
        content = input("请输入需要翻译的内容（退出输入q）：")
        if content in ("Q", "q", "quit"):
            break
        else:
            url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
            data = {}
            data["type"] = "AUTO"
            data["i"] = content
            data["doctype"] = "json"
            data["xmlVersion"] = "1.8"
            data["keyfrom"] = "fanyi.web"
            data["ue"] = "utf-8"
            data["action"] = "FY_BY_CLICKBUTTON"
            data["typoResult"] = "true"
            data = urllib.parse.urlencode(data).encode("utf-8")

            # 增加headers，模拟登陆，而不是对服务器识别为机器登陆。
            headers = {}
            headers[
                "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

            req = urllib.request.Request(url, data, headers)

            # 或者使用Request.add_header(key,value)
            # req=urllib.request.Request(url,data)
            # req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")

            response = urllib.request.urlopen(req)
            html = response.read().decode("utf-8")

            target = json.loads(html)
            print("翻译的结果为：%s" % (target["translateResult"][0][0]["tgt"]))
        time.sleep(2)


if __name__ == "__main__":
    start = time.time()
    # file_name = "D:\data\ec.txt.test.plain"
    # translation_bing_result(file_name)

    # test you dao crawl
    translation_bing("english")
    end = time.time()
    print("耗费的时间是:%d" %(end - start))
