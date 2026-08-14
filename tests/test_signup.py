"""
Tests for POST /activities/{activity_name}/signup endpoint.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestSignup:
    """Test suite for POST /signup endpoint"""
    
    def test_signup_success(self, client):
        """
        Test successful student signup for an activity.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new student email
        - Act: Make POST request to signup endpoint
        - Assert: Status 200, message correct, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in data["message"]
        assert activity_name in data["message"]
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert new_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 3  # 2 original + 1 new
    
    def test_signup_nonexistent_activity(self, client):
        """
        Test signup fails when activity doesn't exist.
        
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
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_email(self, client):
        """
        Test signup fails when student already registered for activity.
        
        AAA Pattern:
        - Arrange: Get existing participant from activity
        - Act: Try to signup same email for same activity
        - Assert: Status 400, error detail about duplicate, list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
        
        # Verify participant list unchanged
        activities = client.get("/activities").json()
        chess_club = activities[activity_name]
        assert len(chess_club["participants"]) == 2
        assert chess_club["participants"].count(existing_email) == 1
    
    def test_signup_multiple_activities_same_student(self, client):
        """
        Test that a student can signup for multiple different activities.
        
        AAA Pattern:
        - Arrange: Prepare student email and two different activities
        - Act: Signup student to both activities
        - Assert: Status 200 for both, student in both participant lists
        """
        # Arrange
        student_email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student_email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities = client.get("/activities").json()
        assert student_email in activities[activity1]["participants"]
        assert student_email in activities[activity2]["participants"]
