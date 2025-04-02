基于生物发光法的体细胞检测仪研发，此代码是一套用于荧光计数的算法。


# 1. 运行环境

导出环境：conda env export --name 环境名称 > environment.yml

复刻环境：conda env create -f environment.yml
环境名称在yml文件name：中修改

覆盖环境：conda env update --name 环境名称 --file environment.yml

# 2. 打包发布

pyinstaller -F -w --icon=./libs/icons/cell.ico main.py
-w (–windowed / –noconsole): 对于 GUI 应用程序，隐藏控制台窗口。
--icon=FILE.ico: 指定可执行文件的图标。