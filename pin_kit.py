import json, subprocess, os, html
e=html.escape
F='/usr/share/fonts/truetype/google-fonts/'
FONTS=f'''@font-face{{font-family:Lora;src:url(file://{F}Lora-Variable.ttf);font-weight:400 700}}
@font-face{{font-family:Poppins;src:url(file://{F}Poppins-Regular.ttf);font-weight:400}}@font-face{{font-family:Poppins;src:url(file://{F}Poppins-Medium.ttf);font-weight:500}}
@font-face{{font-family:Poppins;src:url(file://{F}Poppins-Bold.ttf);font-weight:600 800}}
@font-face{{font-family:Anton;src:url(file://{F}ofl/anton/Anton-Regular.ttf)}}@font-face{{font-family:Archivo;src:url(file://{F}ofl/archivoblack/ArchivoBlack-Regular.ttf)}}
@font-face{{font-family:Montserrat;src:url("file://{F}ofl/montserrat/Montserrat[wght].ttf");font-weight:100 900}}@font-face{{font-family:Gelasio;src:url("file://{F}ofl/gelasio/Gelasio[wght].ttf");font-weight:400 700}}'''
KIT=os.path.dirname(os.path.abspath(__file__))
OUTDIR=os.environ.get('PIN_OUT','/tmp/pins_out'); os.makedirs(OUTDIR,exist_ok=True)
RECIPES=json.load(open(os.path.join(KIT,'recipes.json')))
def R(n,i): return next(x for x in RECIPES if x['book']==n and x['id']==i)
def img(n,i): return 'file://'+os.path.join(KIT,'photos',f'b{n}_{i:02d}.jpg')
def cover(n): return 'file://'+os.path.join(KIT,'photos',f'b{n}_cover.jpg')
LOGO='file://'+os.path.join(KIT,'logo.png')
URL='everydaymealsco.netlify.app'
BASE=f'''*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1000px;height:1500px;overflow:hidden}}body{{font-family:Poppins;color:#3a2a22;background:#fdf1e1;position:relative}}'''
def render(name,css,body):
    p=os.path.join(OUTDIR,name+'.html')
    open(p,'w').write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONTS}{BASE}{css}</style></head><body>{body}</body></html>')
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files','--force-device-scale-factor=1','--window-size=1000,1500',f'--screenshot={OUTDIR}/{name}.png',f'file://{p}'],capture_output=True)
    return f'{OUTDIR}/{name}.png'

# STYLE A1: hero photo + cream band bottom
def heroA(name,n,i,title,sub,tag):
    css='''.ph{position:absolute;inset:0 0 430px 0;background-size:cover;background-position:center}
    .band{position:absolute;left:0;right:0;bottom:0;height:470px;background:#fdf1e1;border-radius:46px 46px 0 0;padding:58px 70px 0;text-align:center}
    .tag{display:inline-block;background:#b83e28;color:#fff;font-weight:600;font-size:26px;letter-spacing:.14em;padding:10px 28px;border-radius:999px;margin-bottom:24px}
    h1{font-family:Lora;font-weight:700;font-size:86px;line-height:1.02;margin-bottom:20px}.sub{font-size:31px;color:#6b5a50}
    .ft{position:absolute;bottom:34px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:18px;font-size:22px;color:#8a776b}.ft img{height:52px}'''
    body=f'<div class="ph" style="background-image:url({img(n,i)})"></div><div class="band"><div class="tag">{e(tag)}</div><h1>{e(title)}</h1><div class="sub">{e(sub)}</div><div class="ft"><img src="{LOGO}"><span>{URL}</span></div></div>'
    return render(name,css,body)
# STYLE A2: full bleed photo, dark gradient, title top white
def heroA2(name,n,i,kicker,title,sub):
    css='''.ph{position:absolute;inset:0;background-size:cover;background-position:center}.g{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,12,8,.82) 0%,rgba(20,12,8,.35) 36%,rgba(0,0,0,0) 55%,rgba(0,0,0,0) 78%,rgba(20,12,8,.6) 100%)}
    .t{position:absolute;top:80px;left:70px;right:70px;color:#fff}.k{font-family:Montserrat;font-weight:800;font-size:30px;letter-spacing:.24em;color:#ffd7a8;margin-bottom:18px}
    h1{font-family:Gelasio;font-weight:700;font-size:96px;line-height:1.02;text-shadow:0 4px 30px rgba(0,0,0,.4)}.s{font-size:32px;margin-top:20px;opacity:.95}
    .ft{position:absolute;bottom:40px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;color:#fff;font-size:24px}.ft .l{background:#fdf1e1;border-radius:18px;padding:10px 16px}.ft img{height:48px;display:block}'''
    body=f'<div class="ph" style="background-image:url({img(n,i)})"></div><div class="g"></div><div class="t"><div class="k">{e(kicker)}</div><h1>{e(title)}</h1><div class="s">{e(sub)}</div></div><div class="ft"><div class="l"><img src="{LOGO}"></div><span>{URL}</span></div>'
    return render(name,css,body)
# STYLE B: collage roundup with big number band
def roundup(name,items,num,line1,line2,color='#b83e28'):
    tiles=''.join(f'<div style="background-image:url({u})"></div>' for u in items[:6])
    css=f'''.grid{{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:8px;background:#fdf1e1}}.grid div{{background-size:cover;background-position:center}}
    .band{{position:absolute;left:50px;right:50px;top:470px;background:#fdf1e1;border-radius:34px;padding:34px 40px 36px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.35)}}
    .num{{font-family:Archivo;font-size:190px;line-height:.9;color:{color}}}.l1{{font-family:Archivo;font-size:66px;line-height:1.05;text-transform:uppercase;margin-top:6px}}
    .l2{{font-family:Lora;font-style:italic;font-size:40px;color:#6b5a50;margin-top:14px}}.ft{{margin-top:20px;display:flex;justify-content:center;align-items:center;gap:14px;font-size:22px;color:#8a776b}}.ft img{{height:46px}}'''
    body=f'<div class="grid">{tiles}</div><div class="band"><div class="num">{num}</div><div class="l1">{e(line1)}</div><div class="l2">{e(line2)}</div><div class="ft"><img src="{LOGO}"><span>{URL}</span></div></div>'
    return render(name,css,body)
# STYLE C: infographic list
def infolist(name,title,subtitle,rows,accent='#5f7f35',footer='Get all 25 recipes in the ebook'):
    rws=''.join(f'<div class="r"><div class="i" style="background-image:url({u})"></div><div class="n">{k+1}</div><div class="tx"><b>{e(t)}</b><span>{e(m)}</span></div></div>' for k,(u,t,m) in enumerate(rows))
    css=f'''body{{background:#fffaf2;padding:56px 54px}}h1{{font-family:Archivo;font-size:76px;line-height:1;text-align:center;text-transform:uppercase}}h1 em{{font-style:normal;color:{accent}}}
    .st{{text-align:center;font-family:Lora;font-style:italic;font-size:34px;color:#6b5a50;margin:14px 0 28px}}.rows{{display:grid;grid-template-columns:1fr 1fr;gap:18px 22px}}
    .r{{display:flex;align-items:center;gap:14px;background:#fdf1e1;border-radius:20px;padding:12px;position:relative}}.i{{width:150px;height:160px;border-radius:16px;background-size:cover;background-position:center;flex:none}}
    .n{{position:absolute;left:4px;top:4px;width:46px;height:46px;border-radius:50%;background:{accent};color:#fff;font-weight:700;font-size:22px;display:flex;align-items:center;justify-content:center}}
    .tx b{{display:block;font-family:Lora;font-size:29px;line-height:1.12}}.tx span{{display:inline-block;margin-top:10px;font-weight:600;font-size:24px;color:#fff;background:{accent};padding:3px 14px;border-radius:999px}}
    .ft{{position:absolute;bottom:44px;left:54px;right:54px;display:flex;justify-content:space-between;align-items:center;font-size:24px;color:#6b5a50}}.ft img{{height:56px}}.ft b{{color:#3a2a22}}'''
    body=f'<h1>{title}</h1><div class="st">{e(subtitle)}</div><div class="rows">{rws}</div><div class="ft"><img src="{LOGO}"><span><b>{e(footer)}</b> · {URL}</span></div>'
    return render(name,css,body)
# STYLE D: magazine cover
def magazine(name,bg,top,big,lines,badge):
    ls=''.join(f'<div>{e(x)}</div>' for x in lines)
    css='''.ph{position:absolute;inset:0;background-size:cover;background-position:center}.g{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0) 40%,rgba(0,0,0,0) 60%,rgba(0,0,0,.65))}
    .top{position:absolute;top:50px;left:60px;right:60px;color:#fff;font-family:Montserrat;font-weight:800;letter-spacing:.3em;font-size:28px;border-bottom:3px solid #fff;padding-bottom:16px}
    .big{position:absolute;top:120px;left:52px;right:52px;font-family:Anton;font-size:178px;line-height:.92;color:#fff;text-transform:uppercase;text-shadow:0 6px 30px rgba(0,0,0,.35)}
    .lines{position:absolute;left:60px;bottom:150px;color:#fff;font-family:Montserrat;font-weight:700;font-size:38px;line-height:1.35;text-shadow:0 3px 14px rgba(0,0,0,.5)}.lines div:before{content:"› ";color:#ffd7a8}
    .badge{position:absolute;right:56px;bottom:150px;width:210px;height:210px;border-radius:50%;background:#b83e28;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:Montserrat;font-weight:800;font-size:28px;line-height:1.05;box-shadow:0 10px 30px rgba(0,0,0,.4)}.badge b{font-family:Anton;font-weight:400;font-size:84px}
    .ft{position:absolute;bottom:40px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center;color:#fff;font-size:24px}.ft .l{background:#fdf1e1;border-radius:16px;padding:8px 14px}.ft img{height:46px;display:block}'''
    body=f'<div class="ph" style="background-image:url({bg})"></div><div class="g"></div><div class="top">{e(top)}</div><div class="big">{big}</div><div class="lines">{ls}</div><div class="badge"><b>{badge[0]}</b>{badge[1]}</div><div class="ft"><div class="l"><img src="{LOGO}"></div><span>{URL}</span></div>'
    return render(name,css,body)
# STYLE E: recipe card
def card(name,n,i,title,tagline):
    r=R(n,i); ing=r['ingredients'][:10]; st=r['steps'][:5]
    css='''body{background:#5f7f35;padding:44px}.c{background:#fffaf2;border-radius:34px;height:100%;padding:44px 44px 36px;position:relative}
    .top{display:flex;gap:30px}.ph{width:400px;height:560px;border-radius:24px;background-size:cover;background-position:center;flex:none}
    .k{font-weight:600;letter-spacing:.2em;font-size:22px;color:#b83e28}h1{font-family:Lora;font-size:64px;line-height:1.05;margin:12px 0 16px}.tl{font-size:26px;color:#6b5a50;margin-bottom:18px}
    .ch span{display:inline-block;background:#fdf1e1;border-radius:999px;padding:6px 16px;font-size:21px;font-weight:600;margin:0 8px 10px 0}
    h3{font-family:Lora;font-size:32px;color:#b83e28;margin:26px 0 10px}ul{columns:2;column-gap:30px;padding-left:24px;font-size:23px;line-height:1.4}ol{padding-left:30px;font-size:22px;line-height:1.38}li{margin-bottom:4px}
    .ft{position:absolute;bottom:28px;left:44px;right:44px;display:flex;justify-content:space-between;align-items:center;font-size:22px;color:#8a776b}.ft img{height:50px}.ft b{color:#b83e28}'''
    tot=r['prep']+r['cook']
    body=f'''<div class="c"><div class="top"><div class="ph" style="background-image:url({img(n,i)})"></div><div><div class="k">SAVE THIS RECIPE</div><h1>{e(title)}</h1><div class="tl">{e(tagline)}</div>
    <div class="ch"><span>⏱ {tot} min</span><span>🍽 Serves {r['serves']}</span>{''.join(f'<span>{e(x)}</span>' for x in r.get('chips',[]))}</div></div></div>
    <h3>Ingredients</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in ing)}</ul><h3>How to make it</h3><ol>{''.join(f'<li>{e(x if len(x)<120 else x[:117].rsplit(" ",1)[0]+"…")}</li>' for x in st)}</ol>
    <div class="ft"><img src="{LOGO}"><span><b>Full recipe</b> · {URL}</span></div></div>'''
    return render(name,css,body)
# STYLE F: cost
def cost(name,n,i,price,title,serves):
    r=R(n,i)
    css='''body{background:#f6e3c8}.ph{position:absolute;top:60px;left:60px;right:60px;height:760px;border-radius:30px;background-size:cover;background-position:center;box-shadow:0 20px 50px rgba(58,42,34,.25)}
    .price{position:absolute;top:640px;right:90px;width:250px;height:250px;border-radius:50%;background:#b83e28;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:26px;letter-spacing:.08em;box-shadow:0 14px 40px rgba(0,0,0,.3);transform:rotate(-8deg)}.price b{font-family:Archivo;font-size:96px;line-height:1;letter-spacing:0}
    .t{position:absolute;top:870px;left:70px;right:70px}.k{font-family:Montserrat;font-weight:800;font-size:30px;letter-spacing:.18em;color:#5f7f35}h1{font-family:Lora;font-weight:700;font-size:84px;line-height:1.03;margin:14px 0 18px}
    .s{font-size:31px;color:#6b5a50}.ft{position:absolute;bottom:44px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;font-size:24px;color:#8a776b}.ft img{height:54px}'''
    body=f'<div class="ph" style="background-image:url({img(n,i)})"></div><div class="price">ABOUT<b>{price}</b>TOTAL</div><div class="t"><div class="k">FEEDS {serves} ON A BUDGET</div><h1>{e(title)}</h1><div class="s">One pot, pantry staples and {r["prep"]+r["cook"]} minutes. Full recipe on our site.</div></div><div class="ft"><img src="{LOGO}"><span>{URL}</span></div>'
    return render(name,css,body)


# STYLE G: one-week dinner plan (7 days, links to free guide or a book)
def weekplan(name,title,subtitle,items,accent='#b83e28',footer='Free printable meal plan'):
    days=['MON','TUE','WED','THU','FRI','SAT','SUN']
    rows=''.join(f'<div class="r"><div class="d">{d}</div><div class="i" style="background-image:url({u})"></div><div class="t">{e(t)}</div></div>' for d,(u,t) in zip(days,items))
    css=f'''body{{background:#fdf1e1;padding:54px 56px}}h1{{font-family:Lora;font-size:74px;line-height:1.02;text-align:center}}h1 em{{font-style:normal;color:{accent}}}
    .st{{text-align:center;font-size:30px;color:#6b5a50;margin:12px 0 26px}}.r{{display:flex;align-items:center;gap:22px;background:#fffaf2;border-radius:22px;padding:12px 20px;margin-bottom:14px}}
    .d{{width:96px;font-family:Montserrat;font-weight:800;font-size:30px;color:{accent};letter-spacing:.08em}}.i{{width:170px;height:128px;border-radius:14px;background-size:cover;background-position:center;flex:none}}
    .t{{font-family:Lora;font-weight:600;font-size:40px;line-height:1.1}}.ft{{position:absolute;bottom:40px;left:56px;right:56px;display:flex;justify-content:space-between;align-items:center;font-size:24px;color:#6b5a50}}.ft img{{height:56px}}.ft b{{color:#3a2a22}}'''
    body=f'<h1>{title}</h1><div class="st">{e(subtitle)}</div>{rows}<div class="ft"><img src="{LOGO}"><span><b>{e(footer)}</b> · {URL}</span></div>'
    return render(name,css,body)

if __name__=='__main__':
    # quick self-test: render one pin of each style
    heroA('test_heroA',1,25,'Korean Ground Beef Bowls','Ready in 17 minutes','17-MINUTE DINNER')
    heroA2('test_heroA2',4,25,'HIGH-PROTEIN DINNER','Cottage Cheese Lasagna Bake','~42g protein per serving')
    roundup('test_roundup',[img(1,i) for i in (1,3,18,5,21,24)],'6','Chicken Dinners','easy weeknight ideas')
    infolist('test_info','10 <em>Test</em> Dinners','subtitle',[(img(4,i),R(4,i)['name'],R(4,i)['chips'][0]) for i in range(1,11)])
    magazine('test_mag',cover(2),'EVERYDAY MEALS CO.','Test<br>Cover',['line one','line two'],('25','RECIPES'))
    card('test_card',1,2,'15-Minute Beef & Broccoli','Better than takeout')
    cost('test_cost',3,1,'$9','One-Pot Cheesy Chicken & Rice','4')
    weekplan('test_week','A Week of <em>Easy</em> Dinners','7 cheap family meals, planned for you',[(img(1,2),'Beef & Broccoli'),(img(1,4),'Taco Skillet'),(img(3,1),'Cheesy Chicken & Rice'),(img(3,12),'Goulash'),(img(1,16),'Tortellini Soup'),(img(3,18),'Black Bean Quesadillas'),(img(3,20),'Egg Fried Rice')])
    print('ok', OUTDIR)
