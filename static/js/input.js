document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.getElementById('title-input');
    const descriptionInput = document.getElementById('description-input');
    const inputBox = document.querySelector('.input-box');
    




    titleInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            inputBox.style.minHeight = '96px'; // Increase box height
            descriptionInput.style.display = 'block';
            descriptionInput.focus();
        }
    });

    descriptionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitNote(titleInput.value, descriptionInput.value);
            
            // Reset the form and box
            titleInput.value = '';
            descriptionInput.value = '';
            descriptionInput.style.display = 'none';
            inputBox.style.minHeight = '48px';
            titleInput.focus();
        }
    });

    // Auto-resize textareas as user types
    [titleInput, descriptionInput].forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    function submitNote(title, description) {
        if (!title.trim()) {
            return; // Don't submit if title is empty
        }

        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `titulo=${encodeURIComponent(title)}&detalhes=${encodeURIComponent(description)}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response;
        })
        .then(() => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Error submitting note:', error);
            // Could add user feedback here
        });
    }

    // Debounce function to limit API calls
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Auto-save function
    const saveNote = debounce((noteId, title, details) => {
        fetch(`/update/${noteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, details })
        })
        .catch(error => console.error('Error saving note:', error));
    }, 500);  // 500ms delay

    // Add event listeners to existing notes
    document.querySelectorAll('.note-container').forEach(note => {
        const noteId = note.dataset.noteId;
        const titleArea = note.querySelector('.note-title');
        const detailsArea = note.querySelector('.note-details');

        [titleArea, detailsArea].forEach(textarea => {
            textarea.addEventListener('input', () => {
                saveNote(noteId, titleArea.value, detailsArea.value);
            });
        });
    });
});
