# Postman Setup Guide for GitHub AI Agent

This guide will help you set up Postman to test and interact with the GitHub AI Agent APIs.

## Prerequisites

1.  **Download and Install Postman**: If you haven't already, download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/).
2.  **Start the Backend Server**: Ensure your backend server is running.
    *   Open a terminal in the `project/backend` directory.
    *   Run `uvicorn main:app --reload` (or the command you usually use to start the server).
    *   The server should be running at `http://localhost:8000`.

---

## Method 1: Import Existing Collection (Recommended)

The easiest way to set up the APIs is to import the pre-configured collection file included in the project.

1.  Open Postman.
2.  Click on the **"Import"** button in the top left corner.
3.  Drag and drop the file `github-ai-agent-bug-analytics.postman_collection.json` from your project folder into the Import window.
    *   *Location:* `project/github-ai-agent-bug-analytics.postman_collection.json`
4.  Click **"Import"**.

You should now see a collection named **"GitHub AI Agent API For Bug Analytics"** in your Collections sidebar. It contains all the necessary requests organized by functionality.

### Using the Collection

The collection comes with a `base_url` variable set to `http://localhost:8000`.

1.  **Register/Login**: Start with the **Register User** or **Login User** request to get a session.
2.  **Session ID**: Most endpoints require a `session_id`.
    *   After logging in, copy the `session_id` from the response.
    *   You can set this as a collection variable:
        *   Click on the collection name **"GitHub AI Agent API For Bug Analytics"**.
        *   Go to the **"Variables"** tab.
        *   Paste the session ID into the `current value` for the `session_id` variable.
        *   Click **"Save"**.
    *   Now all requests using `{{session_id}}` will automatically use your logged-in session.

---

## Method 2: Manual Setup

If you prefer to set up the requests manually, follow these steps for the key endpoints.

### 1. Create a Collection
1.  Click **"New"** > **"Collection"**.
2.  Name it "GitHub AI Agent".

### 2. Add Requests

Here are the details for the essential API endpoints.

#### A. Health Check
*   **Method**: `GET`
*   **URL**: `http://localhost:8000/health`
*   **Description**: Checks if the server is running.

#### B. Register User
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/register`
*   **Headers**: `Content-Type: application/json`
*   **Body** (JSON):
    ```json
    {
      "username": "your_username",
      "email": "your_email@example.com",
      "password": "your_password",
      "github_url": "https://github.com/your/repo"
    }
    ```

#### C. Login User
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/login`
*   **Headers**: `Content-Type: application/json`
*   **Body** (JSON):
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
    *   **Note**: Save the `session_id` from the response for subsequent requests.

#### D. Chat with AI
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/chat`
*   **Headers**: `Content-Type: application/json`
*   **Body** (JSON):
    ```json
    {
      "message": "Show me all open bugs",
      "session_id": "YOUR_SESSION_ID_HERE"
    }
    ```

#### E. Create Bug
*   **Method**: `POST`
*   **URL**: `http://localhost:8000/bugs/create?session_id=YOUR_SESSION_ID_HERE`
*   **Headers**: `Content-Type: application/json`
*   **Body** (JSON):
    ```json
    {
      "title": "Bug Title",
      "description": "Bug Description",
      "bug_type": "ui_ux",
      "priority": 2,
      "assignees": ["dev1"]
    }
    ```

#### F. List Bugs
*   **Method**: `GET`
*   **URL**: `http://localhost:8000/bugs/list?session_id=YOUR_SESSION_ID_HERE&status=open`

---

## Troubleshooting

*   **Connection Refused**: Make sure your backend server is running on port 8000.
*   **401 Unauthorized**: Ensure you are providing a valid `session_id` in the request body or query parameters as required.
