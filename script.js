
document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const imageInput = document.getElementById('image-input');
    const imageFile = imageInput.files[0];
    const resultSection = document.getElementById('result-section');
    const uploadedImage = document.getElementById('uploaded-image');
    const predictionOutput = document.getElementById('prediction-output');

    if (!imageFile) {
        alert('Please select an image file.');
        return;
    }

    // Display the uploaded image
    const reader = new FileReader();
    reader.onload = function(e) {
        uploadedImage.src = e.target.result;
    }
    reader.readAsDataURL(imageFile);

    // Prepare the form data to send to the backend
    const formData = new FormData();
    formData.append('file', imageFile);

    // Show the result section
    resultSection.classList.remove('hidden');
    predictionOutput.innerHTML = '<p>Analyzing...</p>';

    try {
        // Make the API call to the backend
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display the prediction
        let predictionHTML = '<ul>';
        for (const [key, value] of Object.entries(data.prediction)) {
            predictionHTML += `
                <li class="prediction-item">
                    <span>${key.replace('_', ' ')}</span>
                    <strong>${(value * 100).toFixed(2)}%</strong>
                </li>
            `;
        }
        predictionHTML += '</ul>';
        predictionOutput.innerHTML = predictionHTML;

    } catch (error) {
        predictionOutput.innerHTML = `<p>Error: ${error.message}</p>`;
        console.error('There was a problem with the fetch operation:', error);
    }
});
