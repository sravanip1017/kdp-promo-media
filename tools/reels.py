import os
import sys, subprocess, numpy as np, math
from lib import *
from colorize import colorize
from music import track
Wv,Hv,FPS=1080,1920,30
OUT=os.environ.get('KDP_OUT','media/little-boos'); os.makedirs(OUT,exist_ok=True)
BG=bg(Wv,Hv,11).convert('RGBA')
def ease(x): x=min(1,max(0,x)); return 1-(1-x)**3
def pop(x): x=min(1,max(0,x)); return 1+0.12*math.sin(math.pi*x)*(1-x) if x<1 else 1
def hook(im,l1,l2=None,y=230,a=1.0):
    f=fit(l1,chewy,Wv-80,120); otext(im,(Wv/2,y),l1,f)
    if l2: f2=fit(l2,chewy,Wv-80,86); otext(im,(Wv/2,y+f.size),l2,f2,fill=WHITE)
COVER=card(cover_front(),780,border=0,radius=22)
def endcard(im,p):
    s=0.6+0.4*ease(p*2.2); place(im,COVER,Wv/2,900,0,s*pop(p*2))
    if p>0.25:
        otext(im,(Wv/2,1540),'Little Boos',chewy(120))
        dr=ImageDraw.Draw(im); dr.text((Wv/2,1650),'Halloween Coloring & Journal Book',font=fred(48),fill=WHITE,anchor='mm')
    if p>0.4: pill(im,Wv/2,1780,'Ages 4–8  ·  Link in bio',fred(52),fill=YELLOW)
def reveal_mask(w,h,p,soft=60):
    yy,xx=np.mgrid[0:h,0:w]; v=(yy+xx*0.35)/(h+w*0.35)
    m=np.clip((p*(1+soft/h)-v)*h/soft,0,1); return Image.fromarray((m*255).astype(np.uint8))
def render(name,seconds,fn,seed):
    wav=f'{S}/{name}.wav'; track(seconds,wav,seed)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{Wv}x{Hv}','-r',str(FPS),'-i','-','-i',wav,
         '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',f'{OUT}/{name}.mp4']
    pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(int(seconds*FPS)):
        im=BG.copy(); fn(im,i/FPS); pr.stdin.write(im.convert('RGB').tobytes())
    pr.stdin.close(); pr.wait(); print(name, pr.returncode)

# ---------- Reel A: coloring reveal ----------
def reelA():
    items=[(5,None,0),(37,['white','purple','green','yellow'],1),(9,None,2)]
    cw=900; prepared=[]
    for n,big,sd in items:
        line=crop_page(page(n)); colr=crop_page(colorize(page(n),big,sd))
        h=int(line.height*cw/line.width)
        prepared.append((line.resize((cw,h),Image.LANCZOS),colr.resize((cw,h),Image.LANCZOS)))
    seg=3.3; start=0.6
    def fn(im,t):
        if t<start+seg*3:
            k=min(2,int(max(0,t-start)//seg)); lt=(t-start)-k*seg if t>=start else 0
            line,colr=prepared[k]; p=ease((lt-0.5)/2.2) if t>=start else 0
            pg=line.copy()
            if p>0: pg.paste(colr,(0,0),reveal_mask(*line.size,p))
            c=card(pg,cw,border=12,radius=26); sc=0.92+0.08*ease(lt/0.4) if k>0 else 1
            place(im,c,Wv/2,1070,[-2,2,-1][k],sc)
            hook(im,'Watch them color','themselves in!' if k==0 else ['','Ghost Family!','Witchy Kitty!'][k],y=210)
            if 0<p<1:  # crayon dot at reveal edge
                dr=ImageDraw.Draw(im); x=Wv/2-cw/2+cw*min(1,p*1.3); y=1070-line.height/2+line.height*p
                dr.ellipse((x-26,y-26,x+26,y+26),fill=ORANGE,outline=PURPLE_D,width=6)
        else:
            endcard(im,(t-(start+seg*3))/3.2)
    render('reel01-color-reveal',start+seg*3+3.4,fn,1)

# ---------- Reel B: flip-through ----------
def reelB():
    seq=[(5,'color'),(6,'journal'),(8,'trace'),(16,'count'),(25,'color'),(26,'journal'),(29,'color'),(35,'color'),(42,'color'),(65,'award')]
    cw=820; cards=[]
    for i,(n,lab) in enumerate(seq):
        pg=crop_page(colorize(page(n),None,i) if lab=='color' and i in (0,6) else page(n))
        cards.append((card(pg,cw,border=12,radius=26),lab))
    step=0.95; t0=1.0
    def fn(im,t):
        T=t0+step*len(seq)
        if t<T:
            hook(im,"What's inside?",'Little Boos Halloween book',y=210)
            k=int(max(0,t-t0)//step) if t>=t0 else -1
            for j in range(max(0,k-2),k+1):
                c,lab=cards[j]; lt=(t-t0)-j*step; p=ease(lt/0.45)
                x=Wv/2+(1-p)*Wv; ang=[-4,3,-2,4,-3][j%5]
                place(im,c,x,1080,ang)
            if k>=0:
                lab=cards[k][1]; txt={'color':'Color it!','journal':'Write & draw','trace':'Trace words','count':'Count & color','award':'Spooky Artist award'}[lab]
                pill(im,Wv/2,1720,txt,fred(58),fill=YELLOW)
            if t<t0: place(im,cards[0][0],Wv/2+Wv*(1-ease(t/t0))*0.0,1080,-4,0.9+0.1*ease(t/t0))
        else: endcard(im,(t-T)/3.2)
    render('reel02-flip-through',t0+step*len(seq)+3.4,fn,2)

# ---------- Reel C: 4 things ----------
def reelC():
    parts=[('1. Color',5,True),('2. Draw',12,False),('3. Trace',8,False),('4. Count',30,False)]
    cw=760; cards=[card(crop_page(colorize(page(n),None,0) if c else page(n)),cw,border=12,radius=26) for _,n,c in parts]
    seg=2.4; t0=1.2
    def fn(im,t):
        T=t0+seg*4
        if t<t0:
            hook(im,'4 things kids','do in this book',y=820+ (1-ease(t/0.5))*60)
        elif t<T:
            k=int((t-t0)//seg); lt=(t-t0)-k*seg
            hook(im,'4 things kids','do in this book',y=210)
            for j in range(k):  # done labels stacked small? show checklist
                pass
            place(im,cards[k],Wv/2,1110+(1-ease(lt/0.4))*500,[-3,3,-2,2][k])
            s=pop(lt/0.5); f=chewy(int(130*s)); otext(im,(Wv/2,520),parts[k][0],f,fill=YELLOW)
        else: endcard(im,(t-T)/3.2)
    render('reel03-four-things',t0+seg*4+3.4,fn,3)

for r in sys.argv[1:]: {'A':reelA,'B':reelB,'C':reelC}[r]()
