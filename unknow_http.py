def test_http(ip,port):  #http端口，默认80
    # 导入requests包
    import requests
    url = "http://"+ip+':'+str(port)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    try:
    # if 1:
        res = requests.get(url=url,headers=headers,timeout=0.4)
        code = res.status_code
        # print(res.text)
        return True
    except:
        return False

# print(test_http('113.30.191.68',15672))