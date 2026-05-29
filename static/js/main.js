// =============================================================
// main.js — Small JavaScript helpers
// VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
// =============================================================
// Keep this file small and simple.
// Bootstrap handles most interactive components (navbar, dropdowns).
// Add only what Bootstrap cannot do.
// =============================================================


// Auto-dismiss flash alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Bootstrap's Alert API to close it smoothly
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
