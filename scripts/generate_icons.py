from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / 'www'
ANDROID = ROOT / 'android' / 'app' / 'src' / 'main' / 'res'
BG_TOP=(255,181,76); BG_BOTTOM=(255,151,15); PANEL=(255,247,239); LINE=(242,210,173); OUT=(42,33,30); WHITE=(255,255,255); PINK=(255,176,167); TONGUE=(255,112,112); YELLOW=(255,190,74)

def gradient_bg(size):
    img=Image.new('RGBA',(size,size),(0,0,0,0)); d=ImageDraw.Draw(img)
    for y in range(size):
        r=y/max(size-1,1); c=tuple(int(BG_TOP[i]*(1-r)+BG_BOTTOM[i]*r) for i in range(3))+(255,); d.line([(0,y),(size,y)],fill=c)
    return img

def draw_ten_badge(draw,size):
    # Geometric 10 mark: readable even on small Android launchers without font dependencies.
    y=int(size*.68); h=int(size*.14); x=int(size*.54); w=max(4,size//24)
    draw.rounded_rectangle((x,y,x+w,y+h),radius=max(1,w//2),fill=OUT)
    draw.ellipse((int(size*.63),y,int(size*.78),y+h),outline=OUT,width=max(3,size//30))

def make_icon(size,rounded=False):
    img=gradient_bg(size); d=ImageDraw.Draw(img)
    mask=Image.new('L',(size,size),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,size,size),radius=size//2 if rounded else size//5,fill=255); img.putalpha(mask)
    pad=int(size*.13); d.rounded_rectangle((pad,pad,size-pad,size-pad),radius=int(size*.12),fill=PANEL,outline=LINE,width=max(2,size//64))
    d.rounded_rectangle((int(size*.24),int(size*.20),int(size*.76),int(size*.68)),radius=int(size*.16),fill=WHITE,outline=OUT,width=max(4,size//32))
    d.pieslice((int(size*.27),int(size*.14),int(size*.42),int(size*.27)),180,360,fill=WHITE,outline=OUT,width=max(4,size//32))
    ew=size*.035; eh=size*.05; d.ellipse((size*.38-ew,size*.42-eh,size*.38+ew,size*.42+eh),fill=OUT); d.line((size*.57,size*.43,size*.63,size*.40),fill=OUT,width=max(4,size//40))
    d.arc((size*.42,size*.44,size*.58,size*.58),10,170,fill=OUT,width=max(4,size//40)); d.rounded_rectangle((size*.49,size*.51,size*.55,size*.59),radius=int(size*.02),fill=TONGUE,outline=OUT,width=max(2,size//64))
    d.ellipse((size*.27,size*.49,size*.36,size*.56),fill=PINK); d.ellipse((size*.64,size*.49,size*.73,size*.56),fill=PINK)
    d.ellipse((size*.21,size*.56,size*.31,size*.66),fill=WHITE,outline=OUT,width=max(4,size//40)); d.ellipse((size*.69,size*.56,size*.79,size*.66),fill=WHITE,outline=OUT,width=max(4,size//40))
    d.rounded_rectangle((size*.71,size*.17,size*.75,size*.28),radius=int(size*.01),fill=YELLOW); d.rounded_rectangle((size*.79,size*.19,size*.83,size*.27),radius=int(size*.01),fill=YELLOW)
    draw_ten_badge(d,size)
    return img

def save_web_icons():
    WWW.mkdir(parents=True,exist_ok=True); make_icon(192).save(WWW/'icon-192.png'); make_icon(512).save(WWW/'icon-512.png')

def save_android_icons():
    for folder,size in {'mipmap-mdpi':48,'mipmap-hdpi':72,'mipmap-xhdpi':96,'mipmap-xxhdpi':144,'mipmap-xxxhdpi':192}.items():
        target=ANDROID/folder; target.mkdir(parents=True,exist_ok=True); make_icon(size).save(target/'ic_launcher.png'); make_icon(size,True).save(target/'ic_launcher_round.png')

if __name__=='__main__':
    save_web_icons(); save_android_icons(); print('Generated branded 10-second game icons.')