from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
WWW=ROOT/'www'
ANDROID=ROOT/'android/app/src/main/res'
BG=(255,151,15); PANEL=(255,247,239); OUT=(42,33,30); WHITE=(255,255,255); PINK=(255,176,167); YELLOW=(255,190,74)

def remove_adaptive_icons():
    adaptive=ANDROID/'mipmap-anydpi-v26'
    for name in ('ic_launcher.xml','ic_launcher_round.xml'):
        p=adaptive/name
        if p.exists():
            p.unlink()

def icon(size,round_=False):
    im=Image.new('RGBA',(size,size),BG+(255,));d=ImageDraw.Draw(im);r=size//2 if round_ else size//5
    m=Image.new('L',(size,size),0);ImageDraw.Draw(m).rounded_rectangle((0,0,size,size),radius=r,fill=255);im.putalpha(m)
    d.rounded_rectangle((size*.10,size*.10,size*.90,size*.90),radius=size*.16,fill=PANEL+(255,))
    d.rounded_rectangle((size*.22,size*.18,size*.78,size*.66),radius=size*.17,fill=WHITE+(255,),outline=OUT+(255,),width=max(4,size//30))
    d.pieslice((size*.26,size*.12,size*.43,size*.28),180,360,fill=WHITE+(255,),outline=OUT+(255,),width=max(3,size//34))
    d.ellipse((size*.37,size*.38,size*.43,size*.48),fill=OUT+(255,));d.line((size*.58,size*.43,size*.65,size*.40),fill=OUT+(255,),width=max(3,size//38))
    d.arc((size*.41,size*.45,size*.59,size*.59),10,170,fill=OUT+(255,),width=max(3,size//38));d.ellipse((size*.28,size*.49,size*.36,size*.56),fill=PINK+(255,));d.ellipse((size*.64,size*.49,size*.72,size*.56),fill=PINK+(255,))
    d.rounded_rectangle((size*.72,size*.15,size*.76,size*.27),radius=max(1,size//80),fill=YELLOW+(255,));d.rounded_rectangle((size*.80,size*.19,size*.84,size*.29),radius=max(1,size//80),fill=YELLOW+(255,))
    by0,by1=int(size*.64),int(size*.87);bx0,bx1=int(size*.24),int(size*.76)
    d.rounded_rectangle((bx0,by0,bx1,by1),radius=int(size*.07),fill=WHITE+(255,),outline=OUT+(255,),width=max(3,size//32))
    w=max(4,size//22);x=int(size*.38);d.rounded_rectangle((x,int(size*.69),x+w,int(size*.82)),radius=max(1,w//2),fill=OUT+(255,))
    d.ellipse((int(size*.51),int(size*.69),int(size*.66),int(size*.82)),outline=OUT+(255,),width=max(4,size//28))
    return im

remove_adaptive_icons()
for folder,s in {'mipmap-mdpi':48,'mipmap-hdpi':72,'mipmap-xhdpi':96,'mipmap-xxhdpi':144,'mipmap-xxxhdpi':192}.items():
    p=ANDROID/folder;p.mkdir(parents=True,exist_ok=True);icon(s).save(p/'ic_launcher.png');icon(s,True).save(p/'ic_launcher_round.png')
WWW.mkdir(parents=True,exist_ok=True);icon(192).save(WWW/'icon-192.png');icon(512).save(WWW/'icon-512.png')
print('Generated forced 10-second game launcher icons.')