function vote(coffeeId) {
    // Send POST request to vote API
    fetch(`/vote/${coffeeId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Find HTML element displaying votes for this coffee and update the value dynamically
                const voteCountElement = document.getElementById(`vote-count-${coffeeId}`);
                if (voteCountElement) {
                    voteCountElement.textContent = `Votes: ${data.votes}`;
                }
            } else {
                console.error('Error recording vote:', data.error);
            }
        })
        .catch(error => {
            console.error('Request failed:', error);
        });
}
