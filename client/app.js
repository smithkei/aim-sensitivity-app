const API_BASE_URL = window.API_BASE_URL || 'http://127.0.0.1:5000';
const API_TOKEN = window.API_TOKEN || 'secret123';

const statusText = document.getElementById('statusText');
const buttons = Array.from(document.querySelectorAll('button[data-command]'));

async function sendCommand(command) {
  statusText.textContent = `Sending ${command}...`;

  try {
    const response = await fetch(`${API_BASE_URL}/send-command`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        command,
        token: API_TOKEN,
      }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || 'Request failed');
    }

    statusText.textContent = `Queued: ${payload.command}`;
  } catch (error) {
    statusText.textContent = error.message;
  }
}

buttons.forEach((button) => {
  button.addEventListener('click', async () => {
    buttons.forEach((candidate) => {
      candidate.disabled = true;
    });

    await sendCommand(button.dataset.command);

    buttons.forEach((candidate) => {
      candidate.disabled = false;
    });
  });
});
