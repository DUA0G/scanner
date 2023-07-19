ports.py实现了主机存活探测和端口扫描，利用了多线程，但受限于python的特性扫描速度仍然比较慢。

scan4.py是利用python-nmap进行扫描，本质上就是调用nmap（一开始没说协议只要这么多，所以为了保证足量协议就用了nmap，后来也不想改了就用的这个）

honeypot.py是检测蜜罐代码

web_finger.py抄的github上的web_finger.py代码，基本就是改改输出输出格式和指纹库，用于检测部分nmap无法检测的cms如wordpress和设备

unknow_http.py是在测试多个案例后发现部分特殊的http端口nmap无法扫描出http协议而是显示unknown，而增加的用于检测nmap协议结果为unknown的端口是否为http协议的脚本

json_write.py是一个json文件写入案例

使用（建议linux下使用）：

```bash
apt install nmap

conda create -n scan python=3.9

conda activate scan

pip install -r requirements.txt
```



将scan4.py中的ip和ports修改即可进行资产检测，或

```python
import scan4

scan4.scan_finger(ip,ports)


```

在调试完毕后需要将最后的print改成json.dump写到json文件中

注：注意题目中要求null的部分在我的测试结果中为None，而非null，这里是因为python中没有null，代替的是None，利用json dump转json文件后会自动变成null![2](https://gitee.com/javayuanxpy/blog_picture/raw/master/img/2.png)
