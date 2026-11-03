const qs=[...document.querySelectorAll('.quiz [data-q]')];
qs.forEach(b=>b.addEventListener('click',()=>{b.classList.toggle('sel');
const n=document.querySelectorAll('.quiz .sel').length;
const t=['Elige uno para empezar esta semana: con un solo hábito ya sumas.','¡Buen comienzo! Ya tienes 1 de 5. Elige el siguiente.','Vas bien: 2 de 5.','¡3 de 5! Estás construyendo una buena base.','¡4 de 5! Te falta muy poco.','¡5 de 5! En el estudio HUNT, quienes tenían los cinco factores favorables tuvieron una probabilidad bastante mayor de envejecer exitosamente.'];
document.getElementById('res').textContent=t[n];}));
