document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and options
      activitiesList.innerHTML = "";
      
      // Clear dropdown options except the first one
      while (activitySelect.options.length > 1) {
        activitySelect.remove(1);
      }

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-section">
            <p><strong>Participants (${details.participants.length}/${details.max_participants}):</strong></p>
            <ul class="participants-list">
              ${details.participants.map(participant => `<li><span class="participant-email">${participant}</span><button class="delete-participant" data-email="${participant}" data-activity="${name}" title="Remove participant">×</button></li>`).join('')}
            </ul>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Add event delegation for delete buttons (outside fetchActivities to avoid duplicates)
  activitiesList.addEventListener("click", async (event) => {
    if (event.target.classList.contains("delete-participant")) {
      const email = event.target.getAttribute("data-email");
      const activityName = event.target.getAttribute("data-activity");

      if (confirm(`Remove ${email} from ${activityName}?`)) {
        try {
          const response = await fetch(
            `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
            { method: "POST" }
          );

          if (response.ok) {
            messageDiv.textContent = `${email} has been removed from ${activityName}`;
            messageDiv.className = "success";
            messageDiv.classList.remove("hidden");
            setTimeout(() => {
              messageDiv.classList.add("hidden");
            }, 5000);
            fetchActivities(); // Refresh the list
          } else {
            const error = await response.json();
            messageDiv.textContent = error.detail || "Failed to remove participant";
            messageDiv.className = "error";
            messageDiv.classList.remove("hidden");
          }
        } catch (error) {
          messageDiv.textContent = "Failed to remove participant. Please try again.";
          messageDiv.className = "error";
          messageDiv.classList.remove("hidden");
          console.error("Error removing participant:", error);
        }
      }
    }
  });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities(); // Refresh the list to show updated participants
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
