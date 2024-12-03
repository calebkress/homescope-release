# HomeScope

HomeScope is a web application that allows users to recieve machine learning-driven home price predictions for the Austin, TX area. It features a frontend built with JavaScript and Bootstrap, a backend API built with Flask, and a machine learning model deployed on an AWS instance.


## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js (for frontend)
- AWS CLI (for deployment)
- Docker (optional, for containerized deployment)

### Backend
1. Navigate to the `backend` directory.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. Run the Flask server:
    ```
    python run.py
    ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
    ```
    npm install
    ```
3. Start the development server:
    ```
    npm start
    ```

### Deployment
See the `deployment/README.md` for instructions on deploying the application to AWS.

### Roadmap
 - Redo model code
 - Develop Flask API
 - Complete frontend integration
 - Deploy on AWS

### License
This project is licensed under the MIT License. See LICENSE for details.


