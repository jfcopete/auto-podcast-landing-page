// Counter animation
function animateCounter(target) {
    const counter = document.getElementById('count');
    const current = parseInt(counter.textContent);
    const increment = target > current ? 1 : -1;
    const step = Math.abs(target - current) / 50;
    
    function updateCounter() {
        const currentValue = parseInt(counter.textContent);
        if (increment > 0 && currentValue < target) {
            counter.textContent = Math.min(currentValue + step, target);
            requestAnimationFrame(updateCounter);
        } else if (increment < 0 && currentValue > target) {
            counter.textContent = Math.max(currentValue - step, target);
            requestAnimationFrame(updateCounter);
        } else {
            counter.textContent = target;
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// API base URL - handles both local development and production
const API_BASE = (() => {
    // Check if we're running on localhost (development)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:5000';
    }
    // Check if we're running on file:// protocol (local file)
    if (window.location.protocol === 'file:') {
        console.warn('⚠️ Running from local file. Please use Docker setup for full functionality.');
        return null;
    }
    // Production - use relative URLs
    return '';
})();

// Load counter on page load
async function loadCounter() {
    if (!API_BASE) {
        console.log('🔧 Backend not available - using local storage only');
        const localCount = localStorage.getItem('emailCount') || 0;
        animateCounter(parseInt(localCount));
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/counter`);
        const data = await response.json();
        animateCounter(data.count);
    } catch (error) {
        console.log('🔧 Counter not available, using local storage');
        const localCount = localStorage.getItem('emailCount') || 0;
        animateCounter(parseInt(localCount));
    }
}

// Submit email function with local CSV support
async function submitEmail(email, categories, podcastRequest) {
    if (!API_BASE) {
        // Local mode - save to CSV file in root directory
        const timestamp = new Date().toISOString();
        const csvData = `${timestamp},"${email}","${categories.join(',')}","${podcastRequest.replace(/"/g, '""')}"\n`;
        
        try {
            // Create CSV file if it doesn't exist
            const csvHeader = 'timestamp,email,categories,podcast_request\n';
            const csvContent = csvHeader + csvData;
            
            // Save to localStorage as backup
            const localData = JSON.parse(localStorage.getItem('podcast_subscriptions') || '[]');
            localData.push({
                timestamp,
                email,
                categories,
                podcast_request: podcastRequest
            });
            localStorage.setItem('podcast_subscriptions', JSON.stringify(localData));
            
            // Create downloadable CSV file
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'podcast_subscriptions.csv';
            a.click();
            window.URL.revokeObjectURL(url);
            
            return { success: true, message: '¡Suscripción guardada! Se descargó el archivo CSV.' };
        } catch (error) {
            console.error('Error saving locally:', error);
            return { success: false, message: 'Error al guardar. Inténtalo de nuevo.' };
        }
    }

    try {
        const response = await fetch(`${API_BASE}/api/submit-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                categories: categories,
                podcast_request: podcastRequest
            })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error submitting email:', error);
        return { success: false, message: 'Error al enviar. Inténtalo de nuevo.' };
    }
}

// Submit feedback function
async function submitFeedback(type, content, email) {
    if (!API_BASE) {
        return { success: true, message: '¡Gracias por tu feedback! (Modo local)' };
    }

    try {
        const response = await fetch(`${API_BASE}/api/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: type,
                content: content,
                email: email || ''
            })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error submitting feedback:', error);
        return { success: false, message: 'Error al enviar feedback. Inténtalo de nuevo.' };
    }
}

// Submit Kano survey function
async function submitKanoSurvey(surveyData) {
    if (!API_BASE) {
        return { success: true, message: '¡Gracias por completar la encuesta! (Modo local)' };
    }

    try {
        const response = await fetch(`${API_BASE}/api/kano-survey`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(surveyData)
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error submitting Kano survey:', error);
        return { success: false, message: 'Error al enviar encuesta. Inténtalo de nuevo.' };
    }
}

// Kano survey submission handler
document.getElementById('kanoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const messageElement = document.getElementById('kanoMessage');
    const submitButton = document.getElementById('submitKano');
    
    // Collect all form data
    const formData = new FormData(form);
    const surveyData = {
        email: formData.get('kanoEmail') || ''
    };
    
    // Collect all radio button values
    const radioGroups = [
        'personalizacion_funcional', 'personalizacion_disfuncional',
        'duracion_funcional', 'duracion_disfuncional',
        'voz_funcional', 'voz_disfuncional',
        'fuentes_funcional', 'fuentes_disfuncional'
    ];
    
    // Check if all required fields are filled
    let missingFields = [];
    radioGroups.forEach(field => {
        const value = formData.get(field);
        if (!value) {
            missingFields.push(field);
        } else {
            surveyData[field] = value;
        }
    });
    
    if (missingFields.length > 0) {
        messageElement.textContent = 'Por favor completa todas las preguntas de la encuesta';
        messageElement.className = 'error';
        return;
    }
    
    // Disable button and show loading
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Enviando...';
    submitButton.disabled = true;
    
    try {
        const result = await submitKanoSurvey(surveyData);
        
        messageElement.textContent = result.message;
        messageElement.className = result.success ? 'success' : 'error';
        
        if (result.success) {
            // Reset form
            form.reset();
        }
    } catch (error) {
        messageElement.textContent = 'Error al enviar. Inténtalo de nuevo.';
        messageElement.className = 'error';
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
});

// Email subscription handler
document.getElementById('subscribe').addEventListener('click', async function() {
    const email = document.getElementById('email').value.trim();
    const selectedTags = getSelectedTags();
    const podcastRequest = getPodcastRequest();
    
    if (!email) {
        document.getElementById('message').textContent = 'Por favor ingresa tu email';
        document.getElementById('message').className = 'error';
        return;
    }
    
    if (selectedTags.length === 0) {
        document.getElementById('message').textContent = 'Por favor selecciona al menos una categoría';
        document.getElementById('message').className = 'error';
        return;
    }
    
    const button = this;
    const originalText = button.textContent;
    button.textContent = 'Enviando...';
    button.disabled = true;
    
    try {
        const result = await submitEmail(email, selectedTags, podcastRequest);
        
        document.getElementById('message').textContent = result.message;
        document.getElementById('message').className = result.success ? 'success' : 'error';
        
        if (result.success) {
            // Clear form
            document.getElementById('email').value = '';
            document.getElementById('podcastRequest').value = '';
            
            // Clear selected tags
            document.querySelectorAll('.tag.selected').forEach(tag => {
                tag.classList.remove('selected');
            });
            
            // Update counter
            const currentCount = parseInt(document.getElementById('count').textContent);
            animateCounter(currentCount + 1);
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Error al enviar. Inténtalo de nuevo.';
        document.getElementById('message').className = 'error';
    } finally {
        button.textContent = originalText;
        button.disabled = false;
    }
});

// Feedback submission handler
document.getElementById('submitFeedback').addEventListener('click', async () => {
    const content = document.getElementById('feedbackContent').value.trim();
    const email = document.getElementById('feedbackEmail').value.trim();
    const feedbackType = document.querySelector('input[name="feedbackType"]:checked').value;
    const messageElement = document.getElementById('feedbackMessage');
    
    if (!content) {
        messageElement.textContent = 'Por favor ingresa tu idea o feedback';
        messageElement.className = 'error';
        return;
    }
    
    // Disable button and show loading
    const button = document.getElementById('submitFeedback');
    const originalText = button.textContent;
    button.textContent = 'Enviando...';
    button.disabled = true;
    
    try {
        const result = await submitFeedback(feedbackType, content, email);
        
        messageElement.textContent = result.message;
        messageElement.className = result.success ? 'success' : 'error';
        
        if (result.success) {
            document.getElementById('feedbackContent').value = '';
            document.getElementById('feedbackEmail').value = '';
        }
    } catch (error) {
        messageElement.textContent = 'Error al enviar. Inténtalo de nuevo.';
        messageElement.className = 'error';
    } finally {
        button.textContent = originalText;
        button.disabled = false;
    }
});

// Load counter when page loads
document.addEventListener('DOMContentLoaded', loadCounter);

// Audio error handling
document.addEventListener('DOMContentLoaded', function() {
    const audioElements = document.querySelectorAll('audio');
    
    audioElements.forEach((audio, index) => {
        audio.addEventListener('error', function(e) {
            console.error(`Error loading audio ${index + 1}:`, e);
            console.error('Audio source:', audio.currentSrc);
            console.error('Error details:', audio.error);
            
            // Show user-friendly error message
            const audioCard = audio.closest('.audio-card');
            if (audioCard) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'audio-error';
                errorMsg.innerHTML = `
                    <p style="color: #dc3545; background: #f8d7da; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                        ⚠️ Error al cargar el audio. Verifica que el archivo existe en: ${audio.currentSrc}
                    </p>
                `;
                audio.parentNode.insertBefore(errorMsg, audio.nextSibling);
            }
        });
        
        audio.addEventListener('loadstart', function() {
            console.log(`Loading audio ${index + 1}:`, audio.currentSrc);
        });
        
        audio.addEventListener('canplay', function() {
            console.log(`Audio ${index + 1} ready to play`);
        });
    });
});

// Tag selection functionality
document.addEventListener('DOMContentLoaded', function() {
    const tags = document.querySelectorAll('.tag');
    
    tags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.classList.toggle('selected');
            
            // Add visual feedback
            if (this.classList.contains('selected')) {
                this.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
            }
        });
    });
});

// Get selected tags for form submission
function getSelectedTags() {
    const selectedTags = document.querySelectorAll('.tag.selected');
    return Array.from(selectedTags).map(tag => tag.dataset.value);
}

// Get podcast request text
function getPodcastRequest() {
    return document.getElementById('podcastRequest').value.trim();
}
