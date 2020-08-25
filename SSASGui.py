from tkinter import *
import tkinter
import tkinter.ttk

import SICConvert
from SICConvert import *

'''
    title : 제목
    geometry : 너비 x 높이 + x좌표 + y좌표
    resizeable(상하, 좌우)
    win.destroy() : 창 닫음

    notebook으로 탭 만들고 안에 Frame 집어넣음.

'''

output=""
input=""

HexaList = None
AsciiList = None
binaryList = None

def exceuteProcess():
    global input
    global output
    global HexaList
    global AsciiList
    global binaryList

    input = InputText.get("1.0","end") #InputText내용 저장
    t = input.split("\n")
    t = list(map(lambda x:x.strip(), t))[:-1]

    myList = preProcess(t)  # 파일 불러오기 / 스플릿
    mList, startAddr, SymbolTable, progSize, endAddress, programName = get_Address(myList)  # 불러온 파일에서 시작주소, 주소가 담긴 명령어, 심볼테이블 로딩

    Obcode_list = create_ObjCode(mList, SymbolTable)  # Obcode_list에 Obcode 저장
    print(Obcode_list)#[['1000', 'COPY', 'START', '1000', '']...
    Oblist = list(map(lambda x:x[4], Obcode_list))
    for i, x in enumerate(Oblist):
        HexaList.insert(i, x)

    for i, x in enumerate(Oblist):
        Ascii=""
        for k in range(0,len(x),2):
            Ascii=Ascii+(str(HexaToDec(x[k])*16+HexaToDec(x[k+1]))).zfill(2)
        AsciiList.insert(i, Ascii)

    for i,x in enumerate(Oblist):
        Binary=""
        if x!='':
            Binary=bin(int(x,16))[2:]
            binaryList.insert(i,Binary)


    ObProg_list = create_ObjFile(Obcode_list, startAddr, programName, progSize)  # Object_Program이 ObProg_list에 저장

    for i in ObProg_list:
        output += i + "\n"

    outputWindow["text"] = output


def HexaToDec(Hexa):
    if Hexa >= '0' and Hexa <= '9':
        return ord(Hexa) - ord('0')
    if Hexa >= 'A' and Hexa <= 'F':
        return ord(Hexa) - ord('A') + 10
    if Hexa >= 'a' and Hexa <= 'f':
        return ord(Hexa) - ord('a') + 10
    return 0





window = Tk()
window.title("SSAS Project")
window.geometry("1500x550+300+300")

inputLabel=tkinter.Label(text="INPUT",height=1)
inputLabel.grid(row=0,column=0,rowspan=1)

InputText = tkinter.Text(window, width=33, height=34)
InputText.grid(row=1, column=0,columnspan=3)

scroll_y=Scrollbar(window,command=InputText.yview)
scroll_y.grid(row=1,column=3)

LoadBtn = tkinter.Button(window, width=10, text="LOAD")
LoadBtn.grid(row=2, column=0)

ModifyBtn=tkinter.Button(window,width=10,text="MODIFY")
ModifyBtn.grid(row=2,column=1)

ExecuteBtn=tkinter.Button(window,width=10,text="EXECUTE",command=exceuteProcess) #실행
ExecuteBtn.grid(row=2,column=2)

notebook = tkinter.ttk.Notebook(window, width=300, height=426)
notebook.grid(row=1, column=4, padx=10)




binaryFrame = tkinter.Frame(window)
binaryList = tkinter.Listbox(binaryFrame, width=300, height=400)
binaryList.pack()
notebook.add(binaryFrame, text="binary")

AsciiFrame = tkinter.Frame(window)
AsciiList = tkinter.Listbox(AsciiFrame, width=300, height=400)
AsciiList.pack()
notebook.add(AsciiFrame, text="Ascii")

HexaFrame = tkinter.Frame(window)
HexaList = tkinter.Listbox(HexaFrame, width=300, height=400)
HexaList.pack()
notebook.add(HexaFrame, text="Hexa")




outputLabel=tkinter.Label(text="Output")
outputLabel.grid(row=0,column=6)
outputWindow=tkinter.Label(window,bg="white",width=90,height=10)
outputWindow.grid(row=1,column=6)

window.mainloop()

print(input)
