# Lexify

## Setup
NOTE: Note that the docker-compose configurations for development/production environments aren't made. Just yet.

1. `git clone https://github.com/NasuPanda/lexify`
2. `cd lexify`
3. `docker-compose up --build`

### Testing

1. Setup: `ALEMBIC_ENV=test alembic upgrade head` (Assuming your projects already has alembic migration file)

## 1. Background

This application is designed to assist in vocabulary expansion during English language learning. It was created as a personal project to avoid the costs associated with similar applications while providing tailored functionality.

## 2. Requirements

- **Must-Have Features**:
  - User Authentication: Simple username/password mechanism.
  - Card Creation and Review: Support for text, examples, images, and audio clips.
  - Input Method: Uploading data via a spreadsheet.
  - Review Scheduling: User-configurable, based on confidence levels.
  - Cloud Storage: Use AWS S3 for multimedia files.
  - Responsive Design: Compatible with both laptops and mobile phones.

- **Nice-to-Have Features**:
  - Kindle Integration: For direct vocabulary extraction.
  - Progress Tracking and Analytics: To monitor learning progress.

## 3. Software Architecture

### Microservices Architecture

- **Frontend**: React-based SPA (Single Page Application).
- **Backend**: FastAPI, utilizing microservices architecture for scalability and maintenance ease.
- **Services**:
  - User Management: Handles user registration and login.
  - Card Management: Manages card creation, retrieval, updating, and deletion.
  - Review Scheduling: Manages the scheduling of card reviews based on user input.
  - File Storage: Utilizing AWS S3 for storing and retrieving multimedia files like images and audio to ensure availability and scalability.

## 4. Database Design

- **AWS RDS with PostgreSQL**:
  - User Management Schema: Stores user data and hashed passwords.
  - Card Management Schema: Stores details of flashcards including links to images and audio files stored in S3.
  - Review Scheduling Schema: Stores data for scheduling reviews based on confidence levels.

## 5. API Design

### 1. User Authentication

- **POST `/auth/register`**: Registers a new user with a username and password (and optionally, email).
- **POST `/auth/login`**: Authenticates a user and returns a session token.

### 2. Card Management

- **POST `/cards`**: Allows a user to create a new flashcard.
- **GET `/cards/{card_id}`**: Retrieves a specific card by its ID.
- **PUT `/cards/{card_id}`**: Updates a specific card by its ID.
- **DELETE `/cards/{card_id}`**: Deletes a specific card by its ID.
- **GET `/cards`**: Lists all cards for the logged-in user.

### 3. Batch Uploads

- **POST `/cards/upload`**: Allows uploading a spreadsheet to create multiple cards at once. The endpoint will handle parsing and data extraction.

### 4. Review Scheduling

- **POST `/reviews`**: Creates a new review schedule for a card.
- **GET `/reviews/{review_id}`**: Retrieves a specific review schedule by its ID.
- **PUT `/reviews/{review_id}`**: Updates a review schedule (e.g., after a review session to adjust the confidence level).
- **DELETE `/reviews/{review_id}`**: Deletes a specific review schedule.
- **GET `/reviews`**: Lists all review schedules for the logged-in user, possibly with filters for date ranges and confidence levels.

### 5. Cloud Storage Integration

- **POST `/upload/image`**: Endpoint for uploading an image to cloud storage, returns the URL.
- **POST `/upload/audio`**: Endpoint for uploading an audio file to cloud storage, returns the URL.

## 6. Cloud and Deployment Architecture

- **AWS Services**:
  - EC2: For hosting application services.
  - RDS: PostgreSQL for data persistence.
  - S3: For multimedia file storage.
  - Elastic Load Balancer: Considered for future scaling.
- **Containerization**: Docker used for packaging and deployment.
- **Deployment**: AWS Elastic Beanstalk for simplified application deployment and management.
- **CI/CD**:
  - **GitHub Actions**: Use for CI, running tests and builds directly from GitHub at no extra cost.
  - **AWS CodePipeline**: Use for the CD portion, automating deployment from GitHub to Elastic Beanstalk, staying within the Free Tier limits.

## 7. Security Considerations

- **Data Security**:
  - All data at rest in RDS is encrypted.
  - Data in transit secured using TLS.
- **API Security**:
  - Endpoints secured using JWT.
  - Rate limiting and input validation implemented to protect against common web threats.

## 8. Performance and Scalability

- **Database Optimization**:
  - Indexing critical fields to enhance query performance.
  - Connection pooling to manage database connections efficiently.
- **Caching**:
  - Application-level caching for frequently accessed data.
- **File Storage**:
  - Use of Standard-IA for cost-effective storage in S3.
  - Client-side caching for frequently accessed files.

## 9. Monitoring

- **AWS CloudWatch**: Used for monitoring application health and performance metrics.

## 10. Implementation Steps
### 1. Environment and Initial Setup
- **Local Development Environment**:
    - Install necessary tools: Docker, Python, Node.js, an IDE of your choice, and any other relevant development tools.
    - Set up a GitHub repository to manage the application's source code.
- **Docker Setup**:
    - Create Dockerfiles for both the backend (FastAPI) and frontend (React) parts of the application.
    - Develop docker-compose configurations to facilitate local development and testing of the microservices architecture, including services like databases or caches if required.

### 2. Backend Setup (FastAPI)
- **Develop the FastAPI Application**:
    - Implement API endpoints as per the API design.
    - Set up JWT-based authentication and integrate with the user database.
    - Write models and controllers for handling business logic and database interactions.
- **Containerize the Backend**:
  - Build and test the Docker container for the backend.
  - Ensure network configurations allow communication with the database and frontend.

### 3. Frontend Setup (React)
- **React Application Setup**:
  - Initialize the project using `create-react-app`.
  - Implement routing using `react-router`.
  - Develop responsive UI components that correspond to the application requirements.
- **Containerization**:
  - Build and test the Docker container for the frontend.
  - Ensure proper network settings for API communication.

### 4. Database Configuration (AWS RDS)
- **Set Up PostgreSQL on AWS RDS**:
    - Create and configure a new RDS instance via the AWS Management Console, ensuring it’s secure and accessible from your application environment.
    - Initialize the database using schema migrations set up in the backend application.

### 5. AWS S3 Configuration for File Storage
- **Create and Configure an S3 Bucket**:
    - Set up a new S3 bucket through the AWS Management Console for storing multimedia files securely.
    - Implement and test access policies and CORS settings to ensure secure and functional file uploads from the application.

### 6. Deployment Using AWS Elastic Beanstalk
- **Deploy the Application**:
    - Use Elastic Beanstalk's Docker environments to deploy both the backend and frontend containers.
    - Configure environment variables and manage application settings within Elastic Beanstalk for optimal performance and security.

### 7. CI/CD Pipeline Setup
- **Continuous Integration with GitHub Actions**:
  - Set up workflows in GitHub Actions to automate testing, building, and pushing Docker images upon new commits.
- **Continuous Deployment with AWS CodePipeline**:
  - Configure CodePipeline to fetch the latest Docker images and deploy them using Elastic Beanstalk.

### 8. Monitoring and Alerts
- **Set Up AWS CloudWatch**:
    - Configure monitoring for application performance and resource usage.
    - Set up alerts for any critical metrics that may indicate issues with application health or performance.

### 9. Testing and Validation
- **Conduct Thorough Testing**:
    - Implement unit tests, integration tests, and end-to-end tests to cover all aspects of the application.
    - Use staged deployments in Elastic Beanstalk to test the application in a production-like environment before full deployment.
