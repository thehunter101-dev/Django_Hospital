if (annyang) {
  let finalTranscript = '';
  const textarea = document.getElementById("id_observaciones");

  annyang.addCallback('result', function (phrases) {
    finalTranscript += phrases[0] + ' ';
    textarea.value = finalTranscript;
  });

  document.getElementById("start").onclick = () => annyang.start({ continuous: true });
  document.getElementById("stop").onclick = () => annyang.abort();
}
