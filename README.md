Prerequisites
**Docker Desktop must be installed and running in the background.**
Steps to Run.......
1. Pull the Image :Download the specific version of the image from Docker Hub:
CMD
**docker pull nidhi1011/march-1:0.0.1.RELEASE**
2. Run the Container :Start the application and map the ports so you can access it on your browser:
CMD
**docker run -d -p 5000:5000 nidhi1011/march-1:0.0.1.RELEASE**
4. Access the App :Open your browser and go to:
**http://localhost:5000**


**Notes for Self:**
1. Backend Development (Flask)
REST API Architecture: Developed a Flask-based web application with structured routing (/, /welcome, /movies).
Request Handling: Implemented logic for multiple HTTP methods (GET/POST) and dynamic URL parameters for personalized data delivery.
Modular Design: Followed clean code principles by decoupling core application logic from external helper services.
2. Software Quality Assurance (Pytest)
Comprehensive Test Suite: Designed a full testing framework to automate route validation.
Diverse Testing Scenarios: Covered Happy Paths, Edge Cases (empty strings, numeric inputs, special characters), and Negative Testing (404 and 405 error handling).
Advanced Mocking: Leveraged unittest.mock to simulate slow external dependencies, significantly reducing test execution time.
3. DevOps & Automation
CI/CD Pipeline: Configured GitHub Actions to automatically trigger the test suite on every code push, ensuring continuous integration.
Version Control: Managed the full development lifecycle using Git and GitHub.
Documentation: Authored a professional README.md with technical setup and deployment instructions.
4. Containerization (Docker)
Application Dockerization: Created a Docker image (nidhi1011/march-1) for consistent deployment across environments.
Image Management: Implemented semantic versioning (0.0.1.RELEASE) and hosted the final image on Docker Hub for public accessibility.
