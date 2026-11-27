/* Puts your gold star on the home chart if you've taken the quiz in this browser. Nothing is sent anywhere. */
(function(){
  var L=window.LEScore; if(!L) return;
  var code=null; try{code=localStorage.getItem('le_mine')}catch(e){}
  var a=L.parse(code); if(!a) return;
  var me=L.score(a), svg=document.querySelector('#homechart svg'); if(!svg) return;
  var ns='http://www.w3.org/2000/svg', x=L.dx(me.E,me.P), y=L.dy(me.E,me.P);
  function add(tag,attrs,text){var el=document.createElementNS(ns,tag);for(var k in attrs) el.setAttribute(k,attrs[k]); if(text) el.textContent=text; svg.appendChild(el); return el;}
  add('polygon',{points:L.star(x,y,17,8),fill:'#f5c400',stroke:'#1a1a1a','stroke-width':2.5});
  var right=x>L.CX, at={x:right?x-22:x+22,y:y-12,'text-anchor':right?'end':'start','font-size':20,'font-weight':800};
  var h=add('text',at,'You'); h.setAttribute('fill','#fffdf5'); h.setAttribute('stroke','#fffdf5'); h.setAttribute('stroke-width',6); h.setAttribute('aria-hidden','true');
  add('text',at,'You').setAttribute('fill','#1a1a1a');
  var d=svg.querySelector('desc'); if(d) d.textContent+=' A gold star marks you: economic freedom '+me.E+', personal freedom '+me.P+'.';
  var cap=document.getElementById('homecap'); if(cap) cap.innerHTML='The gold star is you, from the quiz you took in this browser. <a href="results.html">See your full results</a>.';
})();
