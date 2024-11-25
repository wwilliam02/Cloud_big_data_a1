        // JavaScript to send form data as JSON using fetch
        document.getElementById('eventForm').addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent the default form submission

            // Create a JavaScript object with the form data
            const formData = {
                artist: document.getElementById('artist').value,
                venue: document.getElementById('venue').value,
                date: document.getElementById('date').value,
                tour: document.getElementById('tour').value
            };

            // Send the form data as JSON to the server using fetch API
            fetch('/concert', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'  // Indicate that we are sending JSON
                },
                body: JSON.stringify(formData)  // Convert the form data object to a JSON string
            })
            .then(response => response.json())  // Parse the JSON response from Flask
            .then(data => {
                // Handle success: Display the message in the responseMessage div
                const responseMessageDiv = document.getElementById('responseMessage');
                responseMessageDiv.innerHTML = `
                    <p style="color: green;">${data.message}</p>
                `;
                // Optionally reload concerts list
                fetchConcerts();
            })
            .catch(error => {
                // Handle any errors that occur during the fetch request
                const responseMessageDiv = document.getElementById('responseMessage');
                responseMessageDiv.innerHTML = `<p style="color: red;">Error: ${error}</p>`;
            });
        });

        // Fetch and display all concerts
        function fetchConcerts() {
            fetch('/concert', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById("concertsTableBody");
                tableBody.innerHTML = ""; // Clear existing rows

                data.concerts.forEach(concert => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${concert._id}</td>
                        <td>${concert.artist}</td>
                        <td>${concert.venue}</td>
                        <td>${concert.date}</td>
                        <td>${concert.tour || "N/A"}</td>
                        <td><button onclick="deleteConcert('${concert._id}')">Delete</button></td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error loading concerts:", error);
            });
        }
        // Delete a concert by ID
        function deleteConcert(concertId) {
            if (!confirm("Are you sure you want to delete this concert?")) {
                return;
            }

            fetch(`/concert/${concertId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || "Concert deleted successfully");
                fetchConcerts(); // Reload the concert list
            })
            .catch(error => {
                console.error("Error deleting concert:", error);
            });
        }
        // Load concerts when the "Load All Concerts" button is clicked
        document.getElementById('loadConcerts').addEventListener('click', fetchConcerts);

        // Optionally load concerts automatically on page load
        // window.onload = fetchConcerts;