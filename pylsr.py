from graphviz import Digraph
import os,re



class PyLookSrc():
    # 初始化
    def __init__(self,searchStr,dir,hasSysHeadFile=False,output='pdf'):
        self.dot = Digraph(comment='Redis Source Relation Graph',node_attr={},engine='dot',format=output)
        self.constStr = searchStr
        self.dot.node_attr.update(color='lightblue2', style='filled')
        self.dir = dir
        self.hasSysHeadFile = hasSysHeadFile

    # 创建关系
    def create_relation(self,filedir):
        with open(filedir, "r") as f:
            file = filedir.split('/')[-1]
            print(file)
            self.dot.node(file, file)
            lines = f.readlines()
            print(lines)
            # 创建节点与关系
            for line in lines:
                if self.constStr in line:
                    # 在#include "xx.h" /* */这个字符串中提取出"xx.h"
                    child = re.search(r'( .*")', line.strip(), re.M | re.I)
                    # 匹配成功返回匹配结果并去掉引号及左右空格或换行符，得到xx.h
                    if child!=None:
                        child = child.group().replace('"', '').strip()
                    # child=None表示没有匹配上，比如#include <xx.h>
                    elif child==None:
                        # 若包含系统头文件，则继续匹配
                        if self.hasSysHeadFile==True:
                            child = re.search(r'(<.*>)', line, re.M | re.I)
                            # 系统头文件·匹配失败
                            if child==None:
                                continue
                            # 匹配成功，返回匹配结果
                            child = child.group().strip()
                        # 不包含系统头文件，直接进入下一次循环
                        else:
                            continue
                    print(child)
                    # 建立节点
                    self.dot.node(child, child)
                    # 建立关系/边
                    self.dot.edge(child, file,constraint='true')


    #输出
    def output(self):
        isfile = os.path.isfile(self.dir)
        # 当是文件夹的时候，截取后缀
        if isfile == False:
            files = os.listdir(self.dir)
            for file in files:
                # 截取后缀
                suffix = file.split('.')[-1]
                if suffix == 'c' or suffix=='cpp':
                    self.create_relation(self.dir + file)

        # 否则，直接传入文件夹目录，扫描文件夹的所有文件
        else:
            suffix = self.dir.split('/')[-1].split('.')[-1]
            if suffix == 'c' or suffix=='cpp':
                self.create_relation(self.dir)
        self.dot.view()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Help you understand the source code.")
    parser.add_argument('-s','--s', type=str, default='#include ',help='search xx.c/xx.cpp/xx.h etc')
    parser.add_argument('-d','--d', type=str, default='./src/',help='your c/cpp file or c/cpp dir')
    parser.add_argument('-i','--i', action='store_true',help='if you add this config,it will include the head file')
    parser.add_argument('-o', '--o', type=str, default='pdf',help='output format')


    args = parser.parse_args()

    searchStr = args.s
    dir = args.d
    sysHead = args.i
    out = args.o

    '''
    用户设置如下：
    第一个参数为在c/c++程序中寻找的头文件信息
    第二个参数为文件夹或者c、c++文件
    第三个参数为是否包含系统头文件，默认值为False
    第四个参数为输出格式，默认值为pdf,可以选择png、svg等
    '''
    pls = PyLookSrc(searchStr,dir,sysHead,out)

    pls.output()