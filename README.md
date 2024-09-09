基于qrcode，opencv-python等库

运行QRCODE.py即可将文件转换成二维码串

```
python3 QRCODE.py -f filename [-s 300] 
```
相机拍摄模糊，识别率低的话，可以适当降低-s的大小，-s默认值为400

然后打开网页即可完成后续传输，注意网页需要https才能访问摄像头

对于个别二维码长时间没扫到，可以直接用键盘输入数字指定显示某张二维码，按下空格继续刷新

demo:
https://luzheminlulu.github.io
