function toggleAvailability(memberId) {
    const checkbox = document.getElementById(`toggle-${memberId}`);
    const badge = document.getElementById(`badge-${memberId}`);
    const row = document.getElementById(`row-${memberId}`);

    const isAvailable = checkbox.checked;

    // Disable control during update
    checkbox.disabled = true;

    // Send status change request to Flask backend
    fetch(`/update_status/${memberId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ is_available: isAvailable })
    })
        .then(response => response.json())
        .then(data => {
            checkbox.disabled = false;

            if (data.success) {
                // Update frontend badge content and styling classes smoothly
                if (data.is_available) {
                    badge.textContent = 'AVAILABLE';
                    badge.className = 'status-badge available';
                    row.className = 'member-available';
                } else {
                    badge.textContent = 'BUSY';
                    badge.className = 'status-badge busy';
                    row.className = 'member-busy';
                }
            } else {
                // Revert state if error occurred
                checkbox.checked = !isAvailable;
                alert('Failed to update status: ' + data.error);
            }
        })
        .catch(error => {
            checkbox.disabled = false;
            checkbox.checked = !isAvailable;
            console.error('Request failed:', error);
            alert('Network request failed. Please check backend connection.');
        });
}
