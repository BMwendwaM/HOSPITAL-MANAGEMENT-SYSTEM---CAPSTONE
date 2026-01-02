import os
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Triage, Diagnosis
from .serializers import TriageSerializer, DiagnosisSerializer
from visits.models import Visit

class TriageViewSet(viewsets.ModelViewSet):
    queryset = Triage.objects.all()
    serializer_class = TriageSerializer

    # When Nurse saves Triage, move patient to Consultation
    def perform_create(self, serializer):
        instance = serializer.save(nurse=self.request.user)
        
        # Find the visit and update status
        visit = instance.visit
        visit.status = Visit.Status.CONSULTATION
        visit.save()

    # Prevent Delete operations on triage records
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Security Alert: Medical records cannot be deleted. They are permanent."}, 
            status=status.HTTP_403_FORBIDDEN
        )

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

    def perform_create(self, serializer):
        # Analyze doctor's prescription to find muscle names
        # Get the prescription text

        prescription_text = serializer.validated_data.get("prescription", "").lower()
        
        # List of valid muscle names for API search

        valid_muscles = [
            "abdominals", "abductors", "adductors", "biceps", "calves", 
            "chest", "forearms", "glutes", "hamstrings", "lats", 
            "lower_back", "middle_back", "neck", "quadriceps", 
            "traps", "triceps"
        ]
        
        # Check for muscle names in the prescription

        target_muscle = None
        for muscle in valid_muscles:
            if muscle in prescription_text:
                target_muscle = muscle

                # Found a muscle, no need to check further
                break 

        # Call external API to get exercise suggestion

        added_info = ""

        # Get API key from environment variable
        api_key = os.getenv("API_NINJAS_KEY")

        # Only call API if we found a muscle and have an API key

        if target_muscle and api_key:
            api_url = f"https://api.api-ninjas.com/v1/exercises?muscle={target_muscle}&difficulty=beginner"
            
            try:
                # Send GET request to the API

                response = requests.get(api_url, headers={"X-Api-Key": api_key})
                
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        # Take the first exercise suggestion
                        exercise = data[0]
                        added_info = (
                            f"\n\n--- SMART PHYSIO SUGGESTION ---\n"
                            f"Exercise: {exercise.get('name')}\n"
                            f"Instructions: {exercise.get('instructions')}"
                        )
            except Exception as e:
                # In case of any error, we just skip adding info
                print(f"External API Error: {e}")

        # Save the Diagnosis record with appended exercise suggestion
        original_prescription = serializer.validated_data.get("prescription", "")
        
        instance = serializer.save(
            doctor=self.request.user,
            prescription=original_prescription + added_info
        )

        # After Diagnosis, move patient based on follow-up decision
        visit = instance.visit
        decision = instance.follow_up
        
        if decision == "lab":
            visit.status = Visit.Status.LAB
        elif decision == "radiology":
            visit.status = Visit.Status.RADIOLOGY
        elif decision == "pharmacy":
            visit.status = Visit.Status.PHARMACY
        else:
            # Default to billing if no follow-up
            visit.status = Visit.Status.BILLING
            
        visit.save()

        # Prevent Delete operations on triage and diagnosis records
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Security Alert: Medical records cannot be deleted. They are permanent."}, 
            status=status.HTTP_403_FORBIDDEN
        )
