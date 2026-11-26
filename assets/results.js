/* Libertarian Enough results. Reads the answer code from the address (#a=...) or this browser. Nothing is sent anywhere. */
(function(){
  var D=window.LE, Q=D.questions, N=Q.length;
  var out=document.getElementById('result'); if(!out) return;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function parse(code){
    if(!code) return null; var m=/^(v\d+)\.([0-4]+)$/.exec(code);
    if(!m||m[1]!==D.version||m[2].length!==N) return null;
    return m[2].split('').map(Number);
  }
  function score(a){
    var dims={E:0,P:0,R:0,L:0,T:0,G:0,C:0,M:0,V:0,X:0}, tot={};
    for(var k in dims) tot[k]=0;
    Q.forEach(function(q,i){var v=a[i]-2; for(var d in q.w){dims[d]+=q.w[d]*v; tot[d]+=Math.abs(q.w[d])*2;}});
    var n={}; for(var d in dims) n[d]=tot[d]?dims[d]/tot[d]:0;
    var E=Math.round((n.E+1)*50), P=Math.round((n.P+1)*50), Rs=(n.R+1)*50;
    var purity=Math.round(.4*E+.4*P+.2*Rs);
    var hi=Q.map(function(q){return q.id}).indexOf('heritage');
    var collectivist=hi>=0&&a[hi]>=3;
    if(collectivist) purity=0;
    var type, runner=null;
    if(collectivist) type='collectivist';
    else if(Math.abs(E-50)<10&&Math.abs(P-50)<10) type='centrist';
    else if(E>=50&&P>=50){
      if(E>=60&&P>=60){
        var c={
          minarchist:.3+.6*Math.max(0,-n.R),
          ancap:n.R-.4*Math.max(0,n.V),
          agorist:n.V>0?.6*n.V+.5*n.R:-1,
          leftlib:n.L-Math.max(0,n.T),
          paleo:1.6*n.T-Math.max(0,n.L),
          mises:n.M,
          classical:n.C-.5*Math.max(0,n.R),
          pragmatist:n.G+.1,
          purist:purity>=90?(purity-80)/10-Math.max(0,n.G):-1
        };
        var ks=Object.keys(c).sort(function(x,y){return c[y]-c[x]});
        if(c[ks[0]]<.45){type='smalll'; runner=ks[0];} else {type=ks[0]; runner=ks[1];}
      } else type='smalll';
    }
    else if(E<50&&P>=50) type='progressive';
    else if(E>=50&&P<50) type='conservative';
    else type='statist';
    return {E:E,P:P,purity:purity,type:type,runner:runner,n:n};
  }
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
  function px(e){return 60+e*5} function py(p){return 520-p*5}
  function star(x,y){var s='',r1=13,r2=6;for(var k=0;k<10;k++){var r=k%2?r2:r1,ang=-Math.PI/2+k*Math.PI/5;s+=(x+r*Math.cos(ang)).toFixed(1)+','+(y+r*Math.sin(ang)).toFixed(1)+' ';}return s.trim();}
  function plot(me,them,label){
    var svg=document.querySelector('#chart svg'); if(!svg) return;
    var ns='http://www.w3.org/2000/svg';
    function add(tag,attrs,text){var el=document.createElementNS(ns,tag);for(var k in attrs) el.setAttribute(k,attrs[k]); if(text) el.textContent=text; svg.appendChild(el); return el;}
    function lab(x,y,dy,txt,size,weight){var right=x>430,top=y+dy<24;add('text',{x:right?x-16:x+16,y:top?y+26:y+dy,'text-anchor':right?'end':'start','font-size':size,'font-weight':weight,fill:'#1a1a1a',stroke:'#fffdf5','stroke-width':5,'stroke-linejoin':'round','paint-order':'stroke'},txt);}
    if(them){var x=px(them.E),y=py(them.P); add('polygon',{points:x+','+(y-12)+' '+(x+12)+','+y+' '+x+','+(y+12)+' '+(x-12)+','+y,fill:'#ffffff',stroke:'#1a1a1a','stroke-width':3}); lab(x,y,5,'Them',16,700);}
    var x2=px(me.E),y2=py(me.P);
    add('polygon',{points:star(x2,y2),fill:'#f5c400',stroke:'#1a1a1a','stroke-width':2.5});
    lab(x2,y2,-8,label,17,800);
    var desc=svg.querySelector('desc');
    if(desc) desc.textContent+=' '+label+': economic freedom '+me.E+', personal freedom '+me.P+'.';
  }
  function nearest(me){
    var r=D.refs.map(function(f,i){return {f:f,i:i,d:Math.hypot(f.e-me.E,f.p-me.P)}}).sort(function(a,b){return a.d-b.d});
    return r.slice(0,3).map(function(x){return '<li><b>'+(x.i+1)+'. '+esc(x.f.n)+'</b>: '+esc(x.f.note)+'</li>'}).join('');
  }
  var h=location.hash.replace(/^#/,''); var params={};
  h.split('&').forEach(function(kv){var p=kv.split('=');if(p[0])params[p[0]]=decodeURIComponent(p[1]||'');});
  var mineCode=null; try{mineCode=localStorage.getItem('le_mine')}catch(e){}
  var code=params.a||mineCode; var a=parse(code);
  if(!a){ out.innerHTML='<p class="lead">No results yet. Take the quiz first. It takes about five minutes and your answers never leave this browser.</p><p><a class="btn gold" href="quiz.html">Take the quiz</a></p>'; return; }
  var isMine=(code===mineCode);
  var me=score(a), t=typeById(me.type), ru=me.runner?typeById(me.runner):null;
  var mine=(!isMine&&parse(mineCode))?score(parse(mineCode)):null;
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
  html+='<h2>Where you sit</h2><p>Economic freedom: <b>'+me.E+'</b> of 100. Personal freedom: <b>'+me.P+'</b> of 100.</p>';
  out.innerHTML=html;
  var rc=document.getElementById('receipts'); if(rc) rc.innerHTML=receipts(a);
  var nb=document.getElementById('neighbors'); if(nb) nb.innerHTML='<ul>'+nearest(me)+'</ul>';
  var sh=document.getElementById('share-url'); if(sh) sh.value=shareUrl;
  var after=document.getElementById('after'); if(after) after.hidden=false;
  plot(me, null, isMine?'You':'This result');
  if(mine){ var x=px(mine.E),y=py(mine.P); var svg=document.querySelector('#chart svg'); var ns='http://www.w3.org/2000/svg';
    var p=document.createElementNS(ns,'polygon'); p.setAttribute('points',star(x,y)); p.setAttribute('fill','#ffffff'); p.setAttribute('stroke','#1a1a1a'); p.setAttribute('stroke-width','2.5'); svg.appendChild(p);
    var tx=document.createElementNS(ns,'text'); tx.setAttribute('x',x+16); tx.setAttribute('y',y+20); tx.setAttribute('font-size','17'); tx.setAttribute('font-weight','800'); tx.textContent='You'; svg.appendChild(tx);
    var desc=svg.querySelector('desc'); if(desc) desc.textContent+=' You: economic freedom '+mine.E+', personal freedom '+mine.P+'.';
  }
  var tbody=document.getElementById('you-row');
  if(tbody){ tbody.innerHTML='<tr><th scope="row">'+(isMine?'You':'This result')+'</th><td>'+me.E+'</td><td>'+me.P+'</td><td>Gold star</td></tr>'+(mine?'<tr><th scope="row">You</th><td>'+mine.E+'</td><td>'+mine.P+'</td><td>White star</td></tr>':''); }
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
