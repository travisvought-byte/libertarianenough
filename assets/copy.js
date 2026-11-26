/* Copy buttons on the Website help page. Without JavaScript the boxes still work: select the text and copy it. */
(function(){
  var bs=document.querySelectorAll('button[data-copy]');
  for(var i=0;i<bs.length;i++) bs[i].hidden=false;
  function said(id){var s=document.getElementById(id+'-s'); if(!s) return; s.textContent='Copied.'; setTimeout(function(){s.textContent='';},4000);}
  function fallback(t,id){t.focus(); t.select(); try{if(document.execCommand('copy')) said(id);}catch(e){}}
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('button[data-copy]'); if(!b) return;
    var id=b.getAttribute('data-copy'), t=document.getElementById(id); if(!t) return;
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t.value).then(function(){said(id);},function(){fallback(t,id);});}
    else fallback(t,id);
  });
})();
