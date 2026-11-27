/* Libertarian Enough scoring, shared by the results page and the home chart. Runs only in this browser. */
(function(){
  var D=window.LE; if(!D) return;
  var Q=D.questions, N=Q.length;
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
  /* How hard you leaned in on each area, and which way. conviction 0-100, lean -100 (more state) to 100 (less state). */
  function priorities(a){
    var by={};
    Q.forEach(function(q,i){ if(!q.area) return; var b=by[q.area]||(by[q.area]={c:0,l:0,k:0}); var v=a[i]-2; b.c+=Math.abs(v)/2; b.l+=v*q.lib/2; b.k++; });
    return D.areas.map(function(ar){var b=by[ar.id]||{c:0,l:0,k:1}; return {area:ar,conviction:Math.round(100*b.c/b.k),lean:Math.round(100*b.l/b.k)};})
      .sort(function(x,y){return (y.conviction*Math.abs(y.lean))-(x.conviction*Math.abs(x.lean))});
  }
  function methods(a){
    var ix={}; Q.forEach(function(q,i){ix[q.id]=i;});
    return D.methods.map(function(m){var s=0,k=0; for(var id in m.q){ if(ix[id]===undefined) continue; s+=(a[ix[id]]-2)*m.q[id]/2; k++; } return {m:m,v:k?Math.round(100*s/k):0};})
      .sort(function(x,y){return y.v-x.v});
  }
  /* The Nolan diamond. Must match chart_svg in _build/core.py. */
  var CX=430, CY=296, S=240;
  function dx(E,P){return CX+(E-P)/100*S} function dy(E,P){return CY-(E+P-100)/100*S}
  function star(x,y,r1,r2){r1=r1||14;r2=r2||6.5;var s='';for(var k=0;k<10;k++){var r=k%2?r2:r1,ang=-Math.PI/2+k*Math.PI/5;s+=(x+r*Math.cos(ang)).toFixed(1)+','+(y+r*Math.sin(ang)).toFixed(1)+' ';}return s.trim();}
  window.LEScore={parse:parse,score:score,priorities:priorities,methods:methods,dx:dx,dy:dy,star:star,CX:CX};
})();
