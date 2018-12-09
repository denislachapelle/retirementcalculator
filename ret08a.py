#version 8a
#convert to qt

#
# conda install -c anaconda pyqt
# http://pyqt.sourceforge.net/Docs/PyQt5/index.html
# conda install -c conda-forge pyinstaller
#

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFrame, QLineEdit
#import os
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages
#import subprocess
#import ConfigParser

N=35 #number of year.

YearOld=[0]*N #year old of this year array.
Salary=[0]*N #salary of this year array.
Salary[0:3]=[0, 0, 0]
Benefit=[0]*N #revenue of this year.


CashAmount=[0]*N #total cash amount of this year.
CashRev=[0]*N
CashTax=[0]*N

CeliAmount=[0]*N #total celi amount of this year.
CeliRev=[0]*N

ReerAmount=[0]*N #total reer amount of this year.
ReerRev=[0]*N
ReerTax=[0]*N

HoldingAmount=[0]*N #total coporate amount of this year.
HoldingRev=[0]*N
HoldingTax=[0]*N

TotalCashEq=[0]*N

Expense=[0]*N #expense of this year.

Ipc=0
IntRate=0
PersoTaxRate=0
HoldingTaxRate=0


def Compute():
    
    i=0
    TotalCashEq[i] = CashAmount[i] + CeliAmount[i] + ReerAmount[i]*(1-PersoTaxRate) + HoldingAmount[i]*(1-HoldingTaxRate)
   
    for i in range(1, N):
       
     
       YearOld[i]=YearOld[i-1]+1
       
       #Compute interest revenue
       if YearOld[i] >= 65:
          Benefit[i] = 30 #30k pour linda et denis, pension qc et can.
       else:
          Benefit[i]=0
          
       CashRev[i]=CashAmount[i-1]*IntRate+Salary[i]+Benefit[i]
       CeliRev[i]=CeliAmount[i-1]*IntRate
       ReerRev[i]=ReerAmount[i-1]*IntRate
       HoldingRev[i]=HoldingAmount[i-1]*IntRate
    	
       #compute tax for each year.
       CashTax[i]=CashRev[i]*PersoTaxRate
       HoldingTax[i]=HoldingRev[i]*HoldingTaxRate
    	
       #Update Amounts
       CashAmount[i]=(CashAmount[i-1] + CashRev[i] - CashTax[i])*(1-Ipc)
       CeliAmount[i]=(CeliAmount[i-1] + CeliRev[i])*(1-Ipc)
       ReerAmount[i]=(ReerAmount[i-1] + ReerRev[i])*(1-Ipc)
       HoldingAmount[i]=(HoldingAmount[i-1] + HoldingRev[i] - HoldingTax[i])*(1-Ipc)
    
       #expenses
       Expense[i]=Expense[i-1]
        
       #where to take the money from.
       if Expense[i]<CashAmount[i]:
           CashAmount[i]=CashAmount[i]-Expense[i]
       else:
            RemainingExp=Expense[i]-CashAmount[i]
            CashAmount[i]=0
            
            #take cash in holding.
            if RemainingExp<HoldingAmount[i]:
                HoldingAmount[i]=HoldingAmount[i]-RemainingExp
            else:
                RemainingExp=RemainingExp-HoldingAmount[i]
                HoldingAmount[i]=0
                
                #take cask in reer
                #need remaining expense plus tax.
                PreTaxRemExp =RemainingExp/(1-PersoTaxRate)
                if PreTaxRemExp<ReerAmount[i]:
                   ReerAmount[i]=ReerAmount[i]-PreTaxRemExp
                   ReerTax[i]=PreTaxRemExp*PersoTaxRate
                else:
                   #remaining expense reduced by reer amount minus tax.
                   RemainingExp=RemainingExp-ReerAmount[i]*(1-PersoTaxRate)
                   ReerAmount[i]=0
                   
                   #take cash in celi
                   if RemainingExp<CeliAmount[i]:
                      CeliAmount[i]=CeliAmount[i]-RemainingExp
                   else:
                      RemainingExp=RemainingExp-CeliAmount[i]
                      CeliAmount[i]=0
        
       TotalCashEq[i] = CashAmount[i] + CeliAmount[i] + ReerAmount[i]*(1-PersoTaxRate) + HoldingAmount[i]*(1-HoldingTaxRate)

    
#    OutCsv()
    PlotFigure()
    
                      

def OutCsv():
    global Ipc, IntRate, PersoTaxRate, HoldingTaxRate
    file = open('result.csv','wt')
    
    file.write(('IPC = , {: .3f}\n').format(Ipc)) 
    file.write(('IntRate = , {: .3f}\n').format(IntRate)) 
    file.write(('PersoTaxRate = , {: .3f}\n').format(PersoTaxRate)) 
    file.write(('HoldingTaxRate = , {: .3f}\n').format(HoldingTaxRate)) 

    file.write('N, DenisYearOld, Salary, Benefit, CashAmount, HoldingAmount, ReerAmount, CeliAmount, TotalCashEq;\n') 
    i=0
    for i in range(1, N): 
        file.write(('{: f}, {: f}, {: f}, {: .2f}, {: .2f}, {: .2f}, {: .2f}, {: .2f}, {: .2f}\n').format(\
        i, YearOld[i], Salary[i], Benefit[i], CashAmount[i], HoldingAmount[i], ReerAmount[i], CeliAmount[i], TotalCashEq[i]))          

 
    file.close() 

def PlotFigure():
    plt.figure()
    plt.title('Amounts')
    plt.ylabel('K$')
    plt.plot(YearOld,TotalCashEq, 'b+')
    plt.plot(YearOld,CashAmount, 'b+')
    plt.plot(YearOld,HoldingAmount, 'g+')
    plt.plot(YearOld,ReerAmount, 'r+')
    plt.plot(YearOld,CeliAmount, 'c+')

    plt.text(80, 1100, 'CashEq: blue', color='blue')
    plt.text(80, 1000, 'Cash: blue', color='blue')
    plt.text(80, 900, 'Holding: green', color='green')
    plt.text(80, 800, 'Reer: red', color='red')
    plt.text(80, 700, 'Celi: cyan', color='cyan')
    plt.grid(which='both')
    plt.savefig('Fig.png', format='png')
    plt.show()

#def SetConfigFile():
    # lets create that config file for next time...
#    cfgfile = open("ret.ini",'w')

    # add the settings to the structure of the file, and lets write it out...
#    Config.add_section('Parameters')
#    Config.set('Parameters','CashAmount',CashAmount[0])
#    Config.write(cfgfile)
#    cfgfile.close()

def ExecuteAll():
    global Ipc, IntRate, PersoTaxRate, HoldingTaxRate
    CashAmount[0]=CashAmountLine.get()
    CeliAmount[0]=CeliAmountLine.get()
    ReerAmount[0]=ReerAmountLine.get()
    HoldingAmount[0]=HoldingAmountLine.get()
    Expense[0]=ExpenseLine.get()
    YearOld[0]=YearOldLine.get()
    Ipc=IpcLine.get()
    IntRate=IntLine.get()
    PersoTaxRate=PersonalTaxLine.get()
    HoldingTaxRate=HoldingTaxLine.get()
    
#    SetConfigFile()
    
    Compute() 
    
class OneLine:
    
    def __init__(self, LabelText, RowPos, InitialVal, Parent):
        self.Lb1=QLabel(LabelText, Parent)
        self.Lb1.move(20, RowPos)
        
        self.Le1=QLineEdit(str(InitialVal), Parent)
        self.Le1.move(120, RowPos)
    
    def get(self):
         return float(self.Le1.text())




app = QApplication([])
MainFrame=QFrame()

rp=100
CashAmountLine=OneLine(LabelText="Initial Cash Amount", RowPos=rp, InitialVal=100, Parent=MainFrame)
rp=rp+20
CeliAmountLine=OneLine(LabelText="Initial CELI Amount", RowPos=rp, InitialVal=100, Parent=MainFrame)
rp=rp+20
ReerAmountLine=OneLine(LabelText="Initial REER Amount", RowPos=rp, InitialVal=100, Parent=MainFrame)
rp=rp+20
PersonalTaxLine=PersonalTaxLine=OneLine(LabelText="Personal Tax Rate", RowPos=rp, InitialVal=0.35, Parent=MainFrame)
rp=rp+20
HoldingAmountLine=OneLine(LabelText="Initial Holding Amount", RowPos=rp, InitialVal=100, Parent=MainFrame)
rp=rp+20
HoldingTaxLine=OneLine(LabelText="Holding Tax Rate", RowPos=rp, InitialVal=0.30, Parent=MainFrame)
rp=rp+20
ExpenseLine=OneLine(LabelText="Expense Amount", RowPos=rp, InitialVal=95, Parent=MainFrame)
rp=rp+20
YearOldLine=OneLine(LabelText="Your Age", RowPos=rp, InitialVal=58, Parent=MainFrame)
rp=rp+20
IpcLine=OneLine(LabelText="IPC", RowPos=rp, InitialVal=0.018, Parent=MainFrame)
rp=rp+20
IntLine=OneLine(LabelText="Interest Rate", RowPos=rp, InitialVal=0.065, Parent=MainFrame)


bt1=QPushButton("test", MainFrame)
bt1.clicked.connect(ExecuteAll)
bt1.move(20, 300)

MainFrame.setGeometry(100, 100, 500, 400)

MainFrame.setWindowTitle("retirement calculator")
MainFrame.show()

app.exec_()










