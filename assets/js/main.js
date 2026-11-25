(function(){
  var btn=document.querySelector('.menu-btn'),nav=document.getElementById('site-nav');
  if(btn&&nav){btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)})}
  var y=document.getElementById('yr');if(y)y.textContent=new Date().getFullYear();
  document.querySelectorAll('input[type=date]').forEach(function(d){d.min=new Date().toISOString().split('T')[0]});
  document.querySelectorAll('form[data-appointment]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var g=function(n){var el=f.elements[n];return el?encodeURIComponent(el.value.trim()):''};
      var msg='Appointment request%0AName: '+g('name')+'%0APhone: '+g('phone')+'%0ADepartment: '+g('department')+'%0APreferred date: '+g('date')+'%0AMessage: '+g('message');
      window.open('https://wa.me/'+f.dataset.wa+'?text='+msg,'_blank','noopener');
    });
  });
})();
