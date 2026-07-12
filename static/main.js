setTimeout(function () {
    const alerts = document.querySelectorAll('.flash-alert');

    alerts.forEach(function (alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 3000);