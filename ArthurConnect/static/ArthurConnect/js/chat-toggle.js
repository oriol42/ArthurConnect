// Chat Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const closeChat = document.getElementById('close-chat');
    
    if (chatToggle && chatWidget) {
        // Toggle chat visibility
        chatToggle.addEventListener('click', function() {
            chatWidget.classList.toggle('d-none');
            chatToggle.classList.toggle('active');
        });
        
        // Close chat
        if (closeChat) {
            closeChat.addEventListener('click', function() {
                chatWidget.classList.add('d-none');
                chatToggle.classList.remove('active');
            });
        }
        
        // Close chat when clicking outside
        document.addEventListener('click', function(event) {
            if (!chatToggle.contains(event.target) && !chatWidget.contains(event.target)) {
                chatWidget.classList.add('d-none');
                chatToggle.classList.remove('active');
            }
        });
    }
});

// Add to Cart Function
function addToCart(productId) {
    fetch(`/arthurconnect/add-to-cart/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showMessage('Produit ajouté au panier!', 'success');
            // Update cart count
            updateCartCount();
        } else {
            showMessage(data.message || 'Erreur lors de l\'ajout au panier', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Erreur lors de l\'ajout au panier', 'error');
    });
}

// Add to Wishlist Function
function addToWishlist(productId) {
    fetch(`/arthurconnect/add-to-wishlist/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('Produit ajouté aux favoris!', 'success');
        } else {
            showMessage(data.message || 'Erreur lors de l\'ajout aux favoris', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Erreur lors de l\'ajout aux favoris', 'error');
    });
}

// Update Cart Count
function updateCartCount() {
    fetch('/arthurconnect/cart-count/')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                if (data.count > 0) {
                    cartCount.textContent = data.count;
                    cartCount.style.display = 'inline';
                } else {
                    cartCount.style.display = 'none';
                }
            }
        })
        .catch(error => console.log('Erreur lors du chargement du panier:', error));
}

// Show Message Function
function showMessage(message, type) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
    messageDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    messageDiv.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert">
            <span>&times;</span>
        </button>
    `;
    
    // Add to page
    document.body.appendChild(messageDiv);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});
