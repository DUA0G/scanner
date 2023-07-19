import nmap
import web_finger
import honeypot
import  unknow_http
import os
import urllib3
urllib3.disable_warnings()
nm = nmap.PortScannerYield()
# nm = nmap.PortScanner()
res_json = {}

all_services = ['windows','centos','ubuntu','openssh','openssl','wordpress','liteSpeed','jetty','java','node.js','express','asp.net','php','microsoft httpapi','rabbitmq','apache','iis','nginx','micro_httpd','openresty','grafana','weblogic','elasticsearch','debian']
#wordpress ，grafana 和大大部分编程语言需要进一步检测 ，apac，httpapi，iis，openresty，Advanced Message Queue Protocol--rabbitmq
all_protocol = ['ssh','http','https','rtsp','ftp','telnet','amqp','mongodb','redis','mysql']
def filter(name):
    name = name.replace('[','').replace(']','')
    for i in all_services:
        if i in name.lower():
            return i
    return None


def getversion(s):
    version = '/'
    for i in s:
        if i == '/' or i == '.' or i.isnumeric() or i == ' ':
            if i == ' ' or i == '/':
                continue
            version += i
        else:
            break
    if version == '/':
        version = '/N'
    return version
def filter_all(name):
    name = name.replace('[','').replace(']','')
    result = []
    for i in all_services:
        if i in name.lower():
            location = name.lower().find(i) + len(i)
            # print(name.lower()[location:])
            version = getversion(name.lower()[location:])
            result.append(i + version)
    return result
def filter_protocol(protocol):
    if protocol == '':
        return None
    for i in all_protocol:
        if protocol.lower() in i:
            return i
    # print(protocol.lower(),type(protocol.lower()))
    return None

def filter_result(services):
    delete_index = []
    for i in range(len(services)):
        for j in range(len(services)):
            if i == j:
                continue
            if services[i].split('/')[0] == services[j].split('/')[0]:
                # print(services[i].split('/')[1], services[j].split('/')[1])
                if services[i].split('/')[1] == 'N' and services[j].split('/')[1] != 'N':
                    delete_index.append(i)
                    continue
                if services[i].split('/')[1] != 'N' and services[j].split('/')[1] == 'N':
                    delete_index.append(j)
                    continue
                if services[i].split('/')[1] >= services[j].split('/')[1]:
                    delete_index.append(j)
                if services[i].split('/')[1] < services[j].split('/')[1]:
                    delete_index.append(i)
    # print(delete_index)
    # print(services)
    delete_index = list(set(delete_index))
    for i in delete_index:
        services.pop(i)



def scan_finger(ip,ports):
    for result in nm.scan(ip, ports=ports, arguments="-sV -Pn"):
    # for result in nm.scan('113.30.191.229', ports='2222,443', arguments="-sV"):
    # for result in nm.scan('103.252.119.251', ports='6379,3306,21,80,1022,8083,7001,9200,2202', arguments="-sV"):
        honeypo = None
        deviceinfo = None
        services = []
        state = result[1]['nmap']['scanstats']['uphosts']
        if state == '0':
            continue
        # print(result[0]) #ip
        ip = result[0]
        scan_result = result[1]['scan'][result[0]]['tcp']
        for i in scan_result:
            # print(i,scan_result[i])
            port = i
            protocol = scan_result[i]['name']
            if protocol == 'unknown':   #经测试namp会将部分http协议扫描为unkonw
                if unknow_http.test_http(ip,port):
                    protocol = 'http'
            protocol = filter_protocol(protocol)
            # print(protocol)

            if port == 443 and protocol == 'http':
                protocol = 'https'
            service_app = filter(scan_result[i]['product'])
            if service_app != None:
                # service_app += '/'
                service_app += getversion(scan_result[i]['version'])
            service_app2 = filter_all(scan_result[i]['extrainfo'])
            service_app_ex = filter_all(scan_result[i]['version'])  #这里经测试后发现OpenSSH 5.1p1 Debian 5会有debian出现在version中所以加了ex变量存一下debian
            if service_app != None:
                service_app2.append(service_app)
            service_app2.extend(service_app_ex)
            # print(service_app2)
            # if protocol == 'amqp':   #一开始通过fofa搜索rabbitmq全是amqp协议所以认为它们一起出现了
            #     service_app2.append('rabbitmq/N')

            if protocol == 'http' or protocol == 'https':
                new_service = web_finger.scan_device_and_cms(ip, port)
                # print(new_service)
                if new_service != None:
                    new_service[0] = new_service[0].replace('[','').replace(']','') #由于未知原因在测试时[0]总会多两个中括号
                    #(fingerprint(body=resp,header=str(resh),url=url), Server,titles,X_Powered)
                    if '/' in new_service[0]:
                        deviceinfo = new_service[0]
                    elif ' ' in new_service[0]:
                        service_app = [new_service[0].split(' ')[0] + '/N', new_service[0].split(' ')[1] + '/N']
                    else:
                        service_app = [new_service[0] + '/N']
                    if service_app != None:
                        service_app2.extend(service_app)
                    service_app3 = filter_all(new_service[1]+new_service[2]+new_service[3])
                    service_app2.extend(service_app3)
                    service_app2 = list(set(service_app2))
            # print(service_app2)
            if protocol == 'http':
                honeypo = honeypot.glastopf(ip,port)
                if honeypo == None:
                    honeypo = honeypot.HFish2(ip, port)
            if protocol == 'telnet':
                honeypo = honeypot.HFish1(ip,port)
            if protocol == 'ssh':
                honeypo = honeypot.kippo(ip,port)

            if '/N' in service_app2:
                service_app2.remove('/N')
            if service_app2 == [None] or service_app2 == []:
                service_app2 = None
            if service_app2 != None:
                filter_result(service_app2)

            services.append({'port':port,'protocol':protocol,'service_app':service_app2})
            # print(services)
        homework = {ip:{"services":services,'deviceinfo':deviceinfo,'honeypo':honeypo}}
        print(homework)
        print()
        # for single in homework[ip]:
        #     print(single,homework[ip][single])


            # print(i, 'state:', scan_result[i]['state'], '\nname:', scan_result[i]['name'], '\nproduct:',
            #       scan_result[i]['product'], '\nversion:', scan_result[i]['version'],'\nextrainfo:', scan_result[i]['extrainfo'],'\ncpe:', scan_result[i]['cpe'])
            # print('*****************')
        # print('----------------------------------')
        # print()

os.environ['ALL_PROXY'] = 'http://192.168.2.93:7890'
# X-Redirect-By:wordpress
#java   X-Powered-By:  asp.net  php express (node.js——未找到单独，但和express同时出现)
# grafana

# ip = '159.65.92.42'
# ports = '80,443'

ip = '185.139.228.48'
ports = '2222,3306,2202,8080'

# ip = '113.30.191.68'
# ports = '15672'

ip = '211.22.90.152'
ports = '80,554,8000,49152,30948,30949,30960,9010,9020,53000'

ip = '185.139.228.183'
ports = '8082,22,80,443,1883,8081'
# ports = '53000'
scan_finger(ip,ports)