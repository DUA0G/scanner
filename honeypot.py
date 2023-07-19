import socket
def kippo(ip,port): #ssh端口
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    banner = s.recv(1024)
    s.send(b'SSH-2.1-OpenSSH_5.9p1\r\n')
    try:
        data=s.recv(1024)
        if b'bad version' in data:
            return str(port)+'/kippo'
        else:
            return None
    except:
        return None

# print(data)
def HFish1(ip,port):  #telnet 端口 默认23
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))
    s.send(b'\r\n')
    try:
        data=s.recv(1024)
        if b'test\r\n' in data:
            return str(port) + '/HFish'
        else:
            return None
    except:
        return None

def HFish2(ip,port):  #默认8080
    # 导入requests包
    import requests
    url = "http://"+ip+':'+str(port)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    res = requests.get(url=url,headers=headers,verify=False)
    # print('url:', res.request.url)  # 查看发送的url
    # print("response:", res.text)  # 返回请求结果
    try:
        if '/static/x.jss' in res.text:
            return str(port) + '/HFish'
        else:
            return None
    except:
        return None

def glastopf(ip,port):  #http端口，默认80
    # 导入requests包
    import requests
    url = "http://"+ip+':'+str(port)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    try:
        res = requests.get(url=url,headers=headers,timeout=0.4,verify=False)
        # print('url:', res.request.url)  # 查看发送的url
        # print("response:", res.text)  # 返回请求结果
        if 'Please post your comments for the blog' in res.text:
            return str(port) + '/glastopf'
        else:
            return None
    except:
        return None


ip = '185.139.228.48'
port = 2222  #ssh端口
kippo(ip,port)

ip = '119.3.213.143'
port = 23
HFish1(ip,port)
port = 8080
HFish2(ip,port)