from tkinter import *
from tkinter import simpledialog

INT_MAX = 999
RLL = 10     # RECTANGLE LINE LENGTH

pts = []
rectangleParams = []
lines = []
l=dict()
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

        # 클릭한 영역이 왼쪽 절반인지 판단
        if pos.x>=250:return
        
        # 클릭한 영역이 이미 있는 사각형 안쪽인지 판단
        drawLineMode=False
        for i in range(len(pts)):
            pt=pts[i]
            if pt[0]<=pos.x<=pt[0]+RLL and pt[1]<=pos.y<=pt[1]+RLL:
                drawLineMode=True
                tpt=i
                break
            
        # 맞는 경우 사각형 선긋기 작동
        if drawLineMode:
            drawLineMode=True
            lines.append([i])
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
        if drawLineMode and pos.x<250:
            # 손을 뗀 영역이 이미 있는 사각형 안쪽인지 판단
            insideFlag = False
            for i in range(len(pts)):
                pt=pts[i]
                if pt[0]<=pos.x<=pt[0]+RLL and pt[1]<=pos.y<=pt[1]+RLL:
                    insideFlag=True
                    tpt=i
                    break
            # 맞는 경우 사각형 선긋기 마무리 및 가중치 설정 팝업
            if insideFlag:
                lines[-1].append(i)
                canvas.create_line(*list(map(lambda x:x+RLL//2,pts[lines[-1][0]])),
                                   *list(map(lambda x:x+RLL//2,pts[lines[-1][1]])))
                bias = simpledialog.askstring("Input",
                                f"선의 가중치를 입력해주세요{INT_MAX}미만", parent=root)
                if bias is not None:
                    lines[-1].append(int(bias))
                    print('bias of the line:',lines[-1][-1])
                    try:l[lines[-1][0]]
                    except KeyError:l[lines[-1][0]]=set()
                    l[lines[-1][0]].add(lines[-1][1])
                    try:l[lines[-1][1]]
                    except KeyError:l[lines[-1][1]]=set()
                    l[lines[-1][1]].add(lines[-1][0])
                    bpt=((pts[lines[-1][0]][0]+pts[lines[-1][1]][0]+RLL)/2,
                        (pts[lines[-1][0]][1]+pts[lines[-1][1]][1]+RLL)/2)
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
        global pts, rectangleParams, lines, l, drawLineMode
        pts, rectangleParams, lines, l, drawLineMode = [], [], [], dict(), False
        textPosX.delete(1.0, "end-1c")
        textPosY.delete(1.0, "end-1c")
        canvas.delete("all")
        # 영역을 반으로 나누는 선
        canvas.create_line(250,0,250,500)

    def onConfirmTap():
        #try:
        print("pts:", pts)
        print("lines:", lines)
        print(l)
        prim(pts,0,canvas)
        #except:
        #    print("***점을 2개 이상 찍어주세요***")
        #    btnReset.invoke()

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

    # 영역을 반으로 나누는 선
    canvas.create_line(250,0,250,500)

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

def detectMin(q, d, c):
    m=INT_MAX
    r=-1
    for i in range(len(d)):
        if m > d[i] and i not in c:
            r=i
    c.add(r)
    return r

def w(u,v):
    for i in range(len(lines)):
        if lines[i][0]==u and lines[i][1]==v or\
        lines[i][0]==v and lines[i][1]==u :
            return lines[i][2]

# 최소비용 신장트리를 구하지 못하는 버그가 있는 것으로 보임
def prim(q, r, canvas): #version 2
    # q: 정점 리스트
    # r: 시작정점(리스트의 인덱스)
    tree=dict()
    d=[INT_MAX for _ in range(len(q))]
    mat=[[999]*len(q)for _ in range(len(q))]
    for i in range(len(q)):mat[i][i]=0
    printMat(mat,0)
    d[r]=0
    c=set()
    cnt=1
    while len(c)<len(q):
        u = detectMin(q,d,c)
        # print(l[u])
        for v in l[u]:
            wuv=w(u,v)
            if v not in c and wuv<d[v]:
                d[v]=wuv
                tree[v]=u                
                for key,value in tree.items():mat[key][value]=mat[value][key]=w(key,value)
                printMat(mat,cnt)
                cnt+=1

    # print(q,tpt)
    # print(d)
    # print(tree)
    
    tpt=list(map(lambda x:(x[0]+250,x[1]),q))
    for i in range(len(q)):mat[i][i]=0
    for key,value in tree.items():
        canvas.create_line(*tpt[key],*tpt[value])
        mat[key][value]=mat[value][key]=w(key,value)
    for i in range(len(tpt)):
        canvas.create_rectangle(tpt[i][0]-RLL*1.5,tpt[i][1]-RLL,
                                tpt[i][0]+RLL*1.5,tpt[i][1]+RLL,
                                outline="white",fill="white")
        canvas.create_text(*tpt[i],text = d[i])
    printMat(mat)

def printMat(mat, cnt=None):
    if cnt is None:print('\n최종')
    else:print(f'\n{cnt}번째 과정')
    r=[]
    for row in mat:r.append('\t'.join(map(str,row)))
    print('\n'.join(r))
    print()

showFrame()
