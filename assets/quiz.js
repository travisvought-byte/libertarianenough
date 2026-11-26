/* Libertarian Enough quiz. Answers stay in this browser. Nothing is sent anywhere. */
(function(){
  var D=window.LE, Q=D.questions, N=Q.length, A=D.answers;
  var root=document.getElementById('quiz'); if(!root) return;
  var ans=[]; var i=0;
  try{var saved=JSON.parse(localStorage.getItem('le_progress')||'null'); if(saved&&saved.v===D.version&&saved.a&&saved.a.length===N){ans=saved.a;}}catch(e){}
  for(var k=0;k<N;k++){ if(ans[k]===undefined) ans[k]=null; }
  var intro=document.getElementById('quiz-intro');
  var stage=document.getElementById('quiz-stage');
  var bar=document.getElementById('quiz-bar');
  var status=document.getElementById('quiz-status');
  function save(){try{localStorage.setItem('le_progress',JSON.stringify({v:D.version,a:ans}))}catch(e){}}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function render(focus){
    var q=Q[i];
    var h='<form id="qform" novalidate><fieldset class="q"><legend><span class="qnum">Statement '+(i+1)+' of '+N+'</span>'+esc(q.t)+'</legend>';
    if(q.aside) h+='<p class="aside">'+esc(q.aside)+'</p>';
    h+='<div class="opts">';
    for(var j=0;j<5;j++){
      var id='q'+i+'o'+j;
      h+='<label class="opt" for="'+id+'"><input type="radio" name="a" id="'+id+'" value="'+j+'"'+(ans[i]===j?' checked':'')+'> '+esc(A[j])+'</label>';
    }
    h+='</div><p class="qerr" id="qerr" aria-live="polite"></p></fieldset>';
    h+='<div class="row">';
    if(i>0) h+='<button type="button" class="btn ghost" id="qback">Back</button>';
    h+='<button type="submit" class="btn gold" id="qnext">'+(i===N-1?'See my results':'Next')+'</button></div></form>';
    stage.innerHTML=h;
    var done=ans.filter(function(x){return x!==null}).length;
    bar.style.width=Math.round(100*i/N)+'%';
    status.textContent='Statement '+(i+1)+' of '+N+'.';
    var form=document.getElementById('qform');
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var sel=form.querySelector('input[name=a]:checked');
      if(!sel){var e=document.getElementById('qerr'); e.textContent='Pick an answer first. "Not sure" counts.'; form.querySelector('input').focus(); return;}
      ans[i]=parseInt(sel.value,10); save();
      if(i<N-1){i++; render(true);} else finish();
    });
    var back=document.getElementById('qback');
    if(back) back.addEventListener('click',function(){var sel=form.querySelector('input[name=a]:checked'); if(sel){ans[i]=parseInt(sel.value,10); save();} i--; render(true);});
    if(focus){ var lg=stage.querySelector('legend'); lg.setAttribute('tabindex','-1'); lg.focus(); }
  }
  function finish(){
    var code=D.version+'.'+ans.join('');
    try{localStorage.setItem('le_mine',code); localStorage.removeItem('le_progress');}catch(e){}
    location.href='results.html#a='+code;
  }
  document.getElementById('quiz-start').addEventListener('click',function(){
    intro.hidden=true; stage.hidden=false; document.getElementById('quiz-prog').hidden=false;
    var first=ans.indexOf(null); i=first<0?0:first; render(true);
  });
  if(ans.some(function(x){return x!==null})){
    var b=document.getElementById('quiz-start'); b.textContent='Pick up where you left off';
    var r=document.getElementById('quiz-restart'); r.hidden=false;
    r.addEventListener('click',function(){ans=ans.map(function(){return null}); save(); b.textContent='Start the quiz'; r.hidden=true;});
  }
})();
