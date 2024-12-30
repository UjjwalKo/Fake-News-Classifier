document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        setTimeout(function() {
            messageContainer.style.opacity = '0';
            setTimeout(function() {
                messageContainer.style.display = 'none';
            }, 500); // Wait for fade out animation to complete
        }, 4000); // 4 seconds
    }
});