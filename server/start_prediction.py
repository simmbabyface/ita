import sys, getopt
import torch
import torch.utils.data as Data
import numpy as np
from torch import nn, optim
import torch.nn.functional as F
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import os
time=time.strftime('%Y-%m-%d')
mpl.rcParams['font.sans-serif'] = ['SimHei']  
mpl.rcParams['axes.unicode_minus'] = False

CHARSET = [' ', '#', '(', ')', '+', '-', '/', ':', '1', '2', '3', '4', '5', '6', '7',
        '8', '=', '@', 'A', 'B', 'C', 'F', 'H', 'I', 'N', 'O', 'P', 'S', '[', '\\', ']',
        'c', 'l', 'n', 'o', 'r', 's', 'i']
padlength=120

class OneHotEncoding(object):
	def __init__(self):
		self.charset=CHARSET
		
	def featurize(self,smiles):
		return np.array([self.encode(smi) for smi in smiles])
	
	def encode(self,smi):
		return np.array([self.one_hot_array(self.one_hot_index(x)) for x in self.pad_smi(smi)])

	def pad_smi(self,smi):
		return smi.ljust(padlength)
	
	def one_hot_index(self,x):
		return self.charset.index(x)
		
	def one_hot_array(self,index):
		return [int(x) for x in [ix == index for ix in range(len(self.charset))]]

def dataset(inputfile):
    # with open('./'+inputfile,encoding="utf-8") as f:
    #     smiles=[]
    #     label=[]
    #     for mol in f:
    #         mol.rstrip()
    #         proper=mol.split()
    #         smiles.append(proper[0])
    #         label.append(proper[1])
    
    smiles = [inputfile]
    label = ['1']
    mol = Chem.MolFromSmiles(smiles[0])
    img = Draw.MolToImage(mol)
    img.save(os.path.join('..', 'client', 'img', 'estrogen_activity_prediction', inputfile + '_1.png'))

    #img.show()
    ohe=OneHotEncoding()
    smiles_ohe=ohe.featurize(smiles)
    #print(smiles_ohe.shape)
    np.savez_compressed('./smilestest_try.npz', arr=smiles_ohe)
    
    #TestDataset建立
    smiles_ohe=np.load('./smilestest_try.npz')['arr'].astype(np.float32)
    test_smiles=torch.from_numpy(smiles_ohe)
    #一维卷积在最后一个维度上扫，所以最后一个维度是句子长度，应该调整为(40,38,120)
    test_smiles=test_smiles.permute(0,2,1)
    #print(test_smiles.shape)
    
    label_int=[]
    for x in label:
        label_int.append(int(x))
    test_label=torch.Tensor(label_int)
    
    testset=Data.TensorDataset(test_smiles,test_label)
    BATCH_SIZE=1
    testset_loader=Data.DataLoader(testset,batch_size=BATCH_SIZE)
    return testset_loader,img

torch.manual_seed(42)
class SmilestoPredict(nn.Module):
    def __init__(self):
        super(SmilestoPredict,self).__init__()
        self.conv1=nn.Sequential(nn.Conv1d(38,64,kernel_size=3),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=3),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=3),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=3),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.MaxPool1d(kernel_size=112))
        self.conv2=nn.Sequential(nn.Conv1d(38,64,kernel_size=5),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=5),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=5),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.MaxPool1d(kernel_size=108))
        self.conv3=nn.Sequential(nn.Conv1d(38,64,kernel_size=7),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=7),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=7),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.MaxPool1d(kernel_size=102))
        self.conv4=nn.Sequential(nn.Conv1d(38,64,kernel_size=9),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=9),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.Conv1d(64,64,kernel_size=9),nn.BatchNorm1d(64),nn.ReLU(),
                                    nn.MaxPool1d(kernel_size=96))
		
        self.fc=nn.Sequential(nn.Linear(256,120),nn.ReLU(),nn.Dropout(0.55),
                              nn.Linear(120,50),nn.ReLU(),nn.Dropout(0.55),
                              nn.Linear(50,20),nn.ReLU(),nn.Dropout(0.55),
                              nn.Linear(20,1),nn.Sigmoid())

    def forward(self, x):
        x1=self.conv1(x)
        x2=self.conv2(x)
        x3=self.conv3(x)
        x4=self.conv4(x)
        x_converge=torch.cat((x1,x2,x3,x4),1)
        x_converge=x_converge.view(-1,x_converge.size(1))
        x_fc=self.fc(x_converge)
        x_out=x_fc.view(x_fc.size(0))
        return x_out

def predict(data_loader):        
    epoch=5
    model=SmilestoPredict()
    model.load_state_dict(torch.load('./train-{:03d}.pth'.format(epoch)))
    model.eval()
    
    for batch_data in data_loader:
        batch_smiles, batch_label=batch_data
        out=model(batch_smiles)
        pred=out.ge(0.24).float()
        out_numpy=out.detach().numpy()
        batchlabel_numpy=batch_label.detach().numpy()
        predictivelabel_numpy=pred.detach().numpy()
    
    # for predictivelabel_single in predictivelabel_numpy:
    #     with open(outputfile,mode='a',encoding="utf-8") as h:
    #         print(str(predictivelabel_single),file=h)

    return out_numpy
   

def input_mapping_prediction(inputfile):
    data_loader,img=dataset(inputfile)
    out=predict(data_loader)
    # print('保存文件成功')
    active_porb=out[0]
    inactive_porb=1-active_porb
    elements = ['活性概率值', '无活性概率值']
    weight1 = [active_porb,inactive_porb]
    cs = ['orange','cyan']
    outer_cs = cs
    inner_cs = cs
    fig = plt.figure(figsize=(12, 8))
    #ax1=plt.subplot2grid((1,2),(0,0))
    #ax2=plt.subplot2grid((1,2),(0,1))
    #ax1.set_xticks([])
    #ax1.set_yticks([])
    #ax1.set_title('分子结构',size=20)
    #ax1.imshow(img)

    # ax1.yticks([])

    wedges1, texts1, autotexts1 = plt.pie(x=weight1,
                                        autopct='%3.1f%%',
                                        radius=1,
                                        pctdistance=0.85,
                                        startangle=90,
                                        counterclock=False,
                                        colors=outer_cs,
                                        # 锲形块边界属性字典
                                        wedgeprops={'edgecolor': 'white',
                                                    'linewidth': 1,
                                                    'linestyle': '-'
                                                    },
                                        # 锲形块标签文本和数据标注文本的字体属性
                                        textprops=dict(color='k',  #  字体颜色
                                                        fontsize=14,
                                                        family='Arial'))
    # 绘制中心空白区域
    plt.pie(x=[1],
            radius=0.6,
            colors=[fig.get_facecolor()])
    
    # 设置图例
    plt.legend(handles=wedges1,
            loc='best',
            labels=elements,
            title='',
            facecolor = fig.get_facecolor(),    # 图例框的填充颜色
            edgecolor='darkgray',
            fontsize=12)
    
    plt.title(label='化学品雌激素受体激活活性预测',
            # color='blue',
            size=20,
            weight='bold')
    plt.savefig(os.path.join('..', 'client', 'img', 'estrogen_activity_prediction', inputfile + '_2.png'), dpi=800)
    plt.clf()
    # plt.show()


def main():
    input_mapping_prediction('CC12CCC3C(CCc4cc(O)ccc43)C1CCC2O')
		

# if __name__ == '__main__':
#     main()                
# #__name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
# if __name__ == '__main__':
# 	main(sys.argv[1:])
#     #sys.argv的值，类型是一个list，分析一下值的组成，sys.argv[0]表示程序文件名，这是个默认值
    
# #Python中sys.argv是命令行参数从程序外部传值的的一种途径，它是一个列表，列表元素是我们想传进去的的新参数，所以可以用索引sys.argv[]来获得想要的值。
# #因为一个写好的程序一般封装好了，直接在编辑软件里运行就行了，但是程序里面的所有参数我们必须在程序里写好。
# #但是当我们想从程序外部向程序传递我们想要用的参数时，在不改动原来程序的基础上，我们可应通过命令行参数，用dos界面运行程序，然后赋参，即向程序输入新的参数，使程序运行。