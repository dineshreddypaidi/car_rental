document.addEventListener('DOMContentLoaded', function () {
    var messageTypeElement = document.getElementById('message-type');
    if (messageTypeElement) {
        var messageType = messageTypeElement.getAttribute('data-type');
        if (messageType === 'success') {
            var successModal = new bootstrap.Modal(document.getElementById('statusSuccessModal'));
            successModal.show();
        } else if (messageType === 'error') {
            var errorModal = new bootstrap.Modal(document.getElementById('statusErrorsModal'));
            errorModal.show();
        }
    }
});
