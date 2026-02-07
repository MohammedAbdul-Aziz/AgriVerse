document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const imageInputLabel = document.getElementById('image-input-label');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeButton = document.getElementById('analyze-button');
    
    const resultSection = document.getElementById('result-section');
    const uploadedImage = document.getElementById('uploaded-image');
    const predictionOutput = document.getElementById('prediction-output');
    const nutrientStatusOutput = document.getElementById('nutrient-status-output');

    // Handle file input changes
    imageInput.addEventListener('change', () => {
        if (imageInput.files.length > 0) {
            fileNameDisplay.textContent = imageInput.files[0].name;
        }
    });

    // Handle drag and drop
    imageInputLabel.addEventListener('dragover', (event) => {
        event.preventDefault();
        imageInputLabel.classList.add('dragover');
    });

    imageInputLabel.addEventListener('dragleave', () => {
        imageInputLabel.classList.remove('dragover');
    });

    imageInputLabel.addEventListener('drop', (event) => {
        event.preventDefault();
        imageInputLabel.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            fileNameDisplay.textContent = files[0].name;
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const imageFile = imageInput.files[0];
        if (!imageFile) {
            alert('Please select an image file first.');
            return;
        }

        // Show spinner and disable button
        const spinnerHTML = '<div class="spinner-container"><div class="spinner"></div><p>Analyzing...</p></div>';
        predictionOutput.innerHTML = spinnerHTML;
        nutrientStatusOutput.innerHTML = spinnerHTML;
        resultSection.classList.remove('hidden');
        analyzeButton.disabled = true;
        analyzeButton.textContent = 'ANALYZING...';

        // Display the uploaded image
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedImage.src = e.target.result;
        }
        reader.readAsDataURL(imageFile);

        // Prepare form data
        const formData = new FormData();
        formData.append('file', imageFile);

        try {
            // Make the API call
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Display disease prediction
            let predictionHTML = '<ul>';
            for (const [key, value] of Object.entries(data.prediction)) {
                predictionHTML += `
                    <li class="prediction-item">
                        <span>${key.replace(/_/g, ' ')}</span>
                        <strong>${(value * 100).toFixed(2)}%</strong>
                    </li>
                `;
            }
            predictionHTML += '</ul>';
            predictionOutput.innerHTML = predictionHTML;

            // Display nutrient status
            if (data.nutrient_status) {
                nutrientStatusOutput.innerHTML = `<strong>${data.nutrient_status}</strong>`;
            } else {
                nutrientStatusOutput.innerHTML = `<p>Not available</p>`;
            }

        } catch (error) {
            predictionOutput.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            nutrientStatusOutput.innerHTML = '';
            console.error('There was a problem with the fetch operation:', error);
        } finally {
            // Re-enable button
            analyzeButton.disabled = false;
            analyzeButton.textContent = 'Analyze';
        }
    });
});
