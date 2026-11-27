/* Libertarian Enough results. Reads the answer code from the address (#a=...) or this browser. Nothing is sent anywhere. */
(function(){
  var D=window.LE, L=window.LEScore, Q=D.questions;
  var out=document.getElementById('result'); if(!out||!L) return;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function verdict(p){for(var i=0;i<D.verdicts.length;i++){if(p>=D.verdicts[i][0]) return D.verdicts[i][1];} return '';}
  function typeById(id){for(var i=0;i<D.types.length;i++) if(D.types[i].id===id) return D.types[i]; return null;}
  function receipts(a){
    var items=[];
    Q.forEach(function(q,i){
      if(!q.trap) return;
      var v=a[i], cls, txt;
      var pure=(q.trap==='agree')?(v>=3):(v<=1);
      var impure=(q.trap==='agree')?(v<=1):(v>=3);
      if(pure){cls='pass';txt=q.pass_;} else if(impure){cls='fail';txt=q.fail;} else {cls='mid';txt=D.hedge.replace('{topic}',q.topic);}
      items.push('<li class="'+cls+'"><span class="sr">'+(cls==='pass'?'Passed: ':cls==='fail'?'Failed: ':'Hedged: ')+'</span><b>'+esc(q.topic.charAt(0).toUpperCase()+q.topic.slice(1))+':</b> '+esc(txt)+'</li>');
    });
    return '<ul class="receipts">'+items.join('')+'</ul>';
  }
  function plot(svg,E,P,label,fill,below){
    var ns='http://www.w3.org/2000/svg', x=L.dx(E,P), y=L.dy(E,P);
    function add(tag,attrs,text){var el=document.createElementNS(ns,tag);for(var k in attrs) el.setAttribute(k,attrs[k]); if(text) el.textContent=text; svg.appendChild(el); return el;}
    add('polygon',{points:L.star(x,y,17,8),fill:fill,stroke:'#1a1a1a','stroke-width':2.5});
    var right=x>L.CX, tx=right?x-22:x+22, ty=below?y+28:y-12, a={x:tx,y:ty,'text-anchor':right?'end':'start','font-size':20,'font-weight':800};
    var h=add('text',a,label); h.setAttribute('fill','#fffdf5'); h.setAttribute('stroke','#fffdf5'); h.setAttribute('stroke-width',6); h.setAttribute('stroke-linejoin','round'); h.setAttribute('aria-hidden','true');
    var t=add('text',a,label); t.setAttribute('fill','#1a1a1a');
  }
  function nearest(me){
    var r=D.refs.map(function(f,i){return {f:f,i:i,d:Math.hypot(f.e-me.E,f.p-me.P)}}).sort(function(a,b){return a.d-b.d});
    return r.slice(0,3).map(function(x){return '<li><b>'+(x.i+1)+'. '+esc(x.f.n)+'</b>: '+esc(x.f.note)+'</li>'}).join('');
  }
  /* A 0-100 bar with its number written beside it, so nothing depends on reading the bar alone. */
  function bar(label,val,note){
    return '<li><span class="bl">'+esc(label)+'</span><span class="bt" aria-hidden="true"><span style="width:'+Math.max(2,val)+'%"></span><i></i></span><span class="bv">'+val+'<span class="sr"> out of 100</span></span>'+(note?'<span class="bn">'+esc(note)+'</span>':'')+'</li>';
  }
  var DIMS=[['R','Wants the state gone','How far toward no government at all'],['L','Left-libertarian','Anti-boss, anti-landlord, pro-co-op'],
    ['T','Traditional','Family, church and local custom first'],['G','Wants to win elections','Suits, potholes, ballots'],
    ['C','Constitutional','The Constitution as written is enough'],['M','Mises Caucus energy','Louder, harder, end the Fed'],
    ['V','Voluntaryist','Build around the state, skip the vote']];
  function statsheet(me){
    var h='<ul class="bars">'+bar('Economic freedom',me.E,'')+bar('Personal freedom',me.P,'')+'</ul><h3>Your flavor stats</h3><p class="src">50 is neutral. Under 50 means you pushed against it, over 50 means you leaned in.</p><ul class="bars">';
    DIMS.forEach(function(d){ h+=bar(d[1],Math.round((me.n[d[0]]+1)*50),d[2]); });
    return h+'</ul>';
  }
  function theory(a,isMine){
    var pr=L.priorities(a), ms=L.methods(a), you=isMine?'you':'they', your=isMine?'your':'their';
    var lead=null; for(var i=0;i<pr.length;i++){ if(Math.abs(pr[i].lean)>=20){lead=pr[i];break;} }
    var h='<p class="lead">'+(isMine?'Your':'This')+' position is a theory. Every answer was a bet about which change would make society better, and so is every vote. Here is '+your+'s, ranked by how hard '+you+' leaned in.</p>';
    if(lead) h+='<div class="note"><p><b>'+(isMine?'Your':'Their')+' theory of change, in one line:</b> '+esc(lead.lean>0?lead.area.free:lead.area.state)+'</p></div>';
    h+='<ol class="prio">';
    pr.forEach(function(p){
      var dir=p.lean>=20?'Less state':p.lean<=-20?'More state':'Split';
      h+='<li><svg class="ico" viewBox="0 0 48 48" width="40" height="40" aria-hidden="true" focusable="false"><use href="assets/icons.svg#'+p.area.icon+'"/></svg><div><p class="ph"><b>'+esc(p.area.name)+'</b> <span class="badge '+(dir==='Less state'?'yes':dir==='More state'?'no':'mid')+'">'+dir+'</span></p>'+
        '<ul class="bars">'+bar('How hard '+you+' leaned in',p.conviction,'')+'</ul><p>'+esc(dir==='More state'?p.area.state:dir==='Less state'?p.area.free:'Pulled both ways here. That usually means this one depends on the details, or on who is asking.')+'</p></div></li>';
    });
    h+='</ol>';
    var top=ms[0];
    h+='<h3>How '+you+' think change happens</h3><ul class="bars">';
    ms.forEach(function(m){ h+=bar(m.m.name,Math.round((m.v+100)/2),m.m.text); });
    h+='</ul>';
    if(top&&top.v>0) h+='<p>Strongest bet: <b>'+esc(top.m.name.toLowerCase())+'</b>. When '+you+' vote, or skip voting, that is the theory '+you+' are acting on.</p>';
    return h;
  }
  var h=location.hash.replace(/^#/,''); var params={};
  h.split('&').forEach(function(kv){var p=kv.split('=');if(p[0])params[p[0]]=decodeURIComponent(p[1]||'');});
  var mineCode=null; try{mineCode=localStorage.getItem('le_mine')}catch(e){}
  var code=params.a||mineCode; var a=L.parse(code);
  if(!a){ out.innerHTML='<p class="lead">No results yet. Take the quiz first. It takes about five minutes and your answers never leave this browser.</p><p><a class="btn gold" href="quiz.html">Take the quiz</a></p>'; return; }
  var isMine=(code===mineCode);
  var me=L.score(a), t=typeById(me.type), ru=me.runner?typeById(me.runner):null;
  var mine=(!isMine&&L.parse(mineCode))?L.score(L.parse(mineCode)):null;
  var shareUrl=location.origin+location.pathname+'#a='+code;
  var html='';
  html+='<div class="result-head"><svg class="typeic" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><use href="assets/icons.svg#'+t.icon+'"/></svg><div>';
  html+='<p class="kicker">'+(isMine?'You are':'This person is')+'</p><h1 id="type-name" tabindex="-1">'+esc(t.name)+'</h1><p class="lead"><b>'+esc(t.tagline)+'</b></p></div></div>';
  html+='<p>'+esc(t.short)+'</p><p class="sass">'+esc(t.roast)+'</p>';
  if(ru) html+='<p>Runner-up: <a href="types/'+ru.id+'.html">'+esc(ru.name)+'</a>. You flirted with it.</p>';
  html+='<p><a href="types/'+t.id+'.html">Read the full '+esc(t.name)+' profile</a></p>';
  html+='<h2>Purity score</h2><p class="purity">'+me.purity+'<span style="font-size:1.4rem">/100</span></p>';
  html+='<div class="meter" role="img" aria-label="Purity '+me.purity+' out of 100"><span style="width:'+me.purity+'%"></span></div>';
  html+='<p><b>'+esc(verdict(me.purity))+'</b></p>';
  if(me.type==='collectivist') html+='<p>We rounded it down to zero. You know why.</p>';
  if(mine){
    var diff=me.purity-mine.purity;
    html+='<div class="note"><p><b>Compared with you:</b> ';
    html+= diff===0?'Dead even. Equally libertarian enough, or equally not.':(diff>0?'This person is '+diff+' points more libertarian enough than you.':'You are '+(-diff)+' points more libertarian enough than this person.');
    html+=' You both show on the chart below.</p></div>';
  }
  var liberty=Math.round((me.E+me.P)/2), lr=me.E-me.P;
  html+='<h2>Where '+(isMine?'you':'they')+' sit</h2><p>Liberty: <b>'+liberty+'</b> of 100. Left to right: <b>'+(Math.abs(lr)<5?'dead center':Math.abs(lr)+' points '+(lr>0?'right':'left')+' of center')+'</b>. That comes from economic freedom <b>'+me.E+'</b> and personal freedom <b>'+me.P+'</b>.</p>';
  out.innerHTML=html;
  var svg=document.querySelector('#chart svg');
  if(svg){
    if(mine) plot(svg,mine.E,mine.P,'You','#ffffff',true);
    plot(svg,me.E,me.P,isMine?'You':'This result','#f5c400',false);
    var desc=svg.querySelector('desc');
    if(desc) desc.textContent+=' Gold star, '+(isMine?'you':'this result')+': economic freedom '+me.E+', personal freedom '+me.P+'.'+(mine?' White star, you: economic freedom '+mine.E+', personal freedom '+mine.P+'.':'');
  }
  var ss=document.getElementById('statsheet'); if(ss) ss.innerHTML=statsheet(me);
  var th=document.getElementById('theory'); if(th) th.innerHTML=theory(a,isMine);
  var rc=document.getElementById('receipts'); if(rc) rc.innerHTML=receipts(a);
  var nb=document.getElementById('neighbors'); if(nb) nb.innerHTML='<ul>'+nearest(me)+'</ul>';
  var sh=document.getElementById('share-url'); if(sh) sh.value=shareUrl;
  var after=document.getElementById('after'); if(after) after.hidden=false;
  var tbody=document.getElementById('you-row');
  if(tbody){ tbody.innerHTML='<tr><th scope="row">'+(isMine?'You':'This result')+'</th><td>'+me.E+'</td><td>'+me.P+'</td><td>Gold star</td></tr>'+(mine?'<tr><th scope="row">You</th><td>'+mine.E+'</td><td>'+mine.P+'</td><td>White star</td></tr>':''); }
  try{ if(isMine) localStorage.setItem('le_mine_ep',JSON.stringify({E:me.E,P:me.P,type:t.name})); }catch(e){}
  var copy=document.getElementById('copy-btn');
  if(copy) copy.addEventListener('click',function(){
    var msg=document.getElementById('copy-msg');
    function ok(){msg.textContent='Link copied. Send it to a friend and see who is more libertarian enough.';}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(shareUrl).then(ok,function(){sh.select();document.execCommand('copy');ok();});}
    else{sh.select();document.execCommand('copy');ok();}
  });
  var nat=document.getElementById('share-native');
  if(nat&&navigator.share){nat.hidden=false; nat.addEventListener('click',function(){navigator.share({title:'Am I libertarian enough?',text:'I got '+t.name+' ('+me.purity+'/100). Are you libertarian enough?',url:shareUrl}).catch(function(){});});}
  var hd=document.getElementById('type-name'); if(hd) hd.focus();
  document.title=t.name+' | Libertarian Enough';
  window.addEventListener('hashchange',function(){location.reload();});
})();
