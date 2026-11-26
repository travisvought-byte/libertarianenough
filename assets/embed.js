/* Libertarian Enough embeds: sizes our iframes (marked data-le-embed) to fit what's inside. Sends nothing anywhere. */
(function(){
  window.addEventListener('message',function(ev){
    if(ev.origin!=='https://libertarianenough.org') return;
    var d=ev.data; if(!d||d.le!=='height'||typeof d.h!=='number') return;
    var f=document.querySelectorAll('iframe[data-le-embed]');
    for(var i=0;i<f.length;i++){ if(f[i].contentWindow===ev.source){ f[i].style.height=Math.min(Math.max(Math.ceil(d.h),240),4000)+'px'; } }
  });
})();
