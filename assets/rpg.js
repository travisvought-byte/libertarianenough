/* Herding Porcupines: a coalition RPG. Your game is saved in this browser only. Nothing is sent anywhere.
   Every number the game uses is shown on screen: the odds you see are the odds you roll. */
(function(){
  var R=window.RPG, root=document.getElementById('rpg'); if(!R||!root) return;
  var KEY='le_rpg', FAME='le_rpg_fame', TS=32, W=R.town[0].length, H=R.town.length;
  var FAC={}, BYPLACE={}, CAMP={}, PL={}, DOOR={}, BOX={}, EXIT={};
  R.factions.forEach(function(f){FAC[f.id]=f; BYPLACE[f.place]=f;});
  R.campaigns.forEach(function(c){CAMP[c.id]=c;});
  Object.keys(R.places).forEach(function(k){R.places[k].key=k; PL[R.places[k].id]=R.places[k];});
  R.town.forEach(function(row,y){row.split('').forEach(function(ch,x){
    var up=ch.toUpperCase(), p=R.places[up]; if(!p) return;
    var b=BOX[up]||(BOX[up]={x0:x,x1:x,y0:y,y1:y});
    b.x0=Math.min(b.x0,x); b.x1=Math.max(b.x1,x); b.y0=Math.min(b.y0,y); b.y1=Math.max(b.y1,y);
    if(ch!==up) DOOR[p.id]=[x,y];
  });});
  var START_DOUBT={'2':60,'1':90,'0':120,'-1':150,'-2':180};
  var REDUCED=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function put(k,v){try{if(v===null) localStorage.removeItem(k); else localStorage.setItem(k,v);}catch(e){}}
  function json(k){try{return JSON.parse(get(k)||'null')}catch(e){return null}}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
  function first(n){return n.replace(/^(Sgt\.|Pastor|Deputy)\s+/,'').split(' ')[0]}
  function lens(id){var l=R.lenses[id]; return '<span class="rpg-lens">'+l.icon+' '+esc(l.name)+'</span>';}
  function tile(x,y){return (x<0||y<0||x>=W||y>=H)?'T':R.town[y][x]}
  function doorAt(x,y){var ch=tile(x,y), p=R.places[ch.toUpperCase()]; return (p&&ch!==ch.toUpperCase())?p.id:null}
  function walkable(x,y){var ch=tile(x,y); return '.:=,'.indexOf(ch)>=0||!!doorAt(x,y)}
  Object.keys(DOOR).forEach(function(id){var d=DOOR[id];
    [[0,1],[0,-1],[1,0],[-1,0]].some(function(o){var x=d[0]+o[0],y=d[1]+o[1]; if(walkable(x,y)&&!doorAt(x,y)){EXIT[id]=[x,y]; return true;} return false;});
  });

  /* ---------- state ---------- */
  var S=null, C=null, steps=null, frame=0, facing='down';
  function save(){if(S) put(KEY,JSON.stringify(S));}
  function load(){var s=json(KEY); return (s&&s.v===R.version&&CAMP[s.camp]&&R.classes[s.cls])?s:null;}
  function rand(){S.seed=(S.seed+0x6D2B79F5)|0; var t=S.seed; t=Math.imul(t^t>>>15,t|1); t^=t+Math.imul(t^t>>>7,t|61); return ((t^t>>>14)>>>0)/4294967296;}
  function CL(){return R.classes[S.cls]}
  function CA(){return CAMP[S.camp]}
  function maxHp(){return CL().hp+4*(S.lvl-1)}
  function quizL(){var m=json('le_mine_ep'); if(!m||isNaN(+m.E)||isNaN(+m.P)) return null; return Math.round((+m.E + +m.P)/2);}
  function startUnity(){var L=quizL(); return L===null?60:clamp(60+Math.round((L-50)/5),45,75);}

  function newGame(camp,cls){
    S={v:R.version,camp:camp,cls:cls,day:R.days,unity:startUnity(),lib:100,xp:0,lvl:1,seed:(Date.now()%2147483647)|0,
       pos:R.start.slice(),fac:{},deals:[],evq:[],hits:{},answered:0,meetings:0,talk:{},done:null};
    R.factions.forEach(function(f){var st=f.stance[camp];
      S.fac[f.id]={doubt:START_DOUBT[String(st)],trust:0,state:st<0?'opposed':'neutral',known:[],cold:false,talks:0};});
    var ev=R.events.map(function(e){return e.id});
    for(var i=ev.length-1;i>0;i--){var j=Math.floor(rand()*(i+1)), t=ev[i]; ev[i]=ev[j]; ev[j]=t;}
    S.evq=ev; save();
  }
  function gainXp(n){
    S.xp+=n; var said=[];
    while(S.lvl<5&&S.xp>=S.lvl*50){S.lvl++; said.push('You reached level '+S.lvl+'. Composure up 4, arguments 4% stronger.'); if(C) C.hp+=4;}
    return said;
  }
  function setUnity(d){S.unity=clamp(S.unity+d,0,100);}
  /* Move groups: negative means less doubt. Keys: a group id, "*" everyone, "ally" your allies, or a lens ("fair") for everyone who cares about it. */
  function moveGroups(move){
    var out=[];
    Object.keys(move).forEach(function(k){
      R.factions.forEach(function(f){
        var hit=k==='*'||k===f.id||(k==='ally'&&S.fac[f.id].state==='ally')||(R.lenses[k]&&f.cares.indexOf(k)>=0);
        if(hit){S.fac[f.id].doubt+=move[k]; out=out.concat(settle(f.id));}
      });
    });
    return out;
  }
  /* The rules for where a group stands. Allies stay allies unless something pushes their doubt past 15.
     Groups fighting the measure stop fighting under 100 doubt. Anyone pushed to 160 starts fighting it. */
  function settle(id){
    var s=S.fac[id], f=FAC[id], out=[];
    if(s.state==='ally'&&s.doubt>15){s.state='neutral'; out.push(f.who+' backed off. '+f.org+' is undecided again.');}
    if(s.state==='opposed'&&s.doubt<100){s.state='neutral'; out.push(f.org+' stopped fighting the measure.');}
    if(s.state==='neutral'&&s.doubt>=160){s.state='opposed'; out.push(f.org+' is now fighting the measure.');}
    if(s.state!=='ally'&&s.doubt<=0){s.state='ally'; s.doubt=Math.min(s.doubt,0); out.push(f.org+' joined your coalition.'); out=out.concat(gainXp(30));}
    return out;
  }
  function lean(id){var s=S.fac[id].state; return s==='ally'?1:s==='opposed'?-1:0}
  function allies(){return R.factions.filter(function(f){return S.fac[f.id].state==='ally'})}
  var STATE_WORD={ally:'with you',neutral:'undecided',opposed:'fighting it'};
  function votes(){
    var al=allies(), side={}; al.forEach(function(f){side[f.side]=1;});
    return R.council.map(function(m){
      if(!m.groups.length){
        var miss=[];
        if(al.length<R.lin.allies) miss.push('wants at least '+R.lin.allies+' groups behind it (you have '+al.length+')');
        if(!(side.left&&side.right)) miss.push('wants allies from both sides of the aisle');
        if(S.unity<R.lin.unity) miss.push('saw your own party fighting you (unity under '+R.lin.unity+')');
        return {m:m,yes:!miss.length,why:miss.length?'Lin '+miss.join(', and ')+'.':'Lin saw a coalition from both sides and a party standing behind it.'};
      }
      var sum=0, parts=m.groups.map(function(g){sum+=lean(g); return FAC[g].org+' '+STATE_WORD[S.fac[g].state];});
      return {m:m,yes:sum>=1,why:parts.join('; ')+'.'};
    });
  }
  function yesCount(){return votes().filter(function(v){return v.yes}).length}

  /* ---------- page skeleton ---------- */
  root.innerHTML='<div id="rpg-hud" hidden></div>'+
    '<div id="rpg-world" hidden><div class="rpg-mapwrap"><canvas id="rpg-map" width="'+W*TS+'" height="'+H*TS+'" tabindex="0" role="application" '+
    'aria-label="Map of Porter County. Arrow keys or W A S D walk. Step into a door to go inside. The list of places below the map does the same thing." aria-describedby="rpg-where"></canvas></div>'+
    '<p class="rpg-where" id="rpg-where"></p>'+
    '<div class="rpg-pad" role="group" aria-label="Walk"><button type="button" data-go="0,-1" aria-label="Walk up">▲</button><button type="button" data-go="-1,0" aria-label="Walk left">◀</button><button type="button" data-go="0,1" aria-label="Walk down">▼</button><button type="button" data-go="1,0" aria-label="Walk right">▶</button></div>'+
    '<h3 class="rpg-h">Places in town</h3><ul class="rpg-places" id="rpg-places"></ul>'+
    '<details class="rpg-notes"><summary>Your notebook: who cares about what</summary><div id="rpg-book"></div></details>'+
    '<div class="row rpg-foot"><button type="button" class="btn ghost small" id="rpg-quit">Back to the title screen</button></div></div>'+
    '<div id="rpg-panel" hidden></div><p class="sr" id="rpg-live" aria-live="polite"></p>';
  var hud=root.querySelector('#rpg-hud'), world=root.querySelector('#rpg-world'), panel=root.querySelector('#rpg-panel'),
      cv=root.querySelector('#rpg-map'), ctx=cv.getContext&&cv.getContext('2d'), liveEl=root.querySelector('#rpg-live');
  function live(t){liveEl.textContent=''; setTimeout(function(){liveEl.textContent=t;},30);}
  var booted=false;
  function focusHead(){var h=panel.querySelector('h3'); if(h&&booted){h.setAttribute('tabindex','-1'); h.focus();}}
  function screen(html,mode){
    world.hidden=mode!=='world'; panel.hidden=mode==='world'; hud.hidden=!S||mode==='title'||mode==='make';
    if(mode!=='world'){panel.innerHTML=html; focusHead(); booted=true;}
    if(!hud.hidden) drawHud();
    if(mode!=='world'&&root.getBoundingClientRect&&root.getBoundingClientRect().top<0&&root.scrollIntoView) root.scrollIntoView({block:'start'});
  }
  function drawHud(){
    var y=yesCount(), hp=C?C.hp+' of '+maxHp():maxHp();
    hud.innerHTML='<ul class="rpg-hud">'+
      '<li><span class="k">Days left</span> <b>'+S.day+'</b></li>'+
      '<li><span class="k">Composure</span> <b>'+hp+'</b></li>'+
      '<li><span class="k">Level</span> <b>'+S.lvl+'</b> <span class="sm">('+S.xp+' XP)</span></li>'+
      '<li'+(S.unity<R.lin.unity?' class="bad"':'')+'><span class="k">Party unity</span> <b>'+S.unity+'</b></li>'+
      '<li'+(y>=3?' class="good"':'')+'><span class="k">Votes</span> <b>'+y+' of 5</b> <span class="sm">(need 3)</span></li>'+
      '<li><span class="k">Liberty kept</span> <b>'+S.lib+'%</b></li></ul>';
  }
  function face(f){return '<canvas class="rpg-face" width="64" height="64" aria-hidden="true" data-face="'+esc(JSON.stringify(f))+'"></canvas>'}
  function paintFaces(){var cs=panel.querySelectorAll('canvas[data-face]'); for(var i=0;i<cs.length;i++) portrait(cs[i],JSON.parse(cs[i].getAttribute('data-face')));}
  function stateTag(id){var s=S.fac[id].state; return '<span class="rpg-st '+s+'">'+(s==='ally'?'✓ With you':s==='opposed'?'× Fighting it':'? Undecided')+'</span>'}

  /* ---------- title and setup ---------- */
  function showTitle(){
    S=load(); C=null;
    var cont=S&&!S.done, fame=json(FAME)||[];
    var h='<div class="rpg-title"><p class="rpg-logo" aria-hidden="true">🦔🦔🦔</p><h3>Herding Porcupines</h3>'+
      '<p>Porter County votes in '+R.days+' days. You have a good idea and a party that agrees about almost nothing. Win over the people in town, keep your own side together, and count to three.</p>'+
      '<div class="row">'+(cont?'<button class="btn gold" type="button" data-a="continue">Continue: '+esc(CA().name)+', '+S.day+' days left</button><button class="btn ghost" type="button" data-a="new">New game</button>':'<button class="btn gold" type="button" data-a="new">New game</button>')+'</div>'+
      '<div id="rpg-confirm"></div>';
    if(fame.length){
      h+='<h4>Hall of fame on this device</h4><ol class="rpg-fame">'+fame.slice(0,5).map(function(r){return '<li><b>'+esc(r.rank)+'</b>: '+esc(r.camp)+', '+esc(r.vote)+' as '+esc(r.cls)+' <span class="sm">('+esc(r.date)+')</span></li>'}).join('')+'</ol>';
    }
    screen(h+'</div>','title');
  }
  function showMake(){
    var life=json('le_life_ep'), had=life&&R.classes[life.cls]?life.cls:null, L=quizL();
    var h='<h3>Who are you, and what are you fighting for?</h3><form id="rpg-make" class="rpg-make">'+
      '<fieldset><legend>Pick a measure</legend>'+R.campaigns.map(function(c,i){
        return '<label class="rpg-opt"><input type="radio" name="camp" value="'+c.id+'"'+(i===0?' checked':'')+'> <span><b>'+esc(c.name)+'</b> <span class="sm">('+esc(c.level)+')</span><br>'+esc(c.pitch)+'</span></label>';}).join('')+'</fieldset>'+
      '<fieldset><legend>Your character</legend>'+(had?'<p class="sm">Picked from your result on <a href="../life/index.html">the real-life quiz</a>. Change it if you like.</p>':'<p class="sm">Take <a href="../life/index.html">the real-life quiz</a> and the game picks the character your choices earned. Or pick one now.</p>')+
      Object.keys(R.classes).map(function(k,i){var c=R.classes[k];
        return '<label class="rpg-opt"><input type="radio" name="cls" value="'+k+'"'+((had?k===had:i===0)?' checked':'')+'> <span><b>'+c.icon+' '+esc(c.name)+'</b><br>Argues best from '+c.lenses.map(function(l){return esc(R.lenses[l].name.toLowerCase())}).join(', ')+'. '+esc(c.perk)+'</span></label>';}).join('')+'</fieldset>'+
      '<p class="sm">Your party starts at <b>'+startUnity()+'</b> unity. '+(L===null?'Take <a href="../quiz.html">the purity test</a> and your score sets this: purer libertarians start with a party that trusts them more.':'That comes from your purity test score of '+L+'.')+'</p>'+
      '<div class="row"><button class="btn gold" type="submit">Start the campaign</button><button class="btn ghost" type="button" data-a="title">Back</button></div></form>';
    screen(h,'make');
    panel.querySelector('#rpg-make').addEventListener('submit',function(ev){
      ev.preventDefault(); var fd=ev.target;
      newGame(fd.querySelector('input[name=camp]:checked').value, fd.querySelector('input[name=cls]:checked').value);
      showIntro();
    });
  }
  function showIntro(){
    var c=CA();
    screen('<h3>Day 1: '+esc(c.name)+'</h3><p>'+esc(c.pitch)+' The county council votes in '+R.days+' days. Five members, and you need three.</p>'+
      '<ul class="facts"><li><b>Each conversation uses a day.</b> So does a caucus meeting. Walking around and checking the whip count are free.</li>'+
      '<li><b>Listen first.</b> People tell you what they care about. An argument aimed at what they care about hits much harder.</li>'+
      '<li><b>Answer the worry they raise.</b> Match the value in their objection and it doesn\'t cost you any composure.</li>'+
      '<li><b>Count votes.</b> Each ward member listens to two groups. Stop by the County Building for the whip count.</li></ul>'+
      '<p>Start at Party HQ. Dev has the whip math, Elinor has advice, and Rex has opinions.</p>'+
      '<div class="row"><button class="btn gold" type="button" data-a="world">Go to town</button></div>','intro');
  }

  /* ---------- the town ---------- */
  function showWorld(msg){
    C=null; save(); screen('','world'); drawMap(); renderPlaces(); renderBook(); whereAmI();
    if(msg) live(msg);
    cv.focus();
  }
  function placeLabel(id){
    var p=PL[id], f=BYPLACE[id];
    if(id==='hq') return 'Party HQ: Rex, Elinor and Dev';
    if(id==='county') return 'County Building: whip count and the vote';
    return p.name+': '+f.who+', '+f.org+' ('+STATE_WORD[S.fac[f.id].state]+')';
  }
  function renderPlaces(){
    var ul=root.querySelector('#rpg-places'), ids=['hq','county'].concat(R.factions.map(function(f){return f.place}));
    ul.innerHTML=ids.map(function(id){var f=BYPLACE[id];
      return '<li><button type="button" class="rpg-go" data-place="'+id+'">'+(f?'<span class="rpg-st '+S.fac[f.id].state+'" aria-hidden="true">'+(S.fac[f.id].state==='ally'?'✓':S.fac[f.id].state==='opposed'?'×':'?')+'</span> ':'')+esc(placeLabel(id))+'</button></li>'}).join('');
  }
  function renderBook(){
    var b=root.querySelector('#rpg-book');
    b.innerHTML='<p class="sm">Cares are what you\'ve learned by listening or by an argument that landed. Doubt is how far each group is from joining you: 0 means they\'re in.</p><div class="tablewrap"><table><thead><tr><th scope="col">Group</th><th scope="col">Side</th><th scope="col">Where they stand</th><th scope="col">Doubt</th><th scope="col">What they care about</th></tr></thead><tbody>'+
      R.factions.map(function(f){var s=S.fac[f.id];
        return '<tr><th scope="row">'+esc(f.who)+'<br><span class="sm">'+esc(f.org)+'</span></th><td>'+(f.side==='left'?'Left':'Right')+'</td><td>'+stateTag(f.id)+'</td><td>'+Math.max(0,s.doubt)+'</td><td>'+
          (s.known.length?s.known.map(lens).join(' '):'<span class="sm">Not yet known</span>')+(s.cold?'<br><span class="sm">'+R.lenses[f.cold].name+' falls flat</span>':'')+'</td></tr>'}).join('')+'</tbody></table></div>';
  }
  function whereAmI(){
    var x=S.pos[0], y=S.pos[1], near=null;
    Object.keys(DOOR).forEach(function(id){var d=DOOR[id]; if(Math.abs(d[0]-x)+Math.abs(d[1]-y)<=2) near=id;});
    root.querySelector('#rpg-where').textContent=near?'You\'re near '+PL[near].name+'.':'You\'re walking through town.';
  }
  function travel(id){S.pos=EXIT[id].slice(); enter(id);}
  function enter(id){steps=null; save(); showPlace(id);}
  function step(dx,dy){
    if(!S||world.hidden) return;
    facing=dy<0?'up':dy>0?'down':dx<0?'left':'right';
    var x=S.pos[0]+dx, y=S.pos[1]+dy;
    if(!walkable(x,y)){drawMap(); return;}
    frame^=1; var d=doorAt(x,y);
    if(d){drawMap(); enter(d); return;}
    S.pos=[x,y]; save(); drawMap(); whereAmI();
  }
  function path(to){
    var key=function(x,y){return x+','+y}, prev={}, q=[S.pos.slice()], seen={}; seen[key(S.pos[0],S.pos[1])]=1;
    while(q.length){var c=q.shift(); if(c[0]===to[0]&&c[1]===to[1]) break;
      [[0,1],[0,-1],[1,0],[-1,0]].forEach(function(o){var x=c[0]+o[0], y=c[1]+o[1], k=key(x,y);
        if(seen[k]||!walkable(x,y)) return; if(doorAt(x,y)&&!(x===to[0]&&y===to[1])) return;
        seen[k]=1; prev[k]=c; q.push([x,y]);});}
    if(!seen[key(to[0],to[1])]) return null;
    var out=[], c=to; while(!(c[0]===S.pos[0]&&c[1]===S.pos[1])){out.unshift(c); c=prev[key(c[0],c[1])];}
    return out;
  }
  function walkTo(to){
    var p=path(to); if(!p||!p.length) return;
    if(REDUCED){var last=p[p.length-1]; p.slice(0,-1).forEach(function(c){S.pos=c;}); step(last[0]-S.pos[0],last[1]-S.pos[1]); return;}
    steps=p; (function tick(){ if(!steps||!steps.length) return; var c=steps.shift(); step(c[0]-S.pos[0],c[1]-S.pos[1]); if(steps&&steps.length) setTimeout(tick,85); })();
  }

  /* ---------- places ---------- */
  function showPlace(id){
    if(id==='hq') return showHQ();
    if(id==='county') return showCounty();
    var f=BYPLACE[id], s=S.fac[f.id], p=PL[id];
    var h='<div class="rpg-who">'+face(f.face)+'<div><h3>'+esc(p.name)+'</h3><p><b>'+esc(f.who)+'</b>, '+esc(f.org)+' · '+(f.side==='left'?'left':'right')+' of the aisle · '+stateTag(f.id)+'</p></div></div>';
    if(s.state==='ally'){
      h+='<p>'+esc(f.joined)+'</p><p class="sm">'+esc(first(f.who))+' is with you. Keep it that way: a deal or a stunt that pushes their doubt past 15 sends them back to undecided.</p>';
    } else {
      h+='<p>'+esc(f.hello)+'</p><p class="sm">Doubt '+Math.max(0,s.doubt)+(s.known.length?'. You know they care about '+s.known.map(function(l){return R.lenses[l].name.toLowerCase()}).join(', ')+'.':'. You don\'t know yet what they care about.')+'</p>'+
         '<div class="row"><button class="btn gold" type="button" data-a="talk" data-f="'+f.id+'">Talk with '+esc(first(f.who))+' (uses a day, '+S.day+' left)</button></div>';
    }
    h+='<div class="row"><button class="btn ghost" type="button" data-a="world">Back to town</button></div>';
    screen(h,'place'); paintFaces();
  }
  function showHQ(){
    var h='<h3>Party HQ</h3><p>Folding chairs, a coffee maker older than the party, and a yellow flag with a porcupine on it. Party unity is <b>'+S.unity+'</b>. Under '+R.lin.unity+', the Purity Caucus campaigns against your measure and Councilmember Lin votes no.</p><div class="rpg-caucus">'+
      R.caucus.map(function(c){var n=S.talk[c.id]||0;
        return '<div class="card"><div class="rpg-who">'+face(c.face)+'<div><h4>'+esc(c.who)+'</h4><p class="sm">'+esc(c.org)+'</p></div></div><p id="rpg-say-'+c.id+'">'+(n?esc(c.talk[(n-1)%c.talk.length]):'')+'</p><button class="btn small ghost" type="button" data-a="chat" data-c="'+c.id+'">Talk to '+esc(c.who.split(' ')[0])+' (free)</button></div>'}).join('')+'</div>'+
      (S.meetings<2?'<div class="row"><button class="btn" type="button" data-a="meeting">Hold a caucus meeting (uses a day, '+S.day+' left)</button></div>':'<p class="sm">You\'ve held two caucus meetings. Nobody will come to a third.</p>')+
      '<div class="row"><button class="btn ghost" type="button" data-a="world">Back to town</button></div>';
    screen(h,'place'); paintFaces();
  }
  function whipTable(v){
    return '<div class="tablewrap"><table class="rpg-whip"><caption>Whip count: '+v.filter(function(x){return x.yes}).length+' of 5 would vote yes today</caption><thead><tr><th scope="col">Council member</th><th scope="col">Vote</th><th scope="col">Why</th></tr></thead><tbody>'+
      v.map(function(x){return '<tr><th scope="row">'+esc(x.m.who)+'<br><span class="sm">'+esc(x.m.ward)+'</span></th><td class="'+(x.yes?'yes':'no')+'">'+(x.yes?'✓ Yes':'× No')+'</td><td>'+esc(x.why)+'</td></tr>'}).join('')+'</tbody></table></div>';
  }
  function showCounty(confirm){
    var v=votes(), h='<h3>County Building</h3><p>The clerk lets you look at the whip count. A ward member votes yes when the two groups they answer to add up in your favor: an ally counts +1, a group fighting it counts −1. A tie is a no.</p>'+whipTable(v);
    h+=confirm?'<div class="warn"><p>Call the vote now with '+S.day+' days left? There\'s no second try.</p><div class="row"><button class="btn gold" type="button" data-a="vote">Yes, call the vote</button><button class="btn ghost" type="button" data-a="county">Not yet</button></div></div>':
      '<div class="row"><button class="btn" type="button" data-a="askvote">Call the vote now</button><button class="btn ghost" type="button" data-a="world">Back to town</button></div>';
    screen(h,'place');
  }
  function showMeeting(){
    var m=R.meeting;
    screen('<h3>'+esc(m.title)+'</h3><p>'+esc(m.text)+'</p><div class="rpg-choices">'+m.opts.map(function(o,i){return '<button class="btn ghost" type="button" data-a="meet" data-i="'+i+'">'+esc(o.label)+'</button>'}).join('')+'</div>','place');
  }
  function eventScreen(ev,pick){
    if(pick==null){
      screen('<h3>'+esc(ev.title)+'</h3><p>'+esc(ev.text)+'</p><div class="rpg-choices">'+ev.opts.map(function(o,i){return '<button class="btn ghost" type="button" data-a="ev" data-e="'+ev.id+'" data-i="'+i+'">'+esc(o.label)+'</button>'}).join('')+'</div>','event');
      return;
    }
    var o=ev.opts[pick], u=o.unity||0; setUnity(u); var said=moveGroups(o.move);
    save();
    screen('<h3>'+esc(ev.title)+'</h3><p><b>You chose:</b> '+esc(o.label)+'.</p><p>'+esc(o.then)+'</p>'+effects(o.move,u,said)+
      '<div class="row"><button class="btn gold" type="button" data-a="world">Back to town</button></div>','event');
  }
  function effects(move,u,said){
    var li=[];
    if(u) li.push('Party unity '+(u>0?'+':'−')+Math.abs(u)+'.');
    Object.keys(move).forEach(function(k){var v=move[k], who=k==='*'?'Every group':k==='ally'?'Your allies':R.lenses[k]?'Everyone who cares about '+R.lenses[k].name.toLowerCase():FAC[k].org;
      li.push(who+': '+(v<0?'doubt −'+(-v)+' (good)':'doubt +'+v+' (bad)')+'.');});
    li=li.concat(said||[]);
    return li.length?'<ul class="rpg-fx">'+li.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ul>':'';
  }
  function afterDay(msg){
    save();
    if(S.day<=0) return finish();
    if(S.day%2===0&&S.evq.length){var id=S.evq.shift(); save(); var ev=R.events.filter(function(e){return e.id===id})[0]; return eventScreen(ev);}
    showWorld(msg);
  }

  /* ---------- conversations ---------- */
  function talk(id){
    S.day--; S.fac[id].talks++;
    var f=FAC[id];
    C={f:id,hp:maxHp(),pat:4,oi:0,ans:false,used:{},cg:false,lines:[{who:f.who,t:f.hello}],sub:null,over:null};
    save(); drawTalk();
  }
  function obj(){return FAC[C.f].objections[C.oi%FAC[C.f].objections.length]}
  function trustMult(){return 1+0.15*S.fac[C.f].trust}
  function lvlMult(){return 1+0.04*(S.lvl-1)}
  function askOdds(){var s=S.fac[C.f], p=0.9-Math.max(0,s.doubt)/80+0.06*s.trust+(S.cls==='fixer'?0.1:0); p=clamp(p,0.05,0.95); var n=Math.ceil(21-20*p); return {p:p,n:n,pct:Math.round((21-n)*5)};}
  function argPower(a){
    var f=FAC[C.f], m=1, why=[];
    if(f.cares.indexOf(a[0])>=0){m*=2.2; why.push('they care');} else if(f.cold===a[0]){m*=0.2; why.push('falls flat');} else m*=0.5;
    if(CL().lenses.indexOf(a[0])>=0){m*=1.25; why.push('your strength');}
    if(a[0]===obj()[0]) m*=1.25;
    var u=C.used[a[0]]||0; m*=Math.pow(0.5,u);
    return {v:Math.round(a[1]*m*trustMult()*lvlMult()),why:why,repeat:u};
  }
  function say(who,t){C.lines.push({who:who,t:t}); if(C.lines.length>5) C.lines.shift();}
  function drawTalk(){
    var f=FAC[C.f], s=S.fac[f.id], o=obj(), od=askOdds();
    var h='<div class="rpg-talk"><div class="rpg-who">'+face(f.face)+'<div><h3>'+esc(f.who)+'</h3><p>'+esc(f.org)+' · '+stateTag(f.id)+'</p></div></div>'+
      '<ul class="rpg-meters">'+
      meter('Doubt',Math.max(0,s.doubt),180,'doubt','0 means they join you')+
      meter('Your composure',C.hp,maxHp(),'hp','')+
      '<li><span class="k">Trust</span> <b>'+'★★★'.slice(0,s.trust)+'☆☆☆'.slice(0,3-s.trust)+'</b> <span class="sm">(arguments +'+s.trust*15+'%)</span></li>'+
      '<li><span class="k">Patience</span> <b>'+C.pat+' turns</b></li></ul>'+
      '<ol class="rpg-lines">'+C.lines.map(function(l){return '<li class="'+(l.who==='You'?'me':l.who===''?'sys':'them')+'">'+(l.who?'<b>'+esc(l.who)+':</b> ':'')+esc(l.t)+'</li>'}).join('')+'</ol>';
    if(C.over){
      h+='<p class="rpg-over">'+esc(C.over)+'</p><div class="row"><button class="btn gold" type="button" data-a="done">Back to town</button></div></div>';
      screen(h,'talk'); paintFaces(); return;
    }
    h+='<div class="rpg-obj"><p><b>'+esc(first(f.who))+' says:</b> "'+esc(o[1])+'"</p><p class="sm">This worry is about '+lens(o[0])+'. Answer with an argument about '+esc(R.lenses[o[0]].name.toLowerCase())+' and it won\'t cost you composure.</p></div>';
    if(C.sub==='args'){
      h+='<h4>Make a case</h4><ul class="rpg-cards">'+CA().args.map(function(a,i){var pw=argPower(a), tags=[];
          if(s.known.indexOf(a[0])>=0) tags.push('they care');
          if(s.cold&&f.cold===a[0]) tags.push('falls flat with them');
          if(a[0]===o[0]) tags.push('answers this worry');
          if(CL().lenses.indexOf(a[0])>=0) tags.push('your strength');
          if(pw.repeat) tags.push('used '+pw.repeat+'×, weaker');
          return '<li><button type="button" data-a="arg" data-i="'+i+'">'+lens(a[0])+' <span>'+esc(a[2])+'</span><span class="sm">Base '+a[1]+(tags.length?' · '+tags.join(' · '):'')+'</span></button></li>'}).join('')+
        '</ul><button class="btn ghost small" type="button" data-a="sub" data-s="">Cancel</button>';
    } else if(C.sub==='deals'){
      var open=CA().deals.filter(function(d){return S.deals.indexOf(d.id)<0});
      h+='<h4>Offer a deal</h4><p class="sm">A deal changes the measure for good, for everyone in town. It can win some groups and lose others, and your own party may not like it.</p><ul class="rpg-cards">'+
        (open.length?open.map(function(d){var u=S.cls==='fixer'&&d.unity>0?Math.ceil(d.unity/2):d.unity, fx=[];
          Object.keys(d.move).forEach(function(k){fx.push(FAC[k].org+' '+(d.move[k]<0?'−'+(-d.move[k]):'+'+d.move[k]))});
          return '<li><button type="button" data-a="deal" data-d="'+d.id+'"><b>'+esc(d.text)+'</b><span class="sm">Doubt: '+esc(fx.join(', '))+'. Party unity '+(u>0?'−'+u:'+'+(-u))+'. Liberty kept '+(d.liberty>0?'−'+d.liberty:d.liberty<0?'+'+(-d.liberty):'no change')+'.</span></button></li>'}).join(''):'<li>You\'ve made every deal on the table.</li>')+
        '</ul><button class="btn ghost small" type="button" data-a="sub" data-s="">Cancel</button>';
    } else {
      var cgOk=!C.cg&&s.known.length>0, shared=s.known.filter(function(l){return CL().lenses.indexOf(l)>=0});
      h+='<div class="rpg-acts">'+
        act('listen','👂 Listen','Learn what they care about. Trust +'+(S.cls==='caretaker'?2:1)+'. Their next jab hits half as hard.',s.trust>=3&&s.known.length>=f.cares.length)+
        act('args','💬 Make a case','Pick an argument. It hits much harder if they care about it.')+
        act('cg','🤝 Find common ground',cgOk?(shared.length?'You both care about '+shared.map(function(l){return R.lenses[l].name.toLowerCase()}).join(' and ')+'. Once per conversation.':'You haven\'t found a value you share yet. Once per conversation.'):C.cg?'You did this already.':'Listen first: you need to know one thing they care about.',!cgOk)+
        act('deals','📝 Offer a deal','Change the measure to win them over.')+
        act('slogan','📢 Say a slogan','Rex will love it. They won\'t.')+
        act('ask','🙋 Ask for support',s.state==='opposed'?'They\'re fighting the measure. Get their doubt under 100 first.':'Roll a d20: you need '+od.n+' or higher ('+od.pct+'% chance).',s.state==='opposed')+
        act('leave','🚪 Walk away','Thank them and go. What you\'ve won so far stays won.')+
        '</div>';
    }
    h+='</div>';
    screen(h,'talk'); paintFaces();
  }
  function act(a,label,sub,dis){return '<button class="rpg-act" type="button" data-a="'+(a==='args'||a==='deals'?'sub':'do')+'" data-s="'+a+'"'+(dis?' disabled':'')+'><b>'+label+'</b><span class="sm">'+esc(sub)+'</span></button>'}
  function meter(label,v,max,cls,note){var pct=clamp(Math.round(100*v/max),0,100);
    return '<li><span class="k">'+label+'</span> <b>'+v+'</b>'+(note?' <span class="sm">('+note+')</span>':'')+'<span class="rpg-bar '+cls+'" aria-hidden="true"><span style="width:'+pct+'%"></span></span></li>'}

  function doAct(a,arg){
    var f=FAC[C.f], s=S.fac[f.id], o=obj(), soft=false, said=[];
    C.sub=null;
    if(a==='listen'){
      var add=S.cls==='caretaker'?2:1, nxt=f.cares.filter(function(l){return s.known.indexOf(l)<0})[0];
      s.trust=Math.min(3,s.trust+add); soft=true;
      say('You','"Tell me more about that."');
      if(nxt){s.known.push(nxt); say('','You learn that '+first(f.who)+' cares about '+R.lenses[nxt].name.toLowerCase()+': '+R.lenses[nxt].short+'.');}
      else say('','You already know what matters to '+first(f.who)+'. Listening still builds trust.');
    } else if(a==='arg'){
      var g=CA().args[arg], pw=argPower(g);
      C.used[g[0]]=(C.used[g[0]]||0)+1; s.doubt-=pw.v;
      say('You','"'+g[2]+'"');
      if(f.cares.indexOf(g[0])>=0){S.hits[g[0]]=(S.hits[g[0]]||0)+1; if(s.known.indexOf(g[0])<0){s.known.push(g[0]); say('','That landed. Now you know '+first(f.who)+' cares about '+R.lenses[g[0]].name.toLowerCase()+'.');}}
      else if(f.cold===g[0]){s.cold=true; say('','That fell flat. '+R.lenses[g[0]].name+' doesn\'t move '+first(f.who)+'.');}
      say('','Doubt −'+pw.v+'.');
      if(g[0]===o[0]){C.ans=true; C.hp=Math.min(maxHp(),C.hp+3); S.answered++; said=said.concat(gainXp(5)); say('','You answered the worry they raised. Composure +3.');}
    } else if(a==='cg'){
      var shared=s.known.filter(function(l){return CL().lenses.indexOf(l)>=0}), p=12+18*shared.length;
      if(S.cls==='neighbor') p*=1.5;
      p=Math.round(p*trustMult()*lvlMult()); C.cg=true; s.doubt-=p;
      say('You',shared.length?'"We both care about '+shared.map(function(l){return R.lenses[l].name.toLowerCase()}).join(' and ')+'. Let\'s start there."':'"We both want this town to work. Let\'s start there."');
      if(!shared.length) say('','You haven\'t found a value you both hold yet, so it only goes so far.');
      say('','Doubt −'+p+'.');
    } else if(a==='deal'){
      var d=CA().deals.filter(function(x){return x.id===arg})[0], u=S.cls==='fixer'&&d.unity>0?Math.ceil(d.unity/2):d.unity;
      S.deals.push(d.id); setUnity(-u); S.lib=clamp(S.lib-d.liberty,0,100);
      say('You',d.say);
      said=said.concat(moveGroups(d.move));
      say('','Deal made. Party unity '+(u>0?'−'+u:'+'+(-u))+'. Liberty kept: '+S.lib+'%.'+(d.move[f.id]?' '+first(f.who)+': doubt '+(d.move[f.id]<0?'−'+(-d.move[f.id]):'+'+d.move[f.id])+'.':' It doesn\'t change much for '+first(f.who)+'.'));
    } else if(a==='slogan'){
      var sl=R.slogans[Math.floor(rand()*R.slogans.length)], back=S.cls==='wolf'?6:12;
      s.doubt+=back; if(S.cls!=='wolf') s.trust=Math.max(0,s.trust-1); setUnity(3);
      say('You','"'+sl+'"'); say('','Rex would be proud. Doubt +'+back+(S.cls==='wolf'?'.':', trust −1.')+' Party unity +3.');
      said=said.concat(settle(f.id));
    } else if(a==='ask'){
      var od=askOdds(), roll=1+Math.floor(rand()*20);
      say('You','"Can I count on you?"');
      if(roll>=od.n){say('','You rolled '+roll+'. You needed '+od.n+'. They say yes.'); s.doubt=Math.min(s.doubt,0);}
      else{say('','You rolled '+roll+'. You needed '+od.n+'. "Not yet." Doubt +10, and they lose a little patience.'); s.doubt+=10; C.pat--;}
    } else if(a==='leave'){
      return endTalk('You thank '+first(f.who)+' and head out. Doubt stands at '+Math.max(0,s.doubt)+'.');
    }
    said=said.concat(settle(f.id));
    said.forEach(function(t){say('',t);});
    if(s.state==='ally'){
      say(f.who,f.joined);
      return endTalk(f.org+' joined your coalition. +30 XP.');
    }
    // their turn
    C.pat--;
    if(!C.ans){var dmg=6+Math.floor(rand()*4)-(S.cls==='monitor'?2:0); if(soft) dmg=Math.ceil(dmg/2); C.hp=Math.max(0,C.hp-dmg); say('','That worry went unanswered. Composure −'+dmg+'.');}
    if(C.hp<=0) return endTalk('You\'re rattled and lose the thread. You leave to regroup. Doubt stands at '+Math.max(0,s.doubt)+'.');
    if(C.pat<=0) return endTalk(first(f.who)+' has to get back to work. Doubt stands at '+Math.max(0,s.doubt)+'.');
    C.oi++; C.ans=false;
    save(); drawTalk();
    live(C.lines.slice(-3).map(function(l){return (l.who?l.who+': ':'')+l.t}).join(' '));
  }
  function endTalk(t){C.over=t; save(); drawTalk(); live(t);}

  /* ---------- the vote ---------- */
  function finish(){
    var v=votes(), y=v.filter(function(x){return x.yes}).length, pass=y>=3, al=allies(), side={};
    al.forEach(function(f){side[f.side]=1;});
    var rank=pass?(side.left&&side.right&&S.unity>=50?'herder':'builder'):(y===2?'close':(S.unity>=50&&al.length>=3?'gadfly':'lone'));
    S.done={y:y,pass:pass,rank:rank}; save();
    var rk=R.ranks.filter(function(r){return r.id===rank})[0], fame=json(FAME)||[];
    fame.unshift({rank:rk.name,camp:CA().name,vote:(pass?'passed ':'failed ')+y+' to '+(5-y),cls:CL().name,date:new Date().toISOString().slice(0,10)});
    put(FAME,JSON.stringify(fame.slice(0,10)));
    showEnd();
  }
  function showEnd(){
    var d=S.done, v=votes(), rk=R.ranks.filter(function(r){return r.id===d.rank})[0], al=allies(), left=al.filter(function(f){return f.side==='left'}), right=al.filter(function(f){return f.side==='right'});
    var over=Object.keys(R.lenses).map(function(l){
      var L=left.filter(function(f){return f.cares.indexOf(l)>=0}), Rr=right.filter(function(f){return f.cares.indexOf(l)>=0});
      return (L.length&&Rr.length)?{l:l,who:L.concat(Rr)}:null;}).filter(Boolean);
    var hits=Object.keys(S.hits).sort(function(a,b){return S.hits[b]-S.hits[a]});
    var names=function(arr){return arr.length?arr.map(function(f){return esc(f.who)+' ('+esc(f.org)+')'}).join(', '):'nobody'};
    var share=(d.pass?'I passed':'I lost')+' "'+CA().name+'" '+d.y+' to '+(5-d.y)+' in Herding Porcupines as '+CL().name+'. Rank: '+rk.name+'. '+location.origin+location.pathname;
    var h='<h3>'+(d.pass?'It passed, '+d.y+' to '+(5-d.y):'It failed, '+d.y+' to '+(5-d.y))+'</h3>'+
      '<p class="rpg-rank"><b>'+esc(rk.name)+'.</b> '+esc(rk.when)+'</p>'+whipTable(v)+
      '<ul class="facts"><li><b>Your coalition:</b> on the left, '+names(left)+'; on the right, '+names(right)+'.</li>'+
      '<li><b>Liberty kept: '+S.lib+'%.</b> '+(S.deals.length?'You traded for: '+CA().deals.filter(function(x){return S.deals.indexOf(x.id)>=0}).map(function(x){return esc(x.text.toLowerCase())}).join('; ')+'.':'You made no deals.')+'</li>'+
      '<li><b>Party unity: '+S.unity+'.</b> '+(S.unity>=50?'Your own side stayed with you.':S.unity>=R.lin.unity?'Your own side grumbled, but stayed.':'Your own side spent the campaign fighting you, and the council saw it.')+'</li></ul>'+
      '<h4>Where the aisles overlapped</h4>'+(over.length?'<p>These values showed up on both sides of your coalition. That\'s the ground a coalition stands on.</p><ul class="rpg-fx">'+over.map(function(o){return '<li>'+lens(o.l)+': '+o.who.map(function(f){return esc(f.who)}).join(', ')+'</li>'}).join('')+'</ul>':'<p>Your allies all came from one side of the aisle, so nothing tied them together but you. Next time, find the value a group on the other side shares with yours.</p>')+
      (hits.length?'<h4>What worked</h4><p>Arguments that landed on what people care about: '+hits.slice(0,4).map(function(l){return lens(l)+' ×'+S.hits[l]}).join(', ')+'. You answered '+S.answered+' worr'+(S.answered===1?'y':'ies')+' head on.</p>':'')+
      '<label for="rpg-share" class="sm">Share your result</label><textarea id="rpg-share" class="rpg-share" rows="3" readonly>'+esc(share)+'</textarea>'+
      '<div class="row"><button class="btn" type="button" data-a="copy">Copy</button><span class="sm" id="rpg-copied" aria-live="polite"></span><button class="btn gold" type="button" data-a="again">Play again</button></div>'+
      '<p>Doing this for real? Read <a href="../organize/index.html">how to organize</a>, and before your first convention, <a href="../convention/index.html">the convention guide</a>.</p>';
    screen(h,'end');
  }

  /* ---------- clicks and keys ---------- */
  root.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('button'); if(!b||!root.contains(b)) return;
    var a=b.getAttribute('data-a');
    if(b.hasAttribute('data-go')){var g=b.getAttribute('data-go').split(','); step(+g[0],+g[1]); return;}
    if(b.hasAttribute('data-place')){travel(b.getAttribute('data-place')); return;}
    if(a==='new'){
      if(load()&&!load().done&&!b.hasAttribute('data-sure')){root.querySelector('#rpg-confirm').innerHTML='<div class="warn"><p>Start over? Your game in progress will be gone.</p><div class="row"><button class="btn gold" type="button" data-a="new" data-sure="1">Yes, start over</button></div></div>'; root.querySelector('#rpg-confirm button').focus(); return;}
      showMake();
    }
    else if(a==='continue'){S=load(); if(S.done) showEnd(); else showWorld('Welcome back. '+S.day+' days left.');}
    else if(a==='title'||a==='quit') showTitle();
    else if(a==='world') showWorld();
    else if(a==='talk') talk(b.getAttribute('data-f'));
    else if(a==='sub'){C.sub=b.getAttribute('data-s')||null; drawTalk(); var t=panel.querySelector('.rpg-cards button,.rpg-acts button:not([disabled])'); if(t) t.focus();}
    else if(a==='do') doAct(b.getAttribute('data-s'));
    else if(a==='arg') doAct('arg',+b.getAttribute('data-i'));
    else if(a==='deal') doAct('deal',b.getAttribute('data-d'));
    else if(a==='done'){C=null; afterDay();}
    else if(a==='chat'){var id=b.getAttribute('data-c'), c=R.caucus.filter(function(x){return x.id===id})[0], n=S.talk[id]=(S.talk[id]||0)+1; save();
      var p=panel.querySelector('#rpg-say-'+id); p.textContent=c.talk[(n-1)%c.talk.length]; live(c.who+': '+p.textContent);}
    else if(a==='meeting'){S.day--; S.meetings++; save(); showMeeting();}
    else if(a==='meet'){var o=R.meeting.opts[+b.getAttribute('data-i')]; setUnity(o.unity); var said=moveGroups(o.move); save();
      screen('<h3>'+esc(R.meeting.title)+'</h3><p><b>You took up:</b> '+esc(o.label)+'.</p><p>'+esc(o.then)+'</p>'+effects(o.move,o.unity,said)+'<div class="row"><button class="btn gold" type="button" data-a="aftermeet">Back to town</button></div>','event');}
    else if(a==='aftermeet') afterDay();
    else if(a==='ev'){var e=R.events.filter(function(x){return x.id===b.getAttribute('data-e')})[0]; eventScreen(e,+b.getAttribute('data-i'));}
    else if(a==='county') showCounty();
    else if(a==='askvote') showCounty(true);
    else if(a==='vote') finish();
    else if(a==='again'){put(KEY,null); S=null; showMake();}
    else if(a==='copy'){var t=panel.querySelector('#rpg-share'), done=function(){panel.querySelector('#rpg-copied').textContent='Copied.';};
      if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(t.value).then(done,function(){t.select();});
      else{t.focus(); t.select(); try{if(document.execCommand('copy')) done();}catch(e){}}}
  });
  cv.addEventListener('keydown',function(ev){
    var k=ev.key, m={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0],w:[0,-1],s:[0,1],a:[-1,0],d:[1,0],W:[0,-1],S:[0,1],A:[-1,0],D:[1,0]}[k];
    if(m){ev.preventDefault(); steps=null; step(m[0],m[1]);}
  });
  cv.addEventListener('click',function(ev){
    if(!S) return; var r=cv.getBoundingClientRect(); if(!r.width) return;
    var x=Math.floor((ev.clientX-r.left)/r.width*W), y=Math.floor((ev.clientY-r.top)/r.height*H), ch=tile(x,y).toUpperCase();
    if(R.places[ch]&&!doorAt(x,y)){var d=DOOR[R.places[ch].id]; x=d[0]; y=d[1];}
    walkTo([x,y]);
  });

  /* ---------- pixel art ---------- */
  function px(c,x,y,w,h,col){c.fillStyle=col; c.fillRect(x,y,w,h);}
  function drawTile(x,y){
    var ch=tile(x,y), X=x*TS, Y=y*TS, up=ch.toUpperCase(), p=R.places[up];
    var grass=function(){px(ctx,X,Y,TS,TS,'#5aa845'); px(ctx,X+((x*7+y*3)%24)+2,Y+((x*5+y*11)%24)+3,2,2,'#78c25e'); px(ctx,X+((x*13+y*5)%26)+2,Y+((x*3+y*7)%26)+2,2,2,'#4b9339');};
    if(ch==='.') grass();
    else if(ch===':'){px(ctx,X,Y,TS,TS,'#cfc6ad'); px(ctx,X,Y,TS,1,'#b3a98d'); px(ctx,X,Y,1,TS,'#b3a98d');}
    else if(ch==='='){px(ctx,X,Y,TS,TS,'#4a4a52'); if(x%2===0) px(ctx,X+6,Y+15,20,3,'#f5c400');}
    else if(ch==='T'){grass(); px(ctx,X+13,Y+20,6,10,'#6b4226'); px(ctx,X+4,Y+3,24,20,'#1f6b2c'); px(ctx,X+8,Y+1,16,4,'#1f6b2c'); px(ctx,X+8,Y+6,6,5,'#2f8a3e');}
    else if(ch==='~'){px(ctx,X,Y,TS,TS,'#3d7fc4'); px(ctx,X+4+(x%3)*4,Y+8,10,2,'#8ec0ee'); px(ctx,X+14,Y+20,10,2,'#8ec0ee');}
    else if(ch===','){px(ctx,X,Y,TS,TS,'#c9a640'); for(var i=0;i<4;i++) px(ctx,X,Y+4+i*8,TS,2,'#a8862c');}
    else if(p){
      var b=BOX[up], roof=y===b.y0;
      px(ctx,X,Y,TS,TS,roof?p.roof:p.wall);
      if(roof){px(ctx,X,Y+TS-4,TS,4,'rgba(0,0,0,.25)');}
      if(ch!==up){var top=y===b.y0; px(ctx,X+8,top?Y+2:Y+6,16,top?28:26,'#5a3a1a'); px(ctx,X+20,Y+16,2,2,'#f5c400');}
      else if(!roof){px(ctx,X+8,Y+8,16,12,'#bfe3f5'); px(ctx,X+8,Y+13,16,2,p.wall); px(ctx,X+15,Y+8,2,12,p.wall);}
      if(x===b.x0) px(ctx,X,Y,2,TS,'#1a1a1a');
      if(x===b.x1) px(ctx,X+TS-2,Y,2,TS,'#1a1a1a');
      if(y===b.y0) px(ctx,X,Y,TS,2,'#1a1a1a');
      if(y===b.y1) px(ctx,X,Y+TS-2,TS,2,'#1a1a1a');
    } else grass();
  }
  function drawPlayer(){
    var X=S.pos[0]*TS, Y=S.pos[1]*TS, l=frame?2:0;
    px(ctx,X+9,Y+29,14,3,'rgba(0,0,0,.3)');
    px(ctx,X+11,Y+22,4,8-l,'#1f2a44'); px(ctx,X+17,Y+22,4,6+l,'#1f2a44');
    px(ctx,X+9,Y+12,14,11,'#f5c400'); px(ctx,X+9,Y+12,14,2,'#1a1a1a');
    px(ctx,X+7,Y+13,2,8,'#e0ac69'); px(ctx,X+23,Y+13,2,8,'#e0ac69');
    px(ctx,X+10,Y+2,12,11,'#e0ac69'); px(ctx,X+10,Y+1,12,4,'#3b2a1a');
    if(facing!=='up'){px(ctx,X+(facing==='left'?11:facing==='right'?15:12),Y+7,2,2,'#1a1a1a'); px(ctx,X+(facing==='left'?15:facing==='right'?19:18),Y+7,2,2,'#1a1a1a');}
    else px(ctx,X+10,Y+1,12,9,'#3b2a1a');
  }
  function badge(x,y,col,txt){
    ctx.fillStyle='#1a1a1a'; ctx.beginPath(); ctx.arc(x,y,10,0,7); ctx.fill();
    ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,8,0,7); ctx.fill();
    ctx.fillStyle=col==='#f5c400'||col==='#d9d3bf'?'#1a1a1a':'#fff'; ctx.font='bold '+(txt.length>1?9:12)+'px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(txt,x,y+1);
  }
  function drawMap(){
    if(!ctx||!S) return;
    ctx.imageSmoothingEnabled=false;
    for(var y=0;y<H;y++) for(var x=0;x<W;x++) drawTile(x,y);
    Object.keys(BOX).forEach(function(k){var b=BOX[k], p=R.places[k], dr=DOOR[p.id], cx=(b.x0+b.x1+1)/2*TS, cy=(dr[1]===b.y0?b.y0+1:b.y0)*TS+15, w;
      ctx.font='bold 11px monospace'; ctx.textAlign='center'; ctx.textBaseline='middle';
      w=ctx.measureText(p.sign).width+10; px(ctx,cx-w/2,cy-8,w,16,'#fffdf5'); ctx.strokeStyle='#1a1a1a'; ctx.lineWidth=1; ctx.strokeRect(cx-w/2+.5,cy-7.5,w-1,15);
      ctx.fillStyle='#1a1a1a'; ctx.fillText(p.sign,cx,cy+1);
      var d=DOOR[p.id], f=BYPLACE[p.id], bx=d[0]*TS+TS-4, by=d[1]*TS+4;
      if(f){var st=S.fac[f.id].state; badge(bx,by,st==='ally'?'#1e6b35':st==='opposed'?'#a4161a':'#d9d3bf',st==='ally'?'✓':st==='opposed'?'×':'?');}
      else if(p.id==='hq') badge(bx,by,'#f5c400','HQ');
      else badge(bx,by,'#1f2a44',String(yesCount()));
    });
    drawPlayer();
  }
  /* Portraits: a 16 by 16 pixel face, drawn from a short description in the game data. */
  function portrait(cn,f){
    var c=cn.getContext&&cn.getContext('2d'); if(!c) return;
    var P=function(x,y,w,h,col){c.fillStyle=col; c.fillRect(x*4,y*4,w*4,h*4);};
    P(0,0,16,16,'#efe6cc');
    if(f.style==='long') P(3,2,10,10,f.hair);
    P(2,11,12,5,f.shirt); P(7,10,2,2,f.skin);
    P(4,3,8,8,f.skin);
    if(f.style==='short'||f.style==='long'||f.style==='beard') P(4,2,8,2,f.hair);
    if(f.style==='short') {P(4,4,1,2,f.hair); P(11,4,1,2,f.hair);}
    if(f.style==='bun'){P(4,2,8,2,f.hair); P(6,0,4,2,f.hair);}
    if(f.style==='fade') P(4,2,8,1,f.hair);
    if(f.style==='bald'){P(4,5,1,2,f.hair); P(11,5,1,2,f.hair);}
    if(f.style==='beard') P(4,8,8,3,f.hair);
    P(6,6,1,1,'#1a1a1a'); P(9,6,1,1,'#1a1a1a'); P(7,9,2,1,f.style==='beard'?'#7a3b2e':'#8a4a3a');
    if(f.extra==='glasses'){c.strokeStyle='#1a1a1a'; c.lineWidth=2; c.strokeRect(21,21,10,10); c.strokeRect(33,21,10,10); P(7,6,2,0.5,'#1a1a1a');}
    if(f.extra==='collar') P(7,11,2,1,'#ffffff');
    if(f.extra==='cap'){P(4,1,8,2,'#4b5320'); P(3,3,10,1,'#3a4119');}
    if(f.extra==='hat'){P(5,0,6,2,'#d9b56b'); P(2,2,12,1,'#c9a04f');}
    if(f.extra==='badge') P(10,12,2,2,'#f5c400');
    if(f.extra==='headset'){P(3,4,1,4,'#333'); P(12,4,1,4,'#333'); P(4,2,8,1,'#333'); P(4,8,3,1,'#333');}
  }

  showTitle();
})();
