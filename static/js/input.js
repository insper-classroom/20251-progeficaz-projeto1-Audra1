document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.getElementById('title-input');
    const descriptionInput = document.getElementById('description-input');
    const inputBox = document.querySelector('.input-box');
    
    // Add event listener for global Enter key
    document.addEventListener('keydown', function(e) {
        // Only focus title input if we're not already in a textarea
        if (e.key === 'Enter' && 
            !e.target.matches('textarea') && 
            document.activeElement !== titleInput) {
            e.preventDefault();
            titleInput.focus();
        }
    });

    titleInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const container = document.querySelector('.input-container');
            const description = document.getElementById('description-input');
            
            container.style.height = '70px';
            description.classList.add('visible');
            description.focus();
        }
    });

    descriptionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitNote(titleInput.value, descriptionInput.value);
            
            titleInput.value = '';
            descriptionInput.value = '';
            descriptionInput.classList.remove('visible');
            document.querySelector('.input-container').style.height = '39px';
            titleInput.focus();
        }
    });

    // Auto-resize textareas as user types
    [titleInput, descriptionInput].forEach(textarea => {
        textarea.addEventListener('input', function() {
            if (this.id === 'description-input') {
                const scrollHeight = Math.max(31, this.scrollHeight);
                this.style.height = scrollHeight + 'px';
            }
        });
    });

    function getCurrentSpace() {
        const activeSpace = document.querySelector('.space-item.active');
        return {
            id: activeSpace.dataset.spaceId,
            name: activeSpace.childNodes[0].textContent.trim()
        };
    }

    function submitNote(title, description) {
        if (!title.trim()) {
            return;
        }
        
        const space = getCurrentSpace();
        
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `space_id=${encodeURIComponent(space.id)}&space=${encodeURIComponent(space.name)}&titulo=${encodeURIComponent(title)}&detalhes=${encodeURIComponent(description)}`
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
        // Extract the actual note ID from the composite ID (space_id/note_id)
        const actualNoteId = noteId.split('/').pop();
        
        fetch(`/update/${actualNoteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, details })
        })
        .catch(error => console.error('Error saving note:', error));
    }, 500);  // 500ms delay

    // Add this function at the start of your file
    function saveNoteImmediate(noteId, title, details) {
        const actualNoteId = noteId.split('/').pop();
        
        return fetch(`/update/${actualNoteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, details })
        }).catch(error => console.error('Error saving note:', error));
    }

    // Modify the existing event listeners section
    document.querySelectorAll('.note-container').forEach(note => {
        const noteId = note.dataset.noteId;
        const titleArea = note.querySelector('.note-title');
        const detailsArea = note.querySelector('.note-details');

        // Save while typing (debounced)
        [titleArea, detailsArea].forEach(textarea => {
            textarea.addEventListener('input', () => {
                saveNote(noteId, titleArea.value, detailsArea.value);
            });
        });

        // Save before page unload if there are unsaved changes
        [titleArea, detailsArea].forEach(textarea => {
            textarea.addEventListener('blur', () => {
                saveNoteImmediate(noteId, titleArea.value, detailsArea.value);
            });
        });

        // Show details on note click
        note.addEventListener('click', (e) => {
            if (e.target === titleArea || e.target === detailsArea) {
                detailsArea.classList.add('visible');
            }
        });

        // Hide empty details when clicking outside
        document.addEventListener('click', (e) => {
            if (!note.contains(e.target) && !detailsArea.value.trim()) {
                detailsArea.classList.remove('visible');
            }
        });
    });

    // Add after existing code inside DOMContentLoaded
    document.querySelectorAll('.menu-trigger').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const menu = trigger.nextElementSibling;
            menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.delete-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    });

    // Handle delete option
    document.querySelectorAll('.delete-option').forEach(option => {
        option.addEventListener('click', (e) => {
            e.stopPropagation();
            const noteId = option.closest('.note-wrapper').querySelector('.note-container').dataset.noteId;
            
            fetch(`/delete/${noteId}`, {
                method: 'POST'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                window.location.reload();
            })
            .catch(error => {
                console.error('Error deleting note:', error);
            });
        });
    });

    // Add this function at the start of your DOMContentLoaded
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    // Add event listeners for all textareas (both input and notes)
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', () => {
            autoResize(textarea);
        });
        
        // Initial resize
        autoResize(textarea);
    });

    // Space navigation
    document.querySelectorAll('.space-item').forEach(item => {
        item.addEventListener('click', () => {
            // Get only the text content, excluding the delete button
            const spaceName = item.childNodes[0].textContent.trim();
            window.location.href = `/${encodeURIComponent(spaceName)}`;
        });
    });

    // Add new space
    const addSpaceBtn = document.querySelector('.add-space-btn');
    addSpaceBtn.addEventListener('click', () => {
        const spaceName = prompt('Enter space name:');
        if (spaceName && spaceName.trim()) {
            fetch('/create-space', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: spaceName.trim() })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Space creation failed');
                }
                window.location.href = `/${encodeURIComponent(spaceName.trim())}`;
            })
            .catch(error => {
                console.error('Error creating space:', error);
                alert('Failed to create space. Please try again.');
            });
        }
    });

    // Add this inside your DOMContentLoaded event listener
    document.querySelectorAll('.delete-space-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const spaceItem = btn.parentElement;
            const spaceId = spaceItem.dataset.spaceId;
            const spaceName = spaceItem.textContent.trim().slice(0, -1); // Remove the × button text
            
            if (confirm(`Are you sure you want to delete the space "${spaceName}" and all its notes?`)) {
                fetch(`/delete-space/${spaceId}`, {
                    method: 'POST'
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error('Error deleting space:', error);
                    alert('Failed to delete space. Please try again.');
                });
            }
        });
    });

    // Add this event listener at the end of your DOMContentLoaded
    window.addEventListener('beforeunload', (e) => {
        const unsavedNotes = document.querySelectorAll('.note-container');
        
        unsavedNotes.forEach(note => {
            const noteId = note.dataset.noteId;
            const titleArea = note.querySelector('.note-title');
            const detailsArea = note.querySelector('.note-details');

            if (titleArea && detailsArea) {
                saveNoteImmediate(noteId, titleArea.value, detailsArea.value);
            }
        });
    });

    // Add this inside your DOMContentLoaded event listener
    const spaceTitle = document.querySelector('.space-title');

    spaceTitle.addEventListener('blur', () => {
        const newName = spaceTitle.textContent.trim();
        if (newName) {
            fetch('/update-space-name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    space_id: getCurrentSpace().id,
                    name: newName
                })
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to update space name');
                window.history.pushState({}, '', `/${encodeURIComponent(newName)}`);
            })
            .catch(error => console.error('Error updating space name:', error));
        }
    });
});
