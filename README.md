# HomeScope

HomeScope is a web application that predicts the price of a prospective Austin, TX area home purchase based on user-inputted details. Powered by a custom-trained machine learning model, it provides a straightforward way to get real-time insights into property pricing.


## Features
- Price Prediction: Input key details about a home, and HomeScope predicts the price using an XGBoost model.
- Train Your Model: Easily retrain the model on your data with train.py.
- Intuitive Interface: A modern, responsive frontend built with Bootstrap.
- Secure & Scalable Deployment: Hosted on an AWS EC2 instance with Nginx, Gunicorn, and Let's Encrypt SSL.

## Tech Stack
### Frontend:

Built with Bootstrap (via Bootstrap Studio).
Client-side scripting in pure JavaScript.
### Backend:

Flask application served via Gunicorn.
Hosted on Ubuntu EC2 with Nginx as a reverse proxy.
### Machine Learning:

- Model: XGBoost.
- Libraries:
    - Data Wrangling: Pandas, NumPy.
    - Model Training: Scikit-learn, XGBoost.
    - Visualization: Matplotlib, Seaborn, Plotly.
    - Serialization: Joblib.

## Setup Instructions

### Prerequisites
- Python 3.8 or later
- Ubuntu (or compatible Linux distribution)
- AWS EC2 instance (optional for deployment)
- Nginx and Gunicorn (optional for deployment)


### Local Development
1. Clone the Repository:
    ```bash
    git clone https://github.com/calebkress/homescope-release.git
    cd homescope-release
    ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Train the Model:
    ```bash
    python3 model/train.py
    ```
4. Run the Application - start the Flask server locally:
    ```bash
    python3 backend/app/routes.py
    ```

## Deployment

### Server Setup
- Hosting: Deployed on an AWS EC2 instance running Ubuntu.
- Stack:
    - Flask backend served with Gunicorn.
    - Nginx for reverse proxy and SSL termination.
    - Let's Encrypt for SSL.

### Deployment Workflow
1. Train the Model: Train the model locally or on the server using train.py and save the model with Joblib.

2. Configure Gunicorn - create a systemd service for Gunicorn:

    ```bash
    [Unit]
    Description=Gunicorn instance to serve HomeScope
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/path/to/homescope
    ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 wsgi:app

    [Install]
    WantedBy=multi-user.target
    ```
3. Configure Nginx - set up Nginx as a reverse proxy:
    ```bash
    server {
        listen 80;
        server_name homescope.homes www.homescope.homes;

        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name homescope.homes www.homescope.homes;

        ssl_certificate /etc/letsencrypt/live/homescope.homes/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/homescope.homes/privkey.pem;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
4. Obtain SSL Certificate - use Certbot to generate and renew SSL certificates:
    ```bash
    sudo certbot --nginx -d homescope.homes -d www.homescope.homes
    ```
5. Restart Services:
    ```bash
    sudo systemctl restart nginx
    sudo systemctl start homescope.service
    ```

## Usage
1. Visit deployed website:
    ```
    https://homescope.homes
    ```
2. Enter details about the prospective home:

- Square footage
- Location
- Number of bedrooms/bathrooms
- All other fields

3. Receive a price prediction in real time!


## License
This project is licensed under the MIT License. See LICENSE for details.


