const btn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');

function getInputValue(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : "";
}

btn.addEventListener('click', async () => {
  resultDiv.style.display = 'none';
  errorDiv.style.display = 'none';
  resultDiv.textContent = '';
  errorDiv.textContent = '';

  const payload = {
    N: getInputValue('N'),
    P: getInputValue('P'),
    K: getInputValue('K'),
    temperature: getInputValue('temperature'),
    humidity: getInputValue('humidity'),
    ph: getInputValue('ph'),
    rainfall: getInputValue('rainfall')
  };

  // basic validation
  const missing = Object.keys(payload).filter(k => payload[k] === '');
  if (missing.length) {
    errorDiv.style.display = 'block';
    errorDiv.textContent = 'Please fill: ' + missing.join(', ');
    return;
  }

  // Send request
  btn.disabled = true;
  btn.textContent = 'Predicting...';

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok || data.success === false) {
      errorDiv.style.display = 'block';
      errorDiv.textContent = data.error || 'Prediction failed';
    } else {
      resultDiv.style.display = 'block';
      resultDiv.textContent = 'Recommended crop: ' + data.prediction;
    }
  } catch (err) {
    errorDiv.style.display = 'block';
    errorDiv.textContent = 'Error: ' + err.message;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Get Recommendation';
  }
});

clearBtn.addEventListener('click', () => {
  ['N','P','K','temperature','humidity','ph','rainfall'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  resultDiv.style.display = 'none';
  errorDiv.style.display = 'none';
});
