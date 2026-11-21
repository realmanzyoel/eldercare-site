/* Evenhome components. Everything works with motion off; reduced-motion users get the end state. */
(function(){
var d=document,rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
function $(s,r){return (r||d).querySelector(s)}function $$(s,r){return [].slice.call((r||d).querySelectorAll(s))}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function fmt(sym,n){return sym+Math.round(n).toLocaleString('en-US')}
function tween(el,to,sym,suffix){var from=+(el.dataset.v||0);el.dataset.v=to;if(rm){el.textContent=fmt(sym,to)+(suffix||'');return}
 var t0=performance.now(),D=500;(function f(t){var p=Math.min(1,(t-t0)/D),e=1-Math.pow(1-p,3);el.textContent=fmt(sym,from+(to-from)*e)+(suffix||'');if(p<1)requestAnimationFrame(f)})(t0)}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.2});
$$('.tick-in,.arc,.pins,.dial').forEach(function(el){io.observe(el)});

/* mobile menu */
var bg=$('.burger'),mn=$('#mnav');if(bg&&mn)bg.addEventListener('click',function(){var o=bg.getAttribute('aria-expanded')==='true';bg.setAttribute('aria-expanded',!o);mn.hidden=o});

/* hero slideshow pause */
var hp=$('.hpause');if(hp){var h2=$('.hero2');if(rm)h2.classList.add('paused'),hp.textContent='Play';hp.addEventListener('click',function(){var p=h2.classList.toggle('paused');hp.textContent=p?'Play':'Pause';hp.setAttribute('aria-pressed',p)})}

/* live care card loop: one event every 2s */
$$('.ccard').forEach(function(c){var li=$$('.cc-l li',c),n=li.length,k=0,vis=4;
 function show(){li.forEach(function(x){x.classList.remove('sh')});for(var j=0;j<vis;j++)li[(k+j)%n].classList.add('sh');k=(k+1)%n}
 show();if(!rm)setInterval(function(){if(!d.hidden)show()},2000)});

/* situation picker: filters content below and remembers the choice */
var notes={dementia:'Showing dementia care first. Everything below is tuned to dementia.',afar:'Showing care from afar first: the app, the Care Director and weekly updates.',hospital:'Showing care after hospital first: a 72-hour start and a first-week plan.'};
function setSit(s){if(!s)return;d.body.dataset.sit=s;store('ev-sit',s);$$('.sit').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.sit===s)});var w=$('.sits');if(w)w.classList.add('chosen');
 $$('.for').forEach(function(f){f.classList.toggle('on',f.dataset.for===s)});$$('.svc').forEach(function(v){v.classList.toggle('match',(v.dataset.tags||'')===s)});var nt=$('.sit-note');if(nt)nt.textContent=notes[s]||''}
$$('.sit').forEach(function(b){b.addEventListener('click',function(){setSit(b.dataset.sit)})});
if($('.sits'))setSit(store('ev-sit'));else{var ss=store('ev-sit');if(ss)$$('.svc').forEach(function(v){v.classList.toggle('match',(v.dataset.tags||'')===ss)})}

/* path draw + step light-up */
$$('.path').forEach(function(p){var st=$$('.ps',p);function up(){var r=p.getBoundingClientRect(),v=(innerHeight*.6-r.top)/r.height;v=Math.max(0,Math.min(1,v));p.style.setProperty('--p',rm?1:v);
 st.forEach(function(s){var q=s.getBoundingClientRect();s.classList.toggle('lit',rm||q.top<innerHeight*.65)})}addEventListener('scroll',up,{passive:true});up()});

/* pinned phone */
$$('.pin').forEach(function(pn){var sc=$$('.scr',pn),st=$$('.pst',pn);var o=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var i=+e.target.dataset.i;
 sc.forEach(function(s,k){s.classList.toggle('on',k===i)});st.forEach(function(s,k){s.classList.toggle('on',k===i)})})},{rootMargin:'-45% 0px -45% 0px'});st.forEach(function(s){o.observe(s)});if(st[0])st[0].classList.add('on')});

/* accordion search */
$$('[data-filter]').forEach(function(inp){var box=d.getElementById(inp.dataset.filter);inp.addEventListener('input',function(){var q=inp.value.toLowerCase().trim(),n=0;
 $$('.acc',box).forEach(function(a){var m=!q||a.textContent.toLowerCase().indexOf(q)>-1;a.hidden=!m;if(m)n++;if(q&&m)a.open=true});$('.nores',box).hidden=n>0})});

/* estimator */
$$('.est').forEach(function(e){var sym=e.dataset.sym,night=+e.dataset.night;function g(k){return $('[data-est='+k+']',e)}
 function calc(){var h=+g('hours').value,r=+g('rate').value*+g('city').value,w=g('wknd'),nt=g('night'),ns=g('nights');
  var wk=h*r;if(w&&w.checked)wk+=h*r*.15*(2/7);var sh=$('[data-show=night]',e);if(sh)sh.classList.toggle('on',!!(nt&&nt.checked));if(nt&&nt.checked)wk+=night*+ns.value;
  var mo=wk*52/12,lo=mo*.92,hi=mo*1.08;$('[data-o=hours]',e).textContent=h;if(ns)$('[data-o=nights]',e).textContent=ns.value;
  tween($('.est-v',e),mo,sym);$('.est-r',e).textContent='Likely range '+fmt(sym,lo)+' to '+fmt(sym,hi)+' a month, about '+fmt(sym,wk)+' a week';
  $('.est-bar i',e).style.setProperty('--w',Math.min(100,mo/((84*48*52/12)/100))+'%')}
 $$('input,select',e).forEach(function(x){x.addEventListener('input',calc)});calc()});

/* Support at Home explainer */
$$('.sah').forEach(function(e){var R={full:[.05,.175],part:[.25,.45],self:[.5,.8]};function g(k){return $('[data-sah='+k+']',e)}
 function calc(){var b=+g('bud').value,p=g('pen').value,ind=+g('ind').value/100,r=R[p];var c=b*ind*r[0]+b*(1-ind)*r[1];
  $('[data-o=bud]',e).textContent=fmt('$',b);$('[data-o=ind]',e).textContent=Math.round(ind*100)+'%';tween($('.sah-v',e),c,'$');
  $('.sah-r',e).textContent='About '+fmt('$',c/52)+' a week. Government pays about '+fmt('$',b-c)+' of a '+fmt('$',b)+' budget.'+(p==='part'?' Part-pensioner rates are a mid-point example.':'');
  $('.est-bar i',e).style.setProperty('--w',Math.min(100,c/b*100)+'%')}$$('input,select',e).forEach(function(x){x.addEventListener('input',calc)});calc()});

/* flip cards on tap */
$$('.flip').forEach(function(f){f.addEventListener('click',function(){f.setAttribute('aria-pressed',f.getAttribute('aria-pressed')!=='true')})});

/* sticky call bar after first scroll */
var sb=$('.sbar');if(sb)addEventListener('scroll',function(){sb.classList.toggle('on',scrollY>300)},{passive:true});

/* chat */
$$('.chat').forEach(function(c){var b=$('.chat-b',c),p=$('.chat-p',c),l=$('.chat-l',c);function tog(o){p.hidden=!o;b.setAttribute('aria-expanded',o)}
 b.addEventListener('click',function(){tog(p.hidden)});$('.chat-x',c).addEventListener('click',function(){tog(false);b.focus()});
 d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!p.hidden){tog(false);b.focus()}});
 $$('.cq',c).forEach(function(q){q.addEventListener('click',function(){var m=d.createElement('p');m.className='cm me';m.textContent=q.textContent;l.appendChild(m);
  setTimeout(function(){var a=d.createElement('p');a.className='cm bot';a.innerHTML=q.dataset.a+' <br><small>Want a person? Use the buttons below.</small>';l.appendChild(a);l.scrollTop=l.scrollHeight},rm?0:450)})})});

/* stage slider */
$$('.stages').forEach(function(s){var r=$('[data-stage]',s),p=$$('.stg',s),n=['Early stage','Middle stage','Late stage'];function up(){var i=+r.value;p.forEach(function(x,k){x.classList.toggle('on',k===i)});
 $('.stg-tl',s).style.setProperty('--s',i);r.setAttribute('aria-valuetext',n[i])}r.addEventListener('input',up);up()});

/* day arc sun */
$$('.arc').forEach(function(a){var c=$('.sun',a);if(!c)return;function up(){var r=a.getBoundingClientRect(),t=Math.max(0,Math.min(1,(innerHeight-r.top)/(innerHeight+r.height)));if(rm)t=.5;
 var x=t*1000,y=200-(1-Math.pow(2*t-1,2))*130*2/2*1.0;c.setAttribute('cx',x);c.setAttribute('cy',Math.max(14,y-0))}addEventListener('scroll',up,{passive:true});up()});

/* respite planner + calendar */
$$('.resp').forEach(function(w){var cal=$('.cal',w),rate=+cal.dataset.rate,sym=cal.dataset.sym,blk=8,t=$('[data-resp=tired]',w);
 function sug(){var v=+t.value;$('[data-o=tired]',w).textContent=v;$('.resp-s',w).textContent=v<=3?'You are coping. One 4-hour break a week keeps it that way.':v<=6?'You need regular time back. We suggest one full day a week, plus a 4-hour break.':v<=8?'You are running on empty. Two full days a week and an overnight once a fortnight.':'Please do not wait. Call us today: we can arrange an overnight break this week and talk about longer support.'}
 function sum(){var n=$$('.cd[aria-pressed=true]',cal).length;$('.resp-sum',w).textContent=n+' break'+(n===1?'':'s')+', '+n*blk+' hours';tween($('.resp-cost',w),n*blk*rate,sym)}
 t.addEventListener('input',sug);sug();$$('[data-blk]',w).forEach(function(b){b.addEventListener('click',function(){blk=+b.dataset.blk;$$('[data-blk]',w).forEach(function(x){x.setAttribute('aria-pressed',x===b)});sum()})});
 $$('.cd',cal).forEach(function(c){c.addEventListener('click',function(){c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')!=='true');sum()})});sum()});

/* 72-hour countdown */
$$('.c72').forEach(function(c){var bx=$$('[data-c72]',c),hrs=[0,2,12,24,48,72];function up(){var n=bx.filter(function(b){return b.checked}).length;c.style.setProperty('--p',n/bx.length*100);
 $('.c72-f',c).style.strokeDasharray=(n/bx.length*100)+' 100';$('.c72-h',c).textContent=String(72-(n?hrs[n-1]:0))}bx.forEach(function(b){b.addEventListener('change',up)});up()});

/* day / night sweep */
$$('.dn24').forEach(function(s){function up(){var r=s.getBoundingClientRect(),t=Math.max(0,Math.min(1,(innerHeight*.8-r.top)/(r.height+innerHeight*.3)));s.style.setProperty('--t',rm?.5:t.toFixed(3))}addEventListener('scroll',up,{passive:true});up()});

/* world to front door zoom */
$$('.zoom').forEach(function(z){if(rm)return;var L=$$('.zl',z),card=$('.zoom-card',z);function up(){var r=z.getBoundingClientRect(),t=Math.max(0,Math.min(.999,-r.top/(r.height-innerHeight)));
 var seg=t*L.length,i=Math.floor(seg),f=seg-i;L.forEach(function(l,k){l.style.setProperty('--o',k<i?0:k===i?1:k===i+1?f:0);l.style.setProperty('--s',k===i?(1+f*.6):k===i+1?(1.6-f*.6):1);if(k===L.length-1&&i===k)l.style.setProperty('--s',1+f*.15)});
 card.style.setProperty('--co',Math.max(0,(t-.72)/.2).toFixed(2))}addEventListener('scroll',up,{passive:true});up()});

/* care quiz */
$$('.quiz').forEach(function(q){var qs=$$('.qq',q),ans=[],i=0,back=$('.qz-back',q),p=q.dataset.p,cg=q.dataset.cg,live=q.dataset.live==='1';
 function go(k){i=k;qs.forEach(function(x,j){x.classList.toggle('on',j===i)});$('.qz-c',q).textContent='Question '+(i+1)+' of '+qs.length;back.hidden=i===0;$('.qz-f',q).style.strokeDasharray=(i/qs.length*100)+' 100';var f=$('.qa',qs[i]);if(f&&k)f.focus({preventScroll:true})}
 function result(){qs.forEach(function(x){x.classList.remove('on')});$('.qz-f',q).style.strokeDasharray='100 100';$('.qz-c',q).textContent='Your suggested plan';back.hidden=false;
  var s=ans[1]+ans[2]+ans[3]+ans[4]+(ans[5]>=2?1:0),dem=ans[1]>=2,far=ans[6]>=2,hosp=ans[7]===2,crisis=ans[7]===3;
  var plan=s<=2?['Companion care','6 to 10 hours a week','Two or three visits for company, meals and outings.']:s<=5?[dem?'Dementia care':'Personal care','15 to 25 hours a week','Daily visits from the same small team, with a routine built around them.']:s<=8?[dem?'Dementia care':'Personal care','30 to 50 hours a week','Long daily shifts, a safety plan and family coaching.']:['24/7 care','Around the clock, by a team','Awake day and evening shifts with a waking or sleep-over night shift.'];
  var extra=[];if(hosp)extra.push('Start with our <a href="/'+p+'/services/after-hospital.html">care after hospital</a> plan: a first-week plan and a 72-hour start.');if(far)extra.push('Add a named Care Director and the family app, see <a href="/'+p+'/services/care-from-afar.html">care from afar</a>.');
  if(ans[5]>=2)extra.push('You need breaks too. <a href="/'+p+'/services/respite-care.html">Respite care</a> can start with one day a week.');if(crisis)extra.push('<b>This sounds urgent. Please call us now rather than waiting.</b>');
  var r=$('.qz-res',q);r.innerHTML='<p class="ey">Suggested starting plan</p><h3>'+plan[0]+'</h3><p class="hrs"><span>Starting hours</span><b>'+plan[1]+'</b></p><p>'+plan[2]+'</p>'+(extra.length?'<ul class="ticks">'+extra.map(function(x){return'<li>'+x+'</li>'}).join('')+'</ul>':'')+
   '<p class="cn">A suggestion, not a medical or care assessment. A care manager will adjust it after meeting them and you.</p><p><a class="btn" href="/'+p+'/book.html">'+(live?'Book a free assessment':'Join the waitlist')+'</a> <a class="btn o" href="/'+p+'/pricing.html">See what it would cost</a></p>'+
   '<p class="cn">Want this plan by email? We only ask after showing it: use the booking form and mention the quiz.</p>';
  fixLinks(r);r.hidden=false;r.focus&&r.setAttribute('tabindex','-1');r.focus()}
 $$('.qa',q).forEach(function(b){b.addEventListener('click',function(){var f=b.closest('.qq'),k=+f.dataset.q;$$('.qa',f).forEach(function(x){x.classList.toggle('sel',x===b)});ans[k]=+b.dataset.v;setTimeout(function(){k+1<qs.length?go(k+1):result()},rm?0:280)})});
 back.addEventListener('click',function(){$('.qz-res',q).hidden=true;go(Math.max(0,Math.min(i,qs.length)-(qs.some(function(x){return x.classList.contains('on')})?1:0)))});go(0)});
function fixLinks(root){var base=d.querySelector('link[rel=stylesheet][href*="assets/site.css"]');var pre=base?base.getAttribute('href').split('assets/')[0]:'';
 $$('a[href^="/"]',root).forEach(function(a){a.setAttribute('href',pre+a.getAttribute('href').slice(1))})}

/* booking: next-24h slots, progress bar, mailto send, calm confirmation */
$$('.book').forEach(function(f){var sl=$('[data-slots]',f),pick='';
 if(sl){var now=new Date(),t=new Date(now);t.setMinutes(0,0,0);t.setHours(t.getHours()+2);var n=0;while(n<8){var h=t.getHours();if(h>=8&&h<=19){var b=d.createElement('button');b.type='button';b.setAttribute('aria-pressed','false');
  var day=t.toDateString()===now.toDateString()?'Today':'Tomorrow';b.innerHTML=t.toLocaleTimeString([], {hour:'numeric',minute:'2-digit'})+'<small>'+day+'</small>';b.dataset.v=day+' '+t.toLocaleTimeString([], {hour:'numeric',minute:'2-digit'});
  b.addEventListener('click',function(){pick=this.dataset.v;$$('button',sl).forEach(function(x){x.setAttribute('aria-pressed','false')});this.setAttribute('aria-pressed','true');prog()});sl.appendChild(b);n++}t.setHours(t.getHours()+(h<8||h>19?1:2))}}
 var req=$$('[required]',f);function prog(){var k=req.filter(function(x){return x.type==='checkbox'?x.checked:x.value.trim()}).length+(pick?1:0);$('.bk-bar i',f).style.setProperty('--w',(k/(req.length+(sl?1:0))*100)+'%')}
 req.forEach(function(x){x.addEventListener('input',prog);x.addEventListener('change',prog)});
 f.addEventListener('submit',function(e){e.preventDefault();var bad=req.filter(function(x){return x.type==='checkbox'?!x.checked:!x.value.trim()});var er=$('.bk-err',f);
  if(bad.length){er.textContent='Please fill in: '+bad.map(function(x){return x.closest('label').textContent.split('.')[0].replace('I agree','consent to contact').trim()}).join(', ');bad[0].focus();return}er.textContent='';
  var fd=new FormData(f),lines=[];fd.forEach(function(v,k){lines.push(k+': '+v)});if(pick)lines.push('requested time: '+pick);lines.push('page: '+location.pathname);
  location.href='mailto:'+f.dataset.mail+'?subject='+encodeURIComponent((f.dataset.kind||'assessment')+' request ('+f.dataset.market+')')+'&body='+encodeURIComponent(lines.join('\n'));
  f.classList.add('sent');var ok=$('.bk-ok',f);ok.hidden=false;ok.focus()})});

/* carousel with pause */
$$('.car').forEach(function(c){var s=$$('.cs',c),dt=$$('.car-d button',c),p=$('.car-p',c),i=0,paused=rm;if(rm){p.textContent='Play';p.setAttribute('aria-pressed','true')}
 function go(k){i=(k+s.length)%s.length;s.forEach(function(x,j){x.classList.toggle('on',j===i)});dt.forEach(function(x,j){x.setAttribute('aria-current',j===i)})}
 dt.forEach(function(b,j){b.addEventListener('click',function(){go(j)})});p.addEventListener('click',function(){paused=!paused;p.textContent=paused?'Play':'Pause';p.setAttribute('aria-pressed',paused)});
 c.addEventListener('mouseenter',function(){c.dataset.h=1});c.addEventListener('mouseleave',function(){c.dataset.h=''});setInterval(function(){if(!paused&&!c.dataset.h&&!d.hidden)go(i+1)},6000)});

/* market selector: suggest from time zone, remember choice */
var mc=$$('.mcard');if(mc.length){var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}var sug=/^Australia\//.test(tz)?'au':'us',saved=store('ev-mkt');
 mc.forEach(function(a){if(a.dataset.m===(saved||sug))a.classList.add('sug');a.addEventListener('click',function(){store('ev-mkt',a.dataset.m)})});var sn=$('.sugnote');if(sn)sn.textContent=saved?'Last time you chose '+(saved==='au'?'Australia':'the United States')+'.':'Your time zone suggests '+(sug==='au'?'Australia':'the United States')+'.'}
})();
