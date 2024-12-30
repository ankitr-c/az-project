document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addDataForm');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Gather form data
        const formData = {
            name: form.name.value,
            email: form.email.value,
            mobile: form.mobile.value
        };

        try {
            // Make POST request to add_data API
            const response = await fetch('http://localhost:5000/add_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                // Display success message
                messageDiv.textContent = 'User added successfully!';
                messageDiv.style.color = 'green';
                form.reset();
            } else {
                // Display error message
                messageDiv.textContent = `Error: ${result.error}`;
                messageDiv.style.color = 'red';
            }
        } catch (error) {
            // Display network error message
            messageDiv.textContent = `Network error: ${error.message}`;
            messageDiv.style.color = 'red';
        }
    });
});
