"""
Tests for POST /activities/{activity_name}/unregister endpoint.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestUnregister:
    """Test suite for POST /unregister endpoint"""
    
    def test_unregister_success(self, client):
        """
        Test successful student unregistration from activity.
        
        AAA Pattern:
        - Arrange: Get activity with participants, select one to remove
        - Act: Make POST request to unregister endpoint
        - Assert: Status 200, participant removed, count decremented
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Verify initial state
        activities = client.get("/activities").json()
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email_to_remove in data["message"]
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1
    
    def test_unregister_nonexistent_activity(self, client):
        """
        Test unregister fails when activity doesn't exist.
        
        AAA Pattern:
        - Arrange: Prepare non-existent activity name
        - Act: Make POST request with invalid activity
        - Assert: Status 404, error detail provided
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_registered(self, client):
        """
        Test unregister fails when student isn't registered for activity.
        
        AAA Pattern:
        - Arrange: Prepare email not in activity participants
        - Act: Try to unregister email not registered
        - Assert: Status 400, error detail about not registered, list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        unregistered_email = "neverjoined@mergington.edu"
        
        # Verify initial state
        activities = client.get("/activities").json()
        initial_participants = activities[activity_name]["participants"].copy()
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": unregistered_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
        
        # Verify participant list unchanged
        activities = client.get("/activities").json()
        assert activities[activity_name]["participants"] == initial_participants
    
    def test_unregister_then_signup_again(self, client):
        """
        Test that a student can unregister and then re-register for same activity.
        
        AAA Pattern:
        - Arrange: Get activity with participant
        - Act: Unregister, then signup again
        - Assert: Both operations succeed, participant present at end
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Remove
        response_remove = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Re-register
        response_add = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response_remove.status_code == 200
        assert response_add.status_code == 200
        
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
