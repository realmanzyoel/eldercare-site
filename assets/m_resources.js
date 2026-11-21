/* resources hub: filter guides by title/summary, hide empty sections */
(function(){var i=document.querySelector('[data-rfilter]');if(!i)return;i.addEventListener('input',function(){var q=i.value.toLowerCase().trim(),n=0;
 document.querySelectorAll('.rsec').forEach(function(s){var k=0;s.querySelectorAll('.rcard').forEach(function(c){var m=!q||c.textContent.toLowerCase().indexOf(q)>-1;c.hidden=!m;if(m)k++});s.hidden=k===0;n+=k});
 document.querySelector('.rnone').hidden=n>0})})();
