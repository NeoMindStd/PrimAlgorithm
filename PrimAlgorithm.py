from tkinter import *
from tkinter import simpledialog

INT_MAX = 999999999
RLL = 8     # RECTANGLE LINE LENGTH

pts = []
rectangleParams = []
lines = []
drawLineMode = False

def showFrame():
    root = Tk()
    root.title("PrimAlgorithm")
    root.geometry("600x500")
    root.resizable(False, False)
    
    # 이벤트 리스너
    def onClick(pos):
        global drawLineMode
        printPosData("onClick", pos)
        
        # 클릭한 영역이 이미 있는 사각형 안쪽인지 판단
        drawLineMode=False
        for pt in pts:
            if pt[0]<=pos.x<=pt[0]+RLL and pt[1]<=pos.y<=pt[1]+RLL:
                drawLineMode=True
                tpt=list(map(lambda x:x+RLL//2,pt))
                break
            
        # 맞는 경우 사각형 선긋기 작동
        if drawLineMode:
            drawLineMode=True
            lines.append([(tpt[0], tpt[1])])
        # 아닌 경우 새로운 사각형 추가
        else:
            rectangleParams.append([pos.x, pos.y, pos.x+RLL, pos.y+RLL,
                                    {'outline':"red",'fill':"white"}])
            canvas.create_rectangle(*rectangleParams[-1][0:4],
                                    **rectangleParams[-1][4])
            pts.append((pos.x, pos.y))

    def onClickReleased(pos):
        global drawLineMode
        printPosData("onClickReleased", pos)
        # 선 긋기 모드인지 판단
        if drawLineMode:
            # 손을 뗀 영역이 이미 있는 사각형 안쪽인지 판단
            insideFlag = False
            for pt in pts:
                if pt[0]<=pos.x<=pt[0]+RLL and pt[1]<=pos.y<=pt[1]+RLL:
                    insideFlag=True
                    tpt=list(map(lambda x:x+RLL//2,pt))
                    break
            # 맞는 경우 사각형 선긋기 마무리 및 가중치 설정 팝업
            if insideFlag:
                lines[-1].append((tpt[0], tpt[1]))
                canvas.create_line(*lines[-1][0],*lines[-1][1])
                bias = simpledialog.askstring("Input",
                                "선의 가중치를 입력해주세요", parent=root)
                if bias is not None:
                    lines[-1].append(int(bias))
                    print('bias of the line:',lines[-1][-1])
                    bpt=((lines[-1][0][0]+lines[-1][1][0])/2,
                        (lines[-1][0][1]+lines[-1][1][1])/2)
                    canvas.create_rectangle(bpt[0]-RLL*1.5,bpt[1]-RLL,
                                            bpt[0]+RLL*1.5,bpt[1]+RLL,
                                            outline="white",fill="white")
                    canvas.create_text(*bpt,text = bias)
                else:
                    del lines[-1]
            # 아닌 경우 선긋기 취소
            else:
                del lines[-1]

        # 아닌경우
        else:
            drawLineMode = False

    def onResetTap():
        pass

    def onConfirmTap():
        try:
            pass
        except:
            print("***점을 2개 이상 찍어주세요***")
            btnReset.invoke()

    def printPosData(eventName, pos):
        print(eventName, "position: ", pos.x, pos.y)
        textPosX.delete(1.0, "end-1c")
        textPosX.insert(INSERT, f"{pos.x}")
        textPosY.delete(1.0, "end-1c")
        textPosY.insert(INSERT, f"{pos.y}")
        

    # 왼쪽 레이아웃    
    canvas = Canvas(root, width=500, height=500,
                        bg="white", relief="solid", bd=1)
    canvas.bind("<Button-1>", onClick)
    canvas.bind("<ButtonRelease-1>", onClickReleased)
    canvas.pack(side="left")

    # 오른쪽 레이아웃
    frameButtonBox = Frame(root, width=100, height=500, relief="solid", bd=1)
    frameButtonBox.pack(side="right")

    # X
    textX=Text(frameButtonBox, bg="#f0f0f0", width=1, height=1, relief="flat")
    textX.insert(INSERT,"X")
    textX.place(relx=0.1, rely=0.32)
 
    # x좌표
    textPosX = Text(frameButtonBox, width=8, height=1)
    textPosX.place(relx=0.3, rely=0.32)

    # Y
    textY=Text(frameButtonBox, bg="#f0f0f0", width=1, height=1, relief="flat")
    textY.insert(INSERT,"Y")
    textY.place(relx=0.1, rely=0.37)

    # y좌표
    textPosY = Text(frameButtonBox, width=8, height=1)
    textPosY.place(relx=0.3, rely=0.37)

    # Reset 버튼
    btnReset = Button(frameButtonBox, text="Reset", command=onResetTap,
                        overrelief="solid", width=10)
    btnReset.place(relx=0.1, rely=0.43)
    
    # Confirm 버튼
    btnConfirm = Button(frameButtonBox, text="Confirm", command=onConfirmTap,
                        overrelief="solid", width=10)
    btnConfirm.place(relx=0.1, rely=0.50)
        
    root.mainloop()

class Graph:
    pass

def detectMin(q):
    d.index(min(d))

def prim(g, r): #version 2
    # G=(V,E): 주어진 그래프
    # r: 시작정점(리스트의 인덱스)
    q=g[0]
    d=[INT_MAX for _ in range(len(q))]
    d[r]=0
    while q:
        u = detectMin(q,d)

showFrame()
