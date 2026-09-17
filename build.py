#!/usr/bin/env python3
"""Rick&Linda(9/20)向け 東京フリーデーのコース選択ページ。 python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note を見る。
PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=12'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

COURSES = [
 dict(id='A', chips=['Everything within 2 km of the hotel','Three things off your interest list','No tickets needed'], name='Tsukiji, knives and tea', tag='Market, knives, matcha',
  why='Your interest list has a fish market, knife sharpening and a tea ceremony on it, and none of them are booked anywhere on the trip. All three sit within two kilometres of your hotel, so this is the day that quietly clears the list.',
  steps=[('9:30','Leave the hotel','Ten minutes by taxi, or a flat twenty-five minute walk. Tsukiji wakes up early and is still busy at ten.'),
         ('9:45','Tsukiji Outer Market','Four blocks, around four hundred shops. Tamagoyaki straight off the grill, scallops on the shell, knives, dried bonito, sea urchin. We eat as we walk.'),
         ('11:00','The knife shops','Tsukiji is where Tokyo chefs buy and sharpen their knives. We watch a whetstone in use, you hold a few, and if one fits your hand we get it engraved with your name.'),
         ('12:00','Lunch in the market','See the three picks below.'),
         ('13:30','Hama-rikyu Gardens','Ten minutes on foot. A 400-year-old shogun&rsquo;s garden with saltwater ponds, sitting inside the modern skyline.'),
         ('14:00','Matcha at Nakajima no Ochaya','A tea house standing out over the pond on stilts. Matcha whisked in front of you with a seasonal sweet, sitting on tatami with the water on three sides. The closest thing to a tea ceremony that needs no booking.'),
         ('15:30','Back at the hotel','A twenty-minute walk or a short taxi, in time to pack for Hakone.')],
  stops=['The Blossom Hibiya Tokyo','Tsukiji Outer Market','Hamarikyu Gardens','The Blossom Hibiya Tokyo'],
  moves='Hotel &rarr; Tsukiji 10 min by taxi. Market on foot. Market &rarr; garden 10 min on foot. Garden &rarr; hotel about 20 min on foot.',
  food=[('Tsukiji Tamagoyaki Marutake','Tsukiji &middot; grilled egg on a stick','The egg stand people queue at from nine in the morning. Warm, sweet, a hundred yen, eaten standing up. The right first bite of the market.','Tsukiji Marutake Tamagoyaki'),
        ('Kitsuneya','Tsukiji &middot; beef and offal over rice','A market stall with a few stools, simmering the same pot since the 1940s. The workers&rsquo; breakfast, not a tourist dish.','Kitsuneya Tsukiji'),
        ('Tsukiji Itadori','Tsukiji &middot; seafood bowls, sit-down','If you want a table and a chair rather than a stool: tuna bowls and grilled fish, with a menu in English.','Tsukiji Itadori Honten')],
  good='Three interests in one morning, and almost no train time. Easy to cut short at any point.',
  mind='Sunday closes some of the market, so I check on Saturday which knife shops are open and route us to those. The tea house takes its last order at 16:30.',
  links=[('Tsukiji Outer Market (official)','https://www.tsukiji.or.jp/english/'),('Hama-rikyu Gardens','https://www.tokyo-park.or.jp/teien/en/hama-rikyu/'),('Nakajima no Ochaya','https://www.tokyo-park.or.jp/teien/en/hama-rikyu/facilities.html')]),
 dict(id='B', chips=['Both museums off your list','Indoors, any weather','Warm-up for the sumo in Osaka'], name='Edo Tokyo and Hokusai', tag='Two museums, ten minutes apart',
  why='Your interest list says &ldquo;Edo Tokyo museum / Hokusai museum&rdquo;. They are in the same neighbourhood, a ten-minute walk apart, and Sunday is the day both are open. Ryogoku is also the sumo district, which makes it a useful warm-up for Osaka on the 28th.',
  steps=[('10:00','Leave the hotel','About 25 minutes by train. A late start after the baseball.'),
         ('10:30','Edo-Tokyo Museum','You enter by walking across a full-size replica of the old Nihonbashi bridge, and the city unfolds underneath: a whole Edo street, a tenement house you can step into, then the earthquake, the war and the neon years. Two hours, all indoors, benches and lifts throughout. 800 yen.'),
         ('12:30','Chanko lunch','The stew sumo wrestlers eat to build weight, served in the streets where they train.'),
         ('14:00','Sumida Hokusai Museum','Ten minutes on foot. Hokusai was born here and moved house ninety-three times without leaving the area. The Great Wave, the views of Fuji, and the sketchbooks where you can watch the brush thinking. This is the ink painting on your list, at its source.'),
         ('15:00','Kokugikan and Kyu-Yasuda Garden','The national sumo arena is across the street, with the handprints of past champions outside. The garden beside it is free, small and almost empty.'),
         ('15:45','Back at the hotel','About 25 minutes by train, in time to pack for Hakone.')],
  stops=['The Blossom Hibiya Tokyo','Edo-Tokyo Museum','Sumida Hokusai Museum','Ryogoku Kokugikan','The Blossom Hibiya Tokyo'],
  moves='Hotel &rarr; Ryogoku about 25 min by train. Museum &rarr; lunch 5 min on foot. Lunch &rarr; Hokusai museum 10 min. Hokusai &rarr; arena and garden 8 min. Ryogoku &rarr; hotel about 25 min.',
  food=[('Chanko Kirishima Ryogoku','Ryogoku &middot; chanko hot pot','Run by a former ozeki. The chicken-broth pot is the one his stable actually ate. Reservations help on a Sunday.','Chanko Kirishima Ryogoku'),
        ('Yoshiba','Ryogoku &middot; chanko in an old stable','You eat around the real training ring of the old Miyagino stable, still in the middle of the room. The building alone is worth the walk.','Yoshiba Ryogoku chanko'),
        ('Edo NOREN','Ryogoku Station &middot; food hall','A restored station building with a full-size sumo ring in the middle and a dozen restaurants around it. Good if you each want something different.','Edo NOREN Ryogoku')],
  good='Two things off the interest list in one afternoon, both indoors, both a short walk apart. The best possible preparation for the sumo on Sept 28.',
  mind='Both museums usually close on Mondays, so the 20th is the day this works. Tickets are sold at the door. Nothing here needs booking except the chanko table.',
  links=[('Edo-Tokyo Museum (official)','https://www.edo-tokyo-museum.or.jp/en/'),('Sumida Hokusai Museum (official)','https://hokusai-museum.jp/?lang=en'),('Ryogoku Kokugikan','https://www.sumo.or.jp/EnKokugikan/')]),
 dict(id='C', chips=['Music and dancing, outdoors','Best for the jet lag','No tickets needed'], name='Meiji shrine and a Sunday in the park', tag='Daylight, brass bands, rockabilly',
  why='Music and dance are on your list and nothing else on the trip covers them. Sunday is the one day Yoyogi Park fills with people playing, and the shrine forest next door is the flattest good walk in Tokyo.',
  steps=[('9:30','Leave the hotel','About 20 minutes by train to Harajuku.'),
         ('9:50','Meiji Jingu','A wide gravel path through a man-made forest of 100,000 donated trees, benches the whole way. On a Sunday morning you often catch a wedding procession crossing the courtyard under a red umbrella.'),
         ('11:00','Yoyogi Park','The park next door is where Tokyo goes to practise in public on Sundays: brass bands, drum circles, and the rockabilly dancers who have been meeting at the entrance since the 1980s.'),
         ('12:00','Lunch on Omotesando','Ten minutes on foot, away from the crowd.'),
         ('13:30','Shibuya','The scramble crossing from above, then the quiet back streets. We stop when you have had enough.'),
         ('15:30','Back at the hotel','About 20 minutes by train, in time to pack for Hakone.')],
  stops=['The Blossom Hibiya Tokyo','Meiji Jingu Shrine','Yoyogi Park Tokyo','Omotesando Tokyo','Shibuya Scramble Crossing'],
  moves='Hotel &rarr; Harajuku about 20 min by train. Shrine walk 10 min each way. Park next door. Park &rarr; Omotesando 10 min on foot. Omotesando &rarr; Shibuya 12 min on foot. Shibuya &rarr; hotel about 20 min.',
  food=[('Maisen Aoyama','Omotesando &middot; tonkatsu','Breaded pork cutlet in a converted 1920s bathhouse. Sit-down, quiet, easy to order.','Maisen Aoyama Honten'),
        ('Marion Crepes','Takeshita street &middot; crepes','The stand that started the Harajuku crepe in 1976. Thirty fillings on a photo menu, eaten while walking.','Marion Crepes Takeshita Street Harajuku'),
        ('Uobei Shibuya Dogenzaka','Shibuya &middot; conveyor sushi','You order on a tablet and the plates arrive on a rail at your seat. Cheap, fast, and quietly entertaining.','Uobei Shibuya Dogenzaka')],
  good='Daylight and live music, and nothing to book. Easy to shorten at any point.',
  mind='The Sunday performers are not on a schedule, so they are a bonus rather than a promise. This is the most walking of the three.',
  links=[('Meiji Jingu (official)','https://www.meijijingu.or.jp/en/'),('Yoyogi Park','https://www.tokyo-park.or.jp/park/yoyogi/'),('Shibuya crossing','https://www.google.com/maps/search/?api=1&query=Shibuya+Scramble+Crossing')]),
]

def menu(c):
    x = PH[c['id']]['card']
    ch = ''.join(f'<li>{html.escape(t)}</li>' for t in c['chips'])
    return f'''<button class="mcard" type="button" data-course="{c['id']}" aria-expanded="false" aria-controls="detail-{c['id']}">
<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">
<span class="mb"><span class="mk">Course {c['id']}</span><span class="mt">{html.escape(c['name'])}</span>
<span class="mtag">{html.escape(c['tag'])}</span><ul class="mch">{ch}</ul><span class="mopen">See the plan</span></span></button>'''

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">' for x in PH[c['id']]['detail'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>'
                 for (n, a, d, q), im in zip(c['food'], PH[c['id']]['food']))
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    sub = f'Sept 20 in Tokyo: we choose course {c["id"]} ({c["name"]})'
    return f'''<section class="detail" id="detail-{c['id']}" hidden><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">Course {c['id']} · {html.escape(c['tag'])}</p><h2>{html.escape(c['name'])}</h2></div>
<button class="dclose" type="button" aria-label="Close">Close ✕</button></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div><h3>The day</h3><ol class="steps">{st}</ol></div>
<div><h3>The route</h3><div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p></div>
</div>
<h3>Where we eat</h3><div class="eats">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">Choose course {c['id']}</a>
</div></section>'''

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:62vh;max-height:600px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#9ee3b8}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.slabel{font:inherit;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 13px;cursor:pointer;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dots{display:flex;gap:7px;margin-left:auto;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),lab=document.querySelector('.slabel'),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)});
   lab.textContent='Course '+sl[n].dataset.course+' · '+sl[n].dataset.name;lab.dataset.course=sl[n].dataset.course}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4000)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  lab.addEventListener('click',function(){document.querySelector('.mcard[data-course="'+lab.dataset.course+'"]').click()});
  show(0);go();
 })();
"""

credits = '; '.join(html.escape(x['title'].replace('File:','')) + ' (' + x['lic'] + ')' for v in PH.values() for x in [v['card']] + v['detail'] + v['food'])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sunday in Tokyo: three ways to spend September 20</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2,.mt{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.mcard{{display:flex;flex-direction:column;text-align:left;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;padding:0;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}}
.mcard:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(34,31,27,.10)}}
.menu.picked .mcard:not([aria-expanded=true]){{opacity:.42;filter:saturate(.45)}}
.menu.picked .mcard:not([aria-expanded=true]):hover{{opacity:.75;filter:none}}
.mcard[aria-expanded=true]{{border:2px solid var(--ink);box-shadow:0 12px 28px rgba(17,17,17,.16);transform:translateY(-3px)}}
.mcard[aria-expanded=true] .mopen{{color:var(--acc);border-bottom-color:var(--acc)}}
.mcard>img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#f0ebe0}}
.mb{{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}}
.mk{{display:block;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}}
.mt{{display:block;font-weight:800;font-size:26px;line-height:1.12;letter-spacing:-.025em;margin-bottom:6px}}
.mtag{{display:block;font-size:15px;color:var(--mute);margin-bottom:12px}}
.mch{{list-style:none;margin:auto 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.mch li{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:4px;padding:3px 8px;color:var(--mute)}}
.mopen{{align-self:flex-start;display:inline-block;font-size:14px;font-weight:600;border-bottom:2px solid var(--acc);padding-bottom:1px}}
.mcard[aria-expanded=true] .mopen::after{{content:" ▲"}} .mcard[aria-expanded=false] .mopen::after{{content:" ▾"}}
.detail{{scroll-margin-top:12px;display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease;margin-top:14px;position:relative}}
.detail[hidden]{{display:none}} .detail.open{{grid-template-rows:1fr}}
.dwrap{{overflow:hidden;min-height:0;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.detail::before{{content:'';position:absolute;top:-11px;left:var(--arrow,50%);width:20px;height:20px;margin-left:-10px;background:var(--acc);border-left:2px solid var(--acc);border-top:2px solid var(--acc);transform:rotate(45deg);z-index:2;opacity:0;transition:opacity .2s .12s}}
.detail.open::before{{opacity:1}}
.dtop{{height:5px;background:var(--acc)}}
.detail.open .dwrap{{overflow:visible}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}} .dwrap>.photos{{margin-left:26px;margin-right:26px}}
.dhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding-top:26px}}
.dclose{{flex:none;font:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer}}
.dclose:hover{{color:var(--ink);border-color:var(--ink)}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:640px}}
.photos{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.choose{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:16px 32px;border-radius:8px;font-size:16px;letter-spacing:-.01em;margin-bottom:28px}} .choose:hover{{background:#333}}
.arrival{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:40px}}
.arrival p{{margin:0 0 10px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.arrival .mapbox iframe{{height:260px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .menu{{grid-template-columns:1fr}} .mcard>img{{aspect-ratio:16/9}}
 .dgrid,.eats,.notes,.arrival,.photos{{grid-template-columns:1fr}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:58vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .menu{{gap:12px}}
 .mb{{padding:15px 16px 16px}} .mt{{font-size:23px;line-height:1.15}} .mtag{{font-size:14px;margin-bottom:10px}}
 .mch{{gap:5px;margin-bottom:12px}} .mch li{{font-size:10.5px;padding:2px 7px}}
 .mopen{{font-size:13.5px}}
 h2{{font-size:26px;line-height:1.12}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .choose{{display:block;text-align:center;padding:15px 0;margin-bottom:22px}}
 .arrival{{gap:16px;padding-bottom:32px}} .arrival p{{font-size:15.5px;line-height:1.55}} .arrival .hint{{font-size:14px}}
 .mapbox iframe{{height:210px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{PH[c["id"]]["card"]["thumb"]}" alt="{html.escape(c["name"])}" data-course="{c["id"]}" data-name="{html.escape(c["name"])}">' for c in COURSES)}</div>
<div class="wrap hcap">
<p class="kicker">Tokyo · Sunday, September 20</p>
<h1>Your one free day <span class="nb">in Tokyo.</span></h1>
<div class="snav"><button class="slabel" type="button"></button><div class="dots">{''.join(f'<button type="button" aria-label="Show course {c["id"]}"></button>' for c in COURSES)}</div></div>
</div></div>
<div class="wrap hbody">
<p>Baseball on Saturday, Hakone on Monday morning. Sunday is the only open day on the Tokyo half of your trip, so here are three ways to spend it. Each one is built around something already on your interest list.</p>
<ul class="facts"><li><b>Guide</b> Yuuki</li><li><b>Time</b> about 9:30–15:30</li><li><b>Group</b> Rick and Linda</li><li><b>Start and end</b> The Blossom Hibiya</li></ul>
</div>
</header>
<div class="wrap">
<div class="sechead"><span class="n">1</span><div><b>Pick a course</b> <span>Tap one to see the plan, the route and where we eat.</span></div></div>
<div class="menu">{''.join(menu(c) for c in COURSES)}</div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">2</span><div><b>The weekend around it</b> <span>Saturday and Monday are already fixed, so Sunday is built to fit between them.</span></div></div>
<div class="arrival">
<div><p><b>Sat 19</b> &mdash; 14:00 baseball at Tokyo Dome, dinner at Ginza Kagari.<br><b>Sun 20</b> &mdash; open. This page.<br><b>Mon 21</b> &mdash; 8:04 train from Shimbashi to Hakone.</p>
<p class="hint">Every course ends by about 15:30 so the evening stays free for packing and an early night before the Hakone train. If you would rather rest after the flight and the game, say so and we drop it &mdash; no hard feelings at all.</p></div>
<div class="mapbox"><iframe src="{emb('The Blossom Hibiya Tokyo')}" loading="lazy" title="The Blossom Hibiya and central Tokyo" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div>
<footer class="wrap"><p>Reply to Yuuki with A, B or C &mdash; or with &ldquo;none, we will rest&rdquo;. Times are approximate and can move earlier or later on the day.</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></footer>
<script>
(function(){{
 var cards=[].slice.call(document.querySelectorAll('.mcard'));
 function close(id,now){{var d=document.getElementById('detail-'+id);d.classList.remove('open');document.querySelector('.menu').classList.remove('picked');if(now){{d.hidden=true;return}}setTimeout(function(){{if(!d.classList.contains('open'))d.hidden=true}},320);
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','false')}}
 function land(id){{var d=document.getElementById('detail-'+id),done=false;function go(){{if(done)return;done=true;d.scrollIntoView({{behavior:'smooth',block:'start'}})}}
   d.addEventListener('transitionend',function f(e){{if(e.target===d){{d.removeEventListener('transitionend',f);go()}}}});setTimeout(go,420)}}
 var menuEl=document.querySelector('.menu');
 function point(id){{var b=document.querySelector('.mcard[data-course="'+id+'"]'),d=document.getElementById('detail-'+id);
   var r=b.getBoundingClientRect(),w=d.getBoundingClientRect();
   d.style.setProperty('--arrow',(r.left+r.width/2-w.left)+'px')}}
 function open_(id){{var d=document.getElementById('detail-'+id);d.hidden=false;menuEl.classList.add('picked');
   requestAnimationFrame(function(){{d.classList.add('open');point(id)}});
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','true')}}
 window.addEventListener('resize',function(){{var o=document.querySelector('.mcard[aria-expanded=true]');if(o)point(o.dataset.course)}});
 var want=(location.hash.match(/^#detail-([ABC])$/)||[])[1]||(location.search.match(/[?&]open=([ABC])/)||[])[1];
 if(want){{open_(want);setTimeout(function(){{document.getElementById('detail-'+want).scrollIntoView()}},80)}}
 cards.forEach(function(b){{
  b.addEventListener('click',function(){{
   var id=b.dataset.course,was=b.getAttribute('aria-expanded')==='true';
   cards.forEach(function(o){{if(o.getAttribute('aria-expanded')==='true')close(o.dataset.course,true)}});
   if(was)return;
   open_(id);history.replaceState(null,'','#detail-'+id);
   land(id);
  }});
 }});
 document.querySelectorAll('.dclose').forEach(function(x){{
  x.addEventListener('click',function(){{var d=x.closest('.detail'),id=d.id.replace('detail-','');close(id);
   document.querySelector('.mcard[data-course="'+id+'"]').scrollIntoView({{behavior:'smooth',block:'center'}})}});
 }});
}})();
{HERO_JS}
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
