const express = require('express');
const Cerebras = require('@cerebras/cerebras_cloud_sdk');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3001;

// Habilita CORS para todas las solicitudes
app.use(cors());

// Permite recibir JSON
app.use(express.json());

// Instancia del cliente Cerebras
const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'],
});

// Ruta de la API
app.post('/api/chat', async (req, res) => {
  try {
    const { messages } = req.body;

    const completionCreateResponse = await client.chat.completions.create({
      messages,
      model: 'llama-3.1-8b',
    });

    res.json({ reply: completionCreateResponse.choices[0].message.content });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Error al conectar con Cerebras' });
  }
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
