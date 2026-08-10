document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendation-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.getElementById('loader');
    
    const formSection = document.getElementById('form-section');
    const resultCard = document.getElementById('result-card');
    const errorCard = document.getElementById('error-card');
    
    const sizeDisplay = document.getElementById('size-display');
    const confidenceScore = document.getElementById('confidence-score');
    const confidenceBadge = document.getElementById('confidence-badge');
    const reasoningText = document.getElementById('reasoning-text');
    const errorText = document.getElementById('error-text');
    const resetBtns = document.querySelectorAll('.reset-btn');

    // Tab Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    let activeMode = 'reference-mode';

    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Set active to clicked
            btn.classList.add('active');
            activeMode = btn.dataset.tab;
            document.getElementById(activeMode).classList.add('active');
            
            // Toggle required attributes based on mode
            if (activeMode === 'reference-mode') {
                document.getElementById('source_brand').required = true;
                document.getElementById('source_size').required = true;
            } else {
                document.getElementById('source_brand').required = false;
                document.getElementById('source_size').required = false;
            }
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;

        let API_URL = 'http://127.0.0.1:8000/recommend-size';
        let requestData = {};

        if (activeMode === 'reference-mode') {
            API_URL = 'http://127.0.0.1:8000/recommend-size';
            requestData = {
                category: document.getElementById('category').value,
                source_brand: document.getElementById('source_brand').value,
                source_size: document.getElementById('source_size').value.toUpperCase(),
                target_brand: document.getElementById('target_brand').value
            };
        } else {
            API_URL = 'http://127.0.0.1:8000/recommend-measurements';
            const chestVal = document.getElementById('chest').value;
            const waistVal = document.getElementById('waist').value;
            
            requestData = {
                category: document.getElementById('category').value,
                target_brand: document.getElementById('target_brand').value,
                chest: chestVal ? parseInt(chestVal) : null,
                waist: waistVal ? parseInt(waistVal) : null
            };
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();
            formSection.classList.add('hidden');
            
            if (response.ok) {
                sizeDisplay.textContent = data.recommended_size;
                confidenceScore.textContent = data.confidence;
                reasoningText.textContent = data.reason;
                
                if(data.confidence >= 90) {
                    confidenceBadge.style.color = '#10b981';
                    confidenceBadge.style.background = 'rgba(16, 185, 129, 0.1)';
                    confidenceBadge.style.borderColor = 'rgba(16, 185, 129, 0.2)';
                } else if(data.confidence >= 80) {
                    confidenceBadge.style.color = '#f59e0b';
                    confidenceBadge.style.background = 'rgba(245, 158, 11, 0.1)';
                    confidenceBadge.style.borderColor = 'rgba(245, 158, 11, 0.2)';
                } else {
                    confidenceBadge.style.color = '#ef4444';
                    confidenceBadge.style.background = 'rgba(239, 68, 68, 0.1)';
                    confidenceBadge.style.borderColor = 'rgba(239, 68, 68, 0.2)';
                }

                resultCard.classList.remove('hidden');
            } else {
                errorText.textContent = data.detail || "Unable to find a mapping.";
                errorCard.classList.remove('hidden');
            }

        } catch (error) {
            formSection.classList.add('hidden');
            errorText.textContent = "Failed to connect to the backend server.";
            errorCard.classList.remove('hidden');
            console.error('Error:', error);
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    resetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            resultCard.classList.add('hidden');
            errorCard.classList.add('hidden');
            formSection.classList.remove('hidden');
        });
    });
});
