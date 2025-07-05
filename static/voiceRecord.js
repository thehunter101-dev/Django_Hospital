if (annyang) {
  // Configura el idioma al español de España o Latinoamérica
  annyang.setLanguage('es-ES'); // Puedes usar 'es-EC', 'es-MX', etc. si prefieres

  let finalTranscript = '';
  const textarea = document.getElementById("id_observaciones");

  // Escucha las frases reconocidas
  annyang.addCallback('result', function (phrases) {
    if (!phrases || phrases.length === 0) return;

    // Evita frases repetidas si ya fueron agregadas
    const latest = phrases[0].trim();
    if (!finalTranscript.endsWith(latest)) {
      finalTranscript += latest + '. ';
      textarea.value = finalTranscript;
    }
  });

  // Botón para iniciar
  document.getElementById("start").onclick = () => {
    finalTranscript = textarea.value.trim(); // conservar lo anterior
    annyang.start({ autoRestart: true, continuous: true });
  };

  // Botón para detener
  document.getElementById("stop").onclick = () => {
    annyang.abort();
  };

  // Manejo de errores opcional
  annyang.addCallback('error', function (err) {
    console.error('Error de reconocimiento de voz:', err.error);
  });
} else {
  alert("Tu navegador no soporta reconocimiento de voz con annyang.");
}
