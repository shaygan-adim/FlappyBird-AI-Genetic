import numpy,math,random,pickle
import matplotlib.pyplot as plt
SHOW=True
if SHOW:
        import pygame
        pygame.init()
        font1=pygame.font.Font(None,30)
        font2=pygame.font.Font(None,20)
        scr = pygame.display.set_mode((1300,600))
        pygame.display.set_caption('Flappy Bird - AI')


dt=0.1
g=1

N=355
mio=0.8
n=120
NB=5
K=25


def Breed1(A1,A2,t1,t2,t):
        A3=numpy.copy(A1)
        for i in range(int(A1.size/A1[0].size)):
                for j in range(A1[0].size):
                        r=random.random()
                        e=(K+1)/(t+K)
                        if r<(t1/(t1+t2)):
                                if random.random()<e:
                                        A3[i,j]=A1[i,j]*(1+mio/100*random.choice([-1,1]))
                        else:
                                if random.random()<e:
                                        A3[i,j]=A2[i,j]*(1+mio/100*random.choice([-1,1]))
        return A3
def Breed2(A1,A2,t1,t2,t):
        A3=numpy.copy(A1)
        for i in range(int(A1.size/A1[0].size)):
                r=random.random()
                e=(K+1)/(t+K)
                if r<(t1/(t1+t2)):
                        if random.random()<e:
                                A3[i]=A1[i]*(1+mio/100*random.choice([-1,1]))
                else:
                        if random.random()<e:
                                A3[i]=A2[i]*(1+mio/100*random.choice([-1,1]))
        return A3
def Breed3(A1,t):
        A3=numpy.copy(A1)
        for i in range(int(A1.size/A1[0].size)):
                for j in range(A1[0].size):
                        r=random.random()
                        e=(K+1)/(t+K)
                        if random.random()<e:
                                A3[i,j]=A1[i,j]*(1+mio/100*random.choice([-1,1]))
        return A3
def Breed4(A1,t):
        A3=numpy.copy(A1)
        for i in range(int(A1.size/A1[0].size)):
                r=random.random()
                e=(K+1)/(t+K)
                if random.random()<e:
                        A3[i]=A1[i]*(1+mio/100*random.choice([-1,1]))
        return A3
def mymax(a):
        big=0
        j=0
        for i in range(len(a)):
                if a[i][0]>big:
                        j=i
                        big=a[i][0]
        return j,big
 
def mysort(a):
        b=[]
        for i in range(len(a)):
                b+=[a[i][0]]
        b.sort()
        c=[0]*len(b)
        for i in range(len(b)):
                for j in range(len(a)):
                        if b[i]==a[j][0]:
                                c[i]=j
        return c
def myadd(A,x):
        f=-1
        for i in range(len(A)):
                if x>A[i] and f==-1:
                        f=i
        if f==-1:
                return False
        return A[:f]+[x]+A[f:len(A)-1],f
SIG = numpy.vectorize(lambda t: t )
IL = numpy.zeros((N,5))
X,Y,Y2=[0],[0],[0]
L1=numpy.zeros((N,3))
L2=numpy.zeros((N,3))
R=numpy.zeros((N,1))
done=False
I=0

SB=[0]*10
W1B = [numpy.zeros((5,3))]*10
W2B = [numpy.zeros((3,3))]*10
W3B = [numpy.zeros((3,1))]*10
B1B = [numpy.zeros((3))]*10
B2B = [numpy.zeros((3))]*10
B3B = [numpy.zeros((1))]*10
W1 = numpy.random.randint(-100,100,size=(N,5,3))/100
W2 = numpy.random.randint(-100,100,size=(N,3,3))/100
W3 = numpy.random.randint(-100,100,size=(N,3,1))/100
B1 = numpy.random.randint(-100,100,size=(N,3))/20
B2 = numpy.random.randint(-100,100,size=(N,3))/20
B3 = numpy.random.randint(-100,100,size=(N,1))/20
while not done:
        if I%5==0:
                print('Generation : '+str(I+1))
                print('Highscore : '+str(max(SB)))
        by=numpy.zeros(N)+300
        bv=numpy.zeros(N)
        ba=numpy.zeros(N)+1
        walls = numpy.array([[1300,random.randint(10,440)]],dtype='float64')
        SCORE=[]
        for i in range(N):
                SCORE+=[[0,i]]
        II=0
        while True:
                if SHOW:
                        txt5=None
                        for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                        pass
                        scr.fill('BLACK')
                        txt1=font1.render('Generation : '+str(I+1),True,(150,150,150))
                        txt2=font1.render('Score : '+str(II),True,(150,150,150))
                        if II<max(SB):
                                txt4=font1.render('Highest Score : '+str(max(SB)),True,(150,150,150))
                        else:
                                txt5=font1.render('New Record !',True,(255,0,0))
                                txt4=font1.render('Highest Score : '+str(II),True,(150,150,150))
                        txt6=font1.render('Alive Birds : '+str(int(numpy.sum(ba))),True,(150,150,150))
                        txt3=font2.render('SHANSTER',True,(150,150,150))
                        scr.blit(txt1,(75,50))
                        scr.blit(txt2,(75,75))
                        scr.blit(txt4,(75,100))
                        try:
                                scr.blit(txt5,(1150,20))
                        except:
                                pass
                        scr.blit(txt6,(75,125))
                        scr.blit(txt3,(1210,570))
                        for i in range(int(walls.size/2)):
                                pygame.draw.rect(scr,(255,255,255),(int(walls[i,0]),0,75,int(walls[i,1])),5)
                                pygame.draw.rect(scr,(255,255,255),(int(walls[i,0]),int(walls[i,1])+100,75,600),5)
                walls[:,0]-=15*dt
                if walls[0,0]<-75:
                        walls=numpy.copy(walls[1:,:])
                if walls[int(walls.size/2)-1,0]<1300-75-170:
                        RR=random.randint(10,440)
                        while abs(RR-walls[int(walls.size/2)-1,1])>80:
                                RR=random.randint(10,440)
                        walls=numpy.append(walls,numpy.array([[1300,RR]],dtype='float64'),axis=0)
                for i in range(N):
                        if -25<walls[0,0]<50:
                                IL[i,0]=-10
                                IL[i,1]=(walls[0,0]+25)/10
                                IL[i,2]=(walls[0,1]-by[i])/10
                        if walls[0,0]>50:
                                IL[i,0]=10
                                IL[i,1]=(walls[0,0]-50)/10
                                IL[i,2]=(walls[0,1]-by[i])/10
                        if walls[0,0]<-25:
                                IL[i,0]=10
                                IL[i,1]=(walls[1,0]-50)/10
                                IL[i,2]=(walls[1,1]-by[i])/10
                        IL[i,3]=bv[i]/5
                        IL[i,4]=by[i]/10
                for i in range(N):
                        if ba[i]==1:
                                L1[i]=numpy.matmul(IL[i],W1[i])+B1[i]
                                L2[i]=numpy.matmul(L1[i],W2[i])+B2[i]
                                R[i]=numpy.matmul(L2[i],W3[i])+B3[i]
                                if R[i,0]>0:
                                        bv[i]=-10
                by+=bv*dt
                bv+=g*dt
                for i in range(N):         
                        if ba[i]==1:
                                if SHOW:
                                        pygame.draw.circle(scr,(255,0,0),(50,by[i]),10)
                                SCORE[i][0]=II
                        if -20<walls[0,0]<55 and (not (walls[0,1]<by[i]<walls[0,1]+100)) and ba[i]==1:
                                ba[i]=0
                                SCORE[i][0]=II-abs(by[i]-walls[0,1]+50)
                        if not(5<by[i]<595) and ba[i]==1:
                                ba[i]=0
                        if ba[i]==1 and myadd(SB,II)!=False:
                                SB,f=myadd(SB,II)
                                W1B = W1B[:f]+[W1[i]]+W1B[f:len(W1B)-1]
                                W2B = W2B[:f]+[W2[i]]+W2B[f:len(W2B)-1]
                                W3B = W3B[:f]+[W3[i]]+W3B[f:len(W3B)-1]
                                B1B = B1B[:f]+[B1[i]]+B1B[f:len(B1B)-1]
                                B2B = B2B[:f]+[B2[i]]+B2B[f:len(B2B)-1]
                                B3B = B3B[:f]+[B3[i]]+B3B[f:len(B3B)-1]
                if numpy.sum(ba)==0:
                        break
                if SHOW:
                        pygame.display.update()
                II+=1
        I+=1
        ss=0
        for i in range(N):
                ss+=SCORE[i][0]
        Y2+=[ss/N]
        X+=[I]
        Y+=[II]

        if I==n:
                done=True
        for i in range(len(SCORE)):
                        for j in range(len(SCORE)):
                                if SCORE[i][0]==SCORE[j][0]:
                                        SCORE[i][0]+=random.random()*0.001*random.choice([1,-1])
        BS = mysort(SCORE)[len(SCORE)-NB:]
        W11= numpy.random.randint(-100,100,size=(N,5,3))/100
        W22 = numpy.random.randint(-100,100,size=(N,3,3))/100
        W33 = numpy.random.randint(-100,100,size=(N,3,1))/100
        B11=numpy.random.randint(-100,100,size=(N,3))/20
        B22=numpy.random.randint(-100,100,size=(N,3))/20
        B33=numpy.random.randint(-100,100,size=(N,1))/20
        k=-1
        for kkk in range(25):
                for i in range(NB):
                        for j in range(i+1,NB):
                                k+=1
                                W11[k]=Breed1(W1[BS[i]],W1[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
                                W22[k]=Breed1(W2[BS[i]],W2[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
                                W33[k]=Breed1(W3[BS[i]],W3[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
                                B11[k]=Breed2(B1[BS[i]],B1[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
                                B22[k]=Breed2(B2[BS[i]],B2[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
                                B33[k]=Breed2(B3[BS[i]],B3[BS[j]],SCORE[BS[i]][0],SCORE[BS[j]][0],I)
        for j in range(20):
                for i in range(NB):
                        k+=1
                        W11[k]=Breed3(W1[k],I)
                        W22[k]=Breed3(W2[k],I)
                        W33[k]=Breed3(W3[k],I)
                        B11[k]=Breed4(B1[k],I)
                        B22[k]=Breed4(B2[k],I)
                        B33[k]=Breed4(B3[k],I)
        for i in range(NB):
                k+=1
                W11[k]=W1[BS[i]]
                W22[k]=W2[BS[i]]
                W33[k]=W3[BS[i]]
                B11[k]=B1[BS[i]]
                B22[k]=B2[BS[i]]
                B33[k]=B3[BS[i]]
        W1=numpy.copy(W11)
        W2=numpy.copy(W22)
        W3=numpy.copy(W33)
        B1=numpy.copy(B11)
        B2=numpy.copy(B22)
        B3=numpy.copy(B33)
file = open('W1'+str(i+1)+'.pkl','wb')
pickle.dump(W1B,file)
file.close()
file = open('W2'+str(i+1)+'.pkl','wb')
pickle.dump(W2B,file)
file.close()
file = open('W3'+str(i+1)+'.pkl','wb')
pickle.dump(W3B,file)
file.close()
file = open('B1'+str(i+1)+'.pkl','wb')
pickle.dump(B1B,file)
file.close()
file = open('B2'+str(i+1)+'.pkl','wb')
pickle.dump(B2B,file)
file.close()
file = open('B3'+str(i+1)+'.pkl','wb')
pickle.dump(B3B,file)
file.close()

plt.plot(X,Y)
plt.xlabel('Generation')
plt.ylabel('Score')
plt.show()

plt.plot(X,Y2)
plt.xlabel('Generation')
plt.ylabel('Average Score')
plt.show()

print(SB)
