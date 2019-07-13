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
            self.dot.node(file, file)
            lines = f.readlines()
            for line in lines:
                if self.constStr in line:
                    child = re.search(r'( .*")', line.strip(), re.M | re.I)

                    if child!=None:
                        child = child.group().replace('"', '').strip()
                    elif child==None and self.hasSysHeadFile==True:
                        child = re.search(r'(<.*>)', line, re.M | re.I)
                        if child==None:
                            continue
                        child = child.group().strip()
                    self.dot.node(child, child)
                    self.dot.edge(child, file,constraint='true')


    #输出
    def output(self):
        isfile = os.path.isfile(self.dir)
        if isfile == False:
            files = os.listdir(self.dir)
            for file in files:
                suffix = file.split('.')[-1]
                if suffix == 'c':
                    self.create_relation(self.dir + file)


        else:
            suffix = self.dir.split('/')[-1].split('.')[-1]
            if suffix == 'c':
                self.create_relation(self.dir)
        self.dot.view()

searchStr = '#include '  # 寻找子节点
pls = PyLookSrc(searchStr,"./src/",True,'pdf')

pls.output()