/* The real-life quiz. Your choices stay in this browser unless you send your link. Nothing is sent anywhere. */
(function(){
  var D=window.LIFE; if(!D) return;
  var SC={}; D.scenes.forEach(function(s){SC[s.id]=s;});
  var CH={}; D.chapters.forEach(function(c){CH[c[0]]=c[1];});
  var HW={}; D.hows.forEach(function(h){HW[h[0]]={label:h[1],line:h[2]};});
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function put(k,v){try{if(v===null) localStorage.removeItem(k); else localStorage.setItem(k,v);}catch(e){}}
  function icon(name,cls,size){return '<svg class="'+(cls||'ico')+'" viewBox="0 0 48 48" width="'+(size||40)+'" height="'+(size||40)+'" aria-hidden="true" focusable="false"><use href="../assets/icons.svg#'+name+'"/></svg>';}

  /* Walk the story. Follow-up scenes come right after the choice that leads to them.
     seq lists every scene reached; when the story isn't done, its last entry is the scene being played. */
  function walk(picks){
    var seq=[], oi=0, pending=null, k=0;
    while(true){
      var id;
      if(pending){id=pending; pending=null;}
      else { if(oi>=D.order.length) return {seq:seq,done:true,ok:k===picks.length,main:oi}; id=D.order[oi++]; }
      seq.push(id);
      if(k>=picks.length) return {seq:seq,done:false,ok:true,main:oi};
      var c=SC[id].c[picks[k]]; if(!c) return {seq:seq,done:false,ok:false,main:oi};
      pending=c.then||null; k++;
    }
  }
  function parse(code){
    var m=/^(l\d+)\.([0-9]+)$/.exec(code||''); if(!m||m[1]!==D.version) return null;
    var p=m[2].split('').map(Number), w=walk(p); return (w.done&&w.ok)?p:null;
  }
  function norm(v,lo,hi){return hi>lo?Math.round(100*(v-lo)/(hi-lo)):50}
  function lib(c){return (c.w.E||0)+(c.w.P||0)}
  /* Each score runs 0-100 against the choices you actually faced: 100 means the freest (or kindest) option every time. */
  function score(picks){
    var seq=walk(picks).seq, s={E:0,P:0,H:0}, lo={E:0,P:0,H:0}, hi={E:0,P:0,H:0}, cops=0, chances=0, how={}, area={};
    seq.forEach(function(id,k){
      var sc=SC[id], c=sc.c[picks[k]];
      ['E','P','H'].forEach(function(d){var v=sc.c.map(function(x){return x.w[d]||0}); lo[d]+=Math.min.apply(null,v); hi[d]+=Math.max.apply(null,v); s[d]+=c.w[d]||0;});
      if(sc.c.some(function(x){return x.cop})){chances++; if(c.cop) cops++;}
      how[c.how]=(how[c.how]||0)+1;
      var a=area[sc.area]||(area[sc.area]={s:0,lo:0,hi:0,cops:0}), lv=sc.c.map(lib);
      a.lo+=Math.min.apply(null,lv); a.hi+=Math.max.apply(null,lv); a.s+=lib(c); if(c.cop) a.cops++;
    });
    var E=norm(s.E,lo.E,hi.E), P=norm(s.P,lo.P,hi.P), H=norm(s.H,lo.H,hi.H), L=Math.round((E+P)/2);
    var areas=D.areas.map(function(ar){var a=area[ar.id]; return {area:ar,lean:a?norm(a.s,a.lo,a.hi):50,cops:a?a.cops:0};})
      .sort(function(x,y){return Math.abs(y.lean-50)-Math.abs(x.lean-50)});
    var hows=D.hows.map(function(h){return {id:h[0],n:how[h[0]]||0}}).filter(function(h){return h.n>0}).sort(function(x,y){return y.n-x.n});
    return {seq:seq,E:E,P:P,H:H,L:L,cops:cops,chances:chances,hows:hows,total:seq.length,areas:areas,cls:classFor(L,H)};
  }
  /* Must match the class map in _build/sec_life.py. */
  function classFor(L,H){
    var id=L>=55&&H>=55?'neighbor':L>=55&&H<45?'wolf':L<45&&H>=55?'caretaker':L<45&&H<45?'monitor':'fixer';
    for(var i=0;i<D.classes.length;i++) if(D.classes[i].id===id) return D.classes[i];
  }
  function region(E,P){
    if(Math.abs(E-50)<10&&Math.abs(P-50)<10) return 'centrist';
    return E>=50&&P>=50?'libertarian':E<50&&P>=50?'progressive':E>=50?'conservative':'statist';
  }

  /* ---------- Playing ---------- */
  function play(){
    var picks=[];
    try{var sv=JSON.parse(get('le_life_progress')||'null'); if(sv&&sv.v===D.version&&walk(sv.p).ok&&!walk(sv.p).done) picks=sv.p;}catch(e){}
    var intro=document.getElementById('life-intro'), prog=document.getElementById('life-prog'), stage=document.getElementById('life-stage');
    var bar=document.getElementById('life-bar'), status=document.getElementById('life-status');
    var start=document.getElementById('life-start'), restart=document.getElementById('life-restart');
    if(picks.length){start.textContent='Pick up where you left off'; restart.hidden=false;}
    function save(){put('le_life_progress',JSON.stringify({v:D.version,p:picks}));}
    function go(){intro.hidden=true; prog.hidden=false; stage.hidden=false; render();}
    start.addEventListener('click',go);
    restart.addEventListener('click',function(){picks=[]; save(); go();});
    function focusHead(){var h=document.getElementById('lh'); if(h) h.focus();}
    function render(){
      var w=walk(picks); if(w.done){finish(); return;}
      var id=w.seq[w.seq.length-1], sc=SC[id], n=w.seq.length, follow=D.order.indexOf(id)<0;
      bar.style.width=Math.round(100*(w.main-1)/D.order.length)+'%';
      var where=follow?'What happens next':CH[sc.ch]+' · situation '+w.main+' of '+D.order.length;
      var h='<p class="qnum">'+esc(where)+'</p><h2 class="scene" id="lh" tabindex="-1">'+esc(sc.t)+'</h2><p class="situ">'+esc(sc.s)+'</p>'+
        '<form id="lform" novalidate><fieldset class="q"><legend>What do you do?</legend><div class="opts">';
      sc.c.forEach(function(c,j){var cid='l'+n+'c'+j; h+='<label class="opt" for="'+cid+'"><input type="radio" name="c" id="'+cid+'" value="'+j+'"> '+esc(c.a)+'</label>';});
      h+='</div><p class="qerr" id="lerr" aria-live="polite"></p></fieldset><div class="row">'+(picks.length?'<button type="button" class="btn ghost" id="lback">Back</button>':'')+
        '<button type="submit" class="btn gold">Do it</button></div></form>';
      stage.innerHTML=h;
      status.textContent=where+'. '+sc.t+'.';
      focusHead();
      var form=document.getElementById('lform');
      form.addEventListener('submit',function(ev){
        ev.preventDefault();
        var sel=form.querySelector('input[name=c]:checked');
        if(!sel){document.getElementById('lerr').textContent='Pick what you\'d do first. Doing nothing is one of the choices when it\'s on the list.'; form.querySelector('input').focus(); return;}
        if(walk(picks).done) return;
        var v=parseInt(sel.value,10), c=sc.c[v]; picks.push(v); save();
        if(c.after) after(c); else render();
      });
      var back=document.getElementById('lback');
      if(back) back.addEventListener('click',function(){picks.pop(); save(); render();});
    }
    function after(c){
      var last=walk(picks).done;
      stage.innerHTML='<div class="after"><p class="qnum">What happens</p><h2 class="scene" id="lh" tabindex="-1">'+esc(c.after)+'</h2>'+
        '<div class="row"><button type="button" class="btn gold" id="lcont">'+(last?'See what it says about you':'Keep going')+'</button></div></div>';
      status.textContent='What happens: '+c.after;
      focusHead();
      document.getElementById('lcont').addEventListener('click',render);
    }
    function finish(){
      var code=D.version+'.'+picks.join('');
      put('le_life',code); put('le_life_progress',null);
      bar.style.width='100%';
      stage.innerHTML='<p class="lead" id="lh" tabindex="-1">Adding up your year...</p>'; focusHead();
      location.href='result.html#r='+code;
    }
  }

  /* ---------- The result ---------- */
  function bar(label,val,note,unit){
    return '<li><span class="bl">'+esc(label)+'</span><span class="bt" aria-hidden="true"><span style="width:'+Math.max(2,val)+'%"></span><i></i></span><span class="bv">'+val+(unit?'%':'<span class="sr"> out of 100</span>')+'</span>'+(note?'<span class="bn">'+esc(note)+'</span>':'')+'</li>';
  }
  var ns='http://www.w3.org/2000/svg';
  function starPts(x,y,r1,r2){var s='';for(var k=0;k<10;k++){var r=k%2?r2:r1,a=-Math.PI/2+k*Math.PI/5;s+=(x+r*Math.cos(a)).toFixed(1)+','+(y+r*Math.sin(a)).toFixed(1)+' ';}return s.trim();}
  function plot(svg,x,y,label,fill,below,mid,side){
    function add(tag,attrs,text){var el=document.createElementNS(ns,tag);for(var k in attrs) el.setAttribute(k,attrs[k]); if(text) el.textContent=text; svg.appendChild(el); return el;}
    add('polygon',{points:starPts(x,y,17,8),fill:fill,stroke:'#1a1a1a','stroke-width':2.5});
    var right=side?side==='left':x>mid, a={x:right?x-22:x+22,y:below?y+30:y-12,'text-anchor':right?'end':'start','font-size':20,'font-weight':800};
    if(!label) return;
    var h=add('text',a,label); h.setAttribute('fill','#fffdf5'); h.setAttribute('stroke','#fffdf5'); h.setAttribute('stroke-width',6); h.setAttribute('stroke-linejoin','round'); h.setAttribute('aria-hidden','true');
    if(label) add('text',a,label).setAttribute('fill','#1a1a1a');
    return right?'left':'right';
  }
  /* The Nolan diamond. Must match chart_svg in _build/core.py. */
  function ndx(E,P){return 430+(E-P)/100*240} function ndy(E,P){return 296-(E+P-100)/100*240}

  function showResult(){
    var out=document.getElementById('lres');
    var m=/[#&]r=([^&]+)/.exec(location.hash), mine=get('le_life'), code=m?decodeURIComponent(m[1]):mine, picks=parse(code);
    if(!picks){
      out.innerHTML='<h1>No result here yet</h1><p>'+(m?'That link looks broken, or it comes from an older version of the quiz.':'You haven\'t finished the real-life quiz in this browser yet.')+'</p><p class="row"><a class="btn gold" href="index.html">Start your year</a></p>';
      return;
    }
    var isMine=code===mine, r=score(picks), cl=r.cls, you=isMine?'you':'they', You=isMine?'You':'They', your=isMine?'your':'their';
    if(isMine) put('le_life_ep',JSON.stringify({E:r.E,P:r.P,H:r.H,cls:cl.id}));
    out.innerHTML=(isMine?'':'<div class="note"><p>You\'re looking at someone else\'s year. <a href="index.html">Play your own</a> and this page will show where you two split.</p></div>')+
      '<div class="result-head">'+icon(cl.icon,'typeic',88)+'<div><p class="kicker">'+(isMine?'Your character':'Their character')+'</p><h1>'+esc(cl.name)+'</h1><p class="lead">'+esc(cl.short)+'</p></div></div>'+
      '<p>'+esc(cl.long)+'</p><div class="note"><p><b>The case against this character:</b> '+esc(cl.argue)+'</p></div>';

    /* Character sheet */
    var top=r.hows[0];
    document.getElementById('lsheet').innerHTML='<ul class="bars">'+
      bar('Economic freedom',r.E,'How often '+you+' handled money and business without bringing in the government.')+
      bar('Personal freedom',r.P,'How often '+you+' left people to run their own lives.')+
      bar('Liberty',r.L,'The two freedoms together. This sets '+your+' place on the chart below.')+
      bar('Care',r.H,'How well '+your+' choices looked after the people involved. Scored on its own, because liberty and kindness are different questions.')+
      '</ul><ul class="facts"><li><b>Called the authorities:</b> '+r.cops+' of '+r.chances+' times '+you+' had the option.</li>'+
      '<li><b>Signature move:</b> '+esc(HW[top.id].label.toLowerCase())+', '+top.n+' of '+r.total+' choices.</li></ul>';
    var map=document.querySelector('#lmap svg');
    if(map){plot(map,70+r.L*4.2,30+(100-r.H)*4.2,'','#f5c400',false,280);
      var md=map.querySelector('desc'); if(md) md.textContent+=' A gold star marks '+(isMine?'you':'them')+': liberty '+r.L+', care '+r.H+'.';}

    /* What you say and what you do */
    var nsvg=document.querySelector('#lchart svg'), say=null;
    try{say=JSON.parse(get('le_mine_ep')||'null');}catch(e){}
    var t='', reg=region(r.E,r.P);
    if(nsvg){
      var doSide=plot(nsvg,ndx(r.E,r.P),ndy(r.E,r.P),isMine?'What you do':'What they do','#f5c400',false,430);
      var nd=nsvg.querySelector('desc'); if(nd) nd.textContent+=' A gold star marks what '+you+' did: economic freedom '+r.E+', personal freedom '+r.P+'.';
      if(isMine&&say){
        var close=Math.hypot(ndx(say.E,say.P)-ndx(r.E,r.P),ndy(say.E,say.P)-ndy(r.E,r.P))<60;
        plot(nsvg,ndx(say.E,say.P),ndy(say.E,say.P),'What you say','#ffffff',false,430,close?(doSide==='left'?'right':'left'):null);
        if(nd) nd.textContent+=' A white star marks what you said on the purity test: economic freedom '+say.E+', personal freedom '+say.P+'.';
      }
    }
    t+='<p>By what '+you+' did, '+you+' land in the <b>'+reg+'</b> part of the chart: economic freedom '+r.E+', personal freedom '+r.P+'.</p>';
    if(isMine&&say){
      var sl=Math.round((say.E+say.P)/2), gap=r.L-sl, dE=r.E-say.E, dP=r.P-say.P, big=Math.abs(dE)>=Math.abs(dP)?['economic freedom',say.E,r.E]:['personal freedom',say.P,r.P];
      if(Math.abs(gap)<8) t+='<div class="note"><p><b>What you say and what you do line up.</b> The purity test put your liberty at '+sl+', and your choices put it at '+r.L+'. That\'s rarer than it sounds.</p></div>';
      else if(gap<0) t+='<div class="note"><p><b>You talk a bigger liberty game than you play.</b> The purity test put your liberty at '+sl+'. When it was your neighbor, your cousin and your street, you landed at '+r.L+'. The gap is widest on '+big[0]+': '+big[1]+' said, '+big[2]+' done.</p></div>';
      else t+='<div class="note"><p><b>You\'re more libertarian in practice than on paper.</b> The purity test put your liberty at '+sl+', and your choices put it at '+r.L+'. The statements may sound scarier in the abstract than the people do up close. The gap is widest on '+big[0]+': '+big[1]+' said, '+big[2]+' done.</p></div>';
    } else if(isMine){
      t+='<p><a class="btn ghost" href="../quiz.html">Take the purity test</a> and come back. Your answers there show up on this chart as a white star, next to what you actually did.</p>';
    }
    document.getElementById('lsaydo').innerHTML=t;

    /* How you fix things */
    var h='<p class="lead">'+(isMine?'Your':'Their')+' most common move when something went wrong: <b>'+esc(HW[top.id].label.toLowerCase())+'</b>.</p><p>'+esc(HW[top.id].line)+'</p><ul class="bars">';
    r.hows.forEach(function(x){h+=bar(HW[x.id].label,Math.round(100*x.n/r.total),x.n+' of '+r.total+' choices',true);});
    document.getElementById('lhow').innerHTML=h+'</ul>';

    /* Theory of change */
    var lead=r.areas[0], th='<p class="lead">Every choice here was a bet about what would make things better for the people involved. That\'s a theory of change. A vote is the same bet, made for a whole country. Here\'s '+your+'s, ranked by how far '+you+' leaned.</p>';
    if(Math.abs(lead.lean-50)>=10) th+='<div class="note"><p><b>'+(isMine?'Your':'Their')+' theory of change, in one line:</b> '+esc(lead.lean>50?lead.area.free:lead.area.state)+'</p></div>';
    th+='<ol class="prio">';
    r.areas.forEach(function(p){
      var dir=p.lean>=60?'Less state':p.lean<=40?'More state':'Split';
      th+='<li>'+icon(p.area.icon)+'<div><p class="ph"><b>'+esc(p.area.name)+'</b> <span class="badge '+(dir==='Less state'?'yes':dir==='More state'?'no':'mid')+'">'+dir+'</span></p><ul class="bars">'+
        bar('Liberty in what '+you+' did',p.lean,p.cops?(You+' called the authorities '+p.cops+(p.cops>1?' times':' time')+' here.'):'')+'</ul><p>'+
        esc(dir==='Less state'?p.area.free:dir==='More state'?p.area.state:'Pulled both ways here. That usually means it depends on who the person is, or how close to home it lands.')+'</p></div></li>';
    });
    th+='</ol><p>If '+your+' theory is right, '+you+' should be able to win over a neighbor who chose differently. That\'s the whole job of politics, and it\'s the part most people skip.</p>';
    document.getElementById('ltheory').innerHTML=th;

    /* Journal, and where two players split */
    var minePicks=(!isMine&&mine)?parse(mine):null, mineAt={};
    if(minePicks){var mw=walk(minePicks).seq; mw.forEach(function(id,k){mineAt[id]=minePicks[k];});}
    var j='', splits=[];
    r.seq.forEach(function(id,k){
      var sc=SC[id], c=sc.c[picks[k]], other=(minePicks&&mineAt[id]!==undefined&&mineAt[id]!==picks[k])?sc.c[mineAt[id]]:null;
      if(other) splits.push('<li><b>'+esc(sc.t)+'.</b> They: '+esc(c.a)+' You: '+esc(other.a)+'</li>');
      j+='<li><h3>'+esc(sc.t)+' <span class="qnum">'+esc(CH[sc.ch])+'</span></h3><p class="situ">'+esc(sc.s)+'</p>'+
        '<p><b>'+You+' chose:</b> '+esc(c.a)+'</p>'+(other?'<p><b>You chose:</b> '+esc(other.a)+'</p>':'')+
        '<p><b>What it shows:</b> '+esc(c.says)+'</p>'+(c.after?'<p><b>What happened:</b> '+esc(c.after)+'</p>':'')+
        '<p class="against"><b>The case against:</b> '+esc(c.push)+'</p></li>';
    });
    var sp='';
    if(minePicks) sp=splits.length?'<div class="note"><p><b>Where you two split, '+splits.length+' of '+r.total+' situations.</b> Each one is an argument worth having.</p><ul>'+splits.join('')+'</ul></div>'
      :'<div class="note"><p><b>You two made the same choice every time.</b> Find someone who didn\'t.</p></div>';
    document.getElementById('ljournal').innerHTML=sp+'<ol class="journal">'+j+'</ol>';

    /* Share */
    var url=location.origin+location.pathname+'#r='+code, inp=document.getElementById('lshare'), msg=document.getElementById('lcopymsg');
    inp.value=url;
    document.getElementById('lcopy').addEventListener('click',function(){
      function ok(){msg.textContent='Copied. Send it to someone who\'d choose differently.';}
      function fb(){inp.focus(); inp.select(); try{if(document.execCommand('copy')) ok();}catch(e){}}
      if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok,fb); else fb();
    });
    var nat=document.getElementById('lnative');
    if(navigator.share){nat.hidden=false; nat.addEventListener('click',function(){navigator.share({title:'I\'m '+cl.name+'. What would you actually do?',url:url}).catch(function(){});});}
    document.getElementById('lafter').hidden=false;
  }

  if(document.getElementById('life')) play();
  if(document.getElementById('lres')) showResult();
})();
