let messages = [
    {
        role: "system",
        content: `
        eres una guia para gestion de hospital te encargaras de solo responder a como acceder a los modulos: 
core/doctores/ — Listar doctores

core/especialidades/ — Listar especialidades

core/empleados/ — Listar empleados

core/diagnosticos/ — Listar diagnósticos

core/gastos/ — Listar gastos mensuales

core/pacientes/ — Listar pacientes

core/tipos_sangre — Listar tipos de sangre

core/medicamentos — Listar medicamentos

core/tipos_medicamento — Listar tipos de medicamentos

core/marca/ — Listar marcas de medicamentos

core/cargos/ — Listar cargos

core/tipos_gasto/ — Listar tipos de gasto

responde resumidamente en menos de 100 palabras 

        `
    }
];

function appendMessage(sender, message) {
  const msgDiv = document.createElement('div');
  msgDiv.className = sender === 'user' ? 'msg-user' : 'msg-bot';
  msgDiv.innerHTML = `<span class="msg-bubble">${message}</span>`;

  const chatContainer = document.getElementById('chat-messages');
  if (!chatContainer) {
    console.error("No se encontró el contenedor de mensajes con id 'chat-messages'");
    return;
  }

  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}


async function sendToCerebras(userMsg) {
  appendMessage('user', userMsg);
  messages.push({ role: 'user', content: userMsg }); // mantiene el historial

  try {
    const res = await fetch('http://localhost:3001/api/chat', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages })
    });
    const data = await res.json();
    appendMessage('bot', data.reply);
    messages.push({ role: 'assistant', content: data.reply }); // añade respuesta al historial
  } catch (e) {
    appendMessage('bot', "⚠️ Error al conectar con Cerebras.");
  }
}

document.getElementById('chat-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const input = document.getElementById('user-input');
  const msg = input.value.trim();
  if (!msg) return;
  sendToCerebras(msg);
  input.value = '';
});


