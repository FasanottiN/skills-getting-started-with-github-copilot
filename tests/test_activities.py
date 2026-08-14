"""
Tests for GET /activities endpoint.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        AAA Pattern:
        - Arrange: Use client fixture (already has fresh activities data)
        - Act: Make GET request to /activities
        - Assert: Status 200, response is dict, contains all expected activity names
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Drama Club", "Science Club", "Debate Team"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_get_activities_has_correct_structure(self, client):
        """
        Test that each activity has required fields with correct structure.
        
        AAA Pattern:
        - Arrange: Use client fixture
        - Act: Make GET request and extract first activity
        - Assert: Verify all required fields present and correct types
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        for field in required_fields:
            assert field in first_activity, f"Missing field: {field}"
        
        assert isinstance(first_activity["description"], str)
        assert isinstance(first_activity["schedule"], str)
        assert isinstance(first_activity["max_participants"], int)
        assert isinstance(first_activity["participants"], list)
    
    def test_get_activities_has_participant_data(self, client):
        """
        Test that activities have participant lists with correct data.
        
        AAA Pattern:
        - Arrange: Use client fixture
        - Act: Make GET request
        - Assert: Verify participant count, max_participants, and list contents
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        
        # Chess Club should have 2 participants
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert chess_club["max_participants"] == 12
        
        # Programming Class should have 2 participants
        prog_class = activities["Programming Class"]
        assert len(prog_class["participants"]) == 2
        assert prog_class["max_participants"] == 20
