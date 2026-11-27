(function(){
  var subj={"ai-crm-waitlist":"AI CRM waitlist","rewind-waitlist":"Rewind waitlist","contact":"Talk to Webdefy"};
  document.querySelectorAll('form[data-mailto]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var hp=f.querySelector('[name="company"]'); if(hp&&hp.value) return;
      var lines=[];
      f.querySelectorAll('input,textarea,select').forEach(function(el){
        if(!el.name||el.type==='hidden'||el.name==='company') return;
        if((el.type==='checkbox'||el.type==='radio')&&!el.checked) return;
        if(el.value) lines.push(el.name.charAt(0).toUpperCase()+el.name.slice(1)+': '+el.value);
      });
      var s=subj[f.getAttribute('name')]||'Webdefy';
      window.location.href='mailto:hello@webdefy.com?subject='+encodeURIComponent(s)+'&body='+encodeURIComponent(lines.join('\n'));
      setTimeout(function(){window.location.href=f.getAttribute('action');},800);
    });
  });
})();
