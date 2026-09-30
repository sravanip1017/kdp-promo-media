import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
S=os.environ.get('KDP_WORK','/tmp/kdp-work')
F=os.environ.get('KDP_FONTS','/tmp/kdp-fonts/')
ORANGE=(255,140,26); PURPLE_D=(58,28,110); PURPLE=(98,52,170); YELLOW=(255,214,79); WHITE=(255,255,255)
def chewy(sz): return ImageFont.truetype(F+'Chewy.ttf', sz)
def fred(sz, w='Bold'):
    f=ImageFont.truetype(F+'Fredoka.ttf', sz); f.set_variation_by_name(w); return f
_pages={}
def page(n):
    if n not in _pages: _pages[n]=Image.open(f'{S}/hi/p-{n:02d}.png').convert('RGB')
    return _pages[n]
def crop_page(im):
    # trim outer white margin a bit
    w,h=im.size; m=int(w*0.03); return im.crop((m,m,w-m,h-m))
def cover_front():
    c=Image.open(f'{S}/hi/cover-1.png').convert('RGB'); w,h=c.size
    return c.crop((int(w*0.525),0,w,h))
def bg(W,H,seed=1,moon=True):
    y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
    d=np.sqrt((x-0.75)**2+(y-0.15)**2)
    t=np.clip(d/1.1,0,1)[...,None]
    top=np.array([124,72,200]); bot=np.array([40,16,84])
    arr=(top*(1-t)+bot*t).astype(np.uint8)
    im=Image.fromarray(arr,'RGB'); dr=ImageDraw.Draw(im); rnd=random.Random(seed)
    for _ in range(int(W*H/22000)):
        cx,cy=rnd.uniform(0,W),rnd.uniform(0,H); r=rnd.uniform(W*0.006,W*0.014)
        star(dr,cx,cy,r)
    return im
def star(dr,cx,cy,r,fill=YELLOW,outline=(20,10,40)):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.45
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    dr.polygon(pts,fill=fill,outline=outline,width=max(1,int(r*0.18)))
def otext(im,xy,text,font,fill=ORANGE,stroke=PURPLE_D,sw=None,anchor='mm',shadow=True):
    dr=ImageDraw.Draw(im); sw=sw or max(2,font.size//9)
    if shadow:
        dr.text((xy[0]+font.size*0.05,xy[1]+font.size*0.07),text,font=font,fill=(20,8,45),stroke_width=sw,stroke_fill=(20,8,45),anchor=anchor)
    dr.text(xy,text,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke,anchor=anchor)
def fit(text,maker,maxw,start):
    s=start
    while s>10:
        f=maker(s)
        if f.getlength(text)<=maxw: return f
        s-=2
    return maker(s)
def card(im, w, border=10, radius=24, shadow=True):
    """Return RGBA card of page image scaled to width w with white rounded border and drop shadow."""
    h=int(im.height*w/im.width); p=im.resize((w,h),Image.LANCZOS)
    cw,ch=w+2*border,h+2*border; pad=40
    out=Image.new('RGBA',(cw+2*pad,ch+2*pad),(0,0,0,0))
    if shadow:
        sh=Image.new('RGBA',out.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((pad+8,pad+14,pad+cw+8,pad+ch+14),radius,fill=(10,0,30,150))
        out=Image.alpha_composite(out,sh.filter(ImageFilter.GaussianBlur(14)))
    body=Image.new('RGBA',out.size,(0,0,0,0)); ImageDraw.Draw(body).rounded_rectangle((pad,pad,pad+cw,pad+ch),radius,fill=WHITE)
    out=Image.alpha_composite(out,body); out.paste(p,(pad+border,pad+border))
    return out
def place(base,rgba,cx,cy,angle=0,scale=1.0):
    r=rgba
    if scale!=1.0: r=r.resize((max(1,int(r.width*scale)),max(1,int(r.height*scale))),Image.LANCZOS)
    if angle: r=r.rotate(angle,resample=Image.BICUBIC,expand=True)
    base.alpha_composite(r,(int(cx-r.width/2),int(cy-r.height/2)))
def pill(im,cx,cy,text,font,fill=ORANGE,fg=PURPLE_D,padx=34,pady=16,outline=PURPLE_D):
    dr=ImageDraw.Draw(im); w=font.getlength(text); h=font.size
    dr.rounded_rectangle((cx-w/2-padx,cy-h/2-pady,cx+w/2+padx,cy+h/2+pady),radius=h,fill=fill,outline=outline,width=5)
    dr.text((cx,cy),text,font=font,fill=fg,anchor='mm')
def burst(im,cx,cy,r,lines,font):
    dr=ImageDraw.Draw(im); pts=[]
    for i in range(32):
        a=i*math.pi/16; rr=r if i%2==0 else r*0.85; pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    dr.polygon(pts,fill=YELLOW,outline=PURPLE_D,width=5)
    lh=font.size*1.05; y0=cy-lh*(len(lines)-1)/2
    for i,l in enumerate(lines): dr.text((cx,y0+i*lh),l,font=font,fill=PURPLE_D,anchor='mm')
