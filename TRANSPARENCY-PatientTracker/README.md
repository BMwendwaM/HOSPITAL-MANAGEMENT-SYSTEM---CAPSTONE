# TRANSPARENCY-PatientTracker

## Project Overview

TRANSPARENCY-PatientTracker is a Hospital Management System developed using Django and Django REST 
Framework. The primary goal of the system is to provide total visibility into a patient's journey through 
the hospital, solving the common problem of patients getting "lost" in the workflow.

Unlike standard database applications, this system uses an event-driven engine. It automatically updates 
the patient's status (Reception -> Triage -> Doctor -> Billing) based on staff actions. This ensures that 
hospital administration always knows exactly where a patient is and prevents patients from leaving 
without finalizing their bills.

## Key Features

### 1. Automated Workflow Tracking
The system manages the patient queue automatically. Staff do not need to manually change status fields; 
the system reacts to their work:
*   **Reception:** Checking in a patient starts the visit with status "Waiting".
*   **Triage:** When a nurse submits vitals, the patient moves to "Consultation".
*   **Diagnosis:** When a doctor submits a diagnosis, the patient moves to "Billing" (or Lab/Pharmacy/
Radiology).
*   **Discharge:** When a cashier processes payment, the status becomes "Completed".

### 2. Smart External API Integration
The system integrates with the API Ninjas Exercises API to assist doctors.
*   **Smart Suggestions:** If a doctor prescribes "rest and biceps therapy", the system detects the 
muscle group, queries the external API and automatically appends specific physiotherapy instructions to 
the patient's prescription record.

### 3. Security and Data Integrity
*   **Role-Based Access:** Specific permissions are enforced for Nurses, Doctors and Cashiers.
*   **Delete Protection:** The system enforces strict rules preventing the deletion of medical history or 
financial records, ensuring data integrity and compliance.
*   **Environment Security:** API keys and debug settings are managed via environment variables.


### 4. Financial Controls
*   **Invoice Management:** Services are dynamically added to invoices.
*   **Discharge Lock:** The system prevents a visit from being marked as "Completed" until the invoice is 
fully paid.

## Technical Stack

*   **Backend:** Django, Django REST Framework
*   **Database:** SQLite (Development) / PostgreSQL (Production)
*   **Authentication:** JWT (JSON Web Tokens)
*   **External API:** API Ninjas (Exercises)
*   **Testing:** Django TestCase (Unit and Integration tests)

## Installation and Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/BMwendwaM/HOSPITAL-MANAGEMENT-SYSTEM---CAPSTONE.git
    cd HOSPITAL-MANAGEMENT-SYSTEM---CAPSTONE
    ```

2.  **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a .env file in the root directory:
    ```text
    SECRET_KEY=your_secret_key
    DEBUG=True
    API_NINJAS_KEY=your_api_key
    ```

5.  **Run Migrations and Create Admin**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## API Usage

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/patients/` | POST | Register a new patient |
| `/api/visits/` | GET/POST | Create a visit or filter by status |
| `/api/medical/triage/` | POST | Nurse records vitals (Moves patient to Consultation) |
| `/api/medical/diagnosis/` | POST | Doctor records diagnosis (Triggers API & moves patient) |
| `/api/billing/invoices/{id}/pay/` | POST | Finalize payment and discharge patient |

## Testing

The project includes integration tests to verify the workflow logic and security features. Run them using:
```bash
python manage.py test