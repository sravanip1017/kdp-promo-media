from lib import *
from colorize import colorize
import os
OUT=os.environ.get('KDP_OUT','media/little-boos'); os.makedirs(OUT,exist_ok=True)
W,H=1000,1500
def base(seed): return bg(W,H,seed).convert('RGBA')
def footer(im,line='Little Boos  ·  Ages 4–8'):
    dr=ImageDraw.Draw(im); dr.rectangle((0,H-110,W,H),fill=ORANGE); dr.line((0,H-110,W,H-110),fill=PURPLE_D,width=6)
    dr.text((W/2,H-55),line,font=fred(46),fill=PURPLE_D,anchor='mm')
def head(im,l1,l2=None,y=120,size=108):
    f=fit(l1,chewy,W-90,size); otext(im,(W/2,y),l1,f)
    if l2:
        f2=fit(l2,chewy,W-90,int(size*0.72)); otext(im,(W/2,y+f.size*0.95),l2,f2,fill=WHITE)
def col(n,big=None,seed=0): return colorize(page(n),big,seed)

def save(im,name): im.convert('RGB').save(f'{OUT}/{name}.jpg',quality=90); print(name)

# 1 hero cover
im=base(1); head(im,'Halloween Coloring','& Journal Book for Kids',y=115)
c=card(cover_front(),800,border=0,radius=20); place(im,c,W/2,800)
footer(im,'Ages 4–8  ·  Big, bold lines')
save(im,'pin01-cover')

# 2 before/after
im=base(2); head(im,'Color me in!','Hello, Pumpkin!')
place(im,card(crop_page(page(5)),430),265,760,4)
place(im,card(crop_page(col(5)),430),735,760,-4)
pill(im,265,1195,'before',fred(42),fill=WHITE); pill(im,735,1195,'after',fred(42))
footer(im); save(im,'pin02-before-after')

# 3 picture + journal back
im=base(3); head(im,'Color it, then','write about it!')
place(im,card(crop_page(page(10)),430),690,770,6)
place(im,card(crop_page(col(9)),430),330,780,-5)
pill(im,W/2,1235,'Every picture has a journal page',fred(38),fill=YELLOW)
footer(im); save(im,'pin03-journal')

# 4 trace count write
im=base(4); head(im,'Trace, count','& draw too!')
for i,(n,x,a) in enumerate([(8,210,7),(16,500,0),(12,790,-7)]):
    place(im,card(crop_page(page(n)),330),x,760+(0 if i==1 else 40),a)
pill(im,W/2,1230,'Early learning, spooky-cute',fred(40),fill=YELLOW)
footer(im); save(im,'pin04-activities')

# 5 rainy day
im=base(5); head(im,'Screen-free','Halloween fun')
place(im,card(crop_page(col(29,seed=3)),600),W/2,790,-2)
footer(im,'Rainy-day activity  ·  Ages 4–8'); save(im,'pin05-screen-free')

# 6 grid of 9
im=base(6); head(im,'30 spooky-cute','pictures to color')
ns=[5,7,9,11,17,19,25,27,31]; cw=270
for i,n in enumerate(ns):
    r,cc=divmod(i,3); pg=col(n,seed=i) if i in (0,4,8) else page(n)
    place(im,card(crop_page(pg),cw,border=6,radius=14,shadow=True),190+cc*310,470+r*330,0)
footer(im); save(im,'pin06-grid')

# 7 no bleed
im=base(7); head(im,'Markers welcome!','One picture per sheet')
place(im,card(crop_page(col(37,big=['white','purple','green','yellow'])),560),W/2,800,3)
pill(im,W/2,1240,'No bleed-through onto other pictures',fred(34),fill=YELLOW)
footer(im); save(im,'pin07-markers')

# 8 gift
im=base(8); head(im,'Boo basket','gift idea!')
place(im,card(cover_front(),620,border=0,radius=16),W/2+70,790,-4)
place(im,card(crop_page(col(31,seed=2)),330),230,1010,8)
pill(im,W/2,1250,'Party favor · Class gift · Boo basket',fred(34),fill=YELLOW)
footer(im); save(im,'pin08-gift')
