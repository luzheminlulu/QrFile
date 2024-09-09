# 将文件变成二维码传输~

## 1.发送端使用方法
pip安装缺失的python库
```
pip install pillow
pip install opencv-python
pip install qrcode
```
运行QRCODE.py即可将文件转换成二维码串

```
python3 QRCODE.py -f filename [-s 300] 
```
如果相机拍摄模糊，识别率低的话，可以适当降低-s的大小，-s默认值为400


## 2.接收端使用方法
由于访问摄像头需要https，在运行服务端前请先配置ssl证书，有域名的用域名证书，没有的自己用opsnessl生成
```
#用编辑器打开server.py
httpd.socket = ssl.wrap_socket(httpd.socket,  
                                certfile='/mnt/disk1/unraid/ssl/cert.pem',   #修改这两行
                                keyfile='/mnt/disk1/unraid/ssl/key.pem',     #修改这两行
                                server_side=True,
                                ssl_version=ssl.PROTOCOL_TLSv1_2)  
```
运行服务端。然后打开网页，点击[开扫]即可完成后续传输，
```
python3 server.py  #访问https://[ip]:4443
```


## 3.使用提醒
速度不是很快。实测算上丢包大约0.5~1KB/s

对于个别二维码长时间没扫到，可以直接用键盘输入数字指定显示某张二维码

按下空格可以暂停或继续刷新二维码

可以用方向键控制加速/减速/上一张/下一张二维码


## 3.网页demo
如果不想自己创建服务端，可以直接使用此demo：

https://luzheminlulu.github.io
