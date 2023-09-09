打印机计算覆盖率程序
环境
```text
python     3.11
Pillow     10.0.0
pip        22.3.1
PyQt6      6.5.2
PyQt6-Qt6  6.5.2
PyQt6-sip  13.5.2
setuptools 65.5.1
wheel      0.38.4
```
1. 不同的图片识别工具可能对像素点识别结果不同。我这边对黑色的识别逻辑RGB色彩中的000000(0,0,0)，
对白色识别是FFFFFF(255,255,255)。
2. 题目中没有给每个像素点需要多少墨量，因此价格是无法计算的。我这边是默认取的10万像素1墨量，
计算公式为 总价=基价+增价*墨量、墨量=黑(彩)点阵数/100000
3. 我看视频中的演示程序应该是用C#做的，我这边采用的是Python，所以材料中给的SkinSharp文件(.she文件)我这边用不了。

打包成可执行文件
pyinstaller -F -w (-i icofile) 文件名.py