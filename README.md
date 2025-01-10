GI_Assessment
Objective:
  Develop a custom Django middleware to implement request rate limiting based on IP addresses.

Functionality:
  Implement a middleware that tracks the number of requests made by a user (identified by their IP address).
Block requests from an IP if the number exceeds 100 requests in a rolling 5-minute window.
Return an HTTP 429 (Too Many Requests) status code for blocked IPs.

Technologies Used:
  Python,
  Django,
  Django Cache Framework

Installation Instructions:

1) Clone the repository :
  git clone https://github.com/midhuprasad/GI_Assessment.git

2) Navigate to the project directory :
  cd GI_Assessment

3) Set up a virtual environment : 
  python -m venv venv
  source venv\Scripts\activate

4) Start server : 
python manage.py runserver
