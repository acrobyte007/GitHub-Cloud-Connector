# GitHub API Integration with FastAPI

This project provides a FastAPI backend for interacting with the GitHub API. It allows you to:

- Exchange OAuth codes for GitHub access tokens.
- Fetch user information.
- Retrieve repositories, issues, and commits.
- Create GitHub issues and pull requests.

---

## 📦 Features

- **OAuth Token Exchange** – Convert GitHub authorization codes into access tokens.
- **User Data** – Fetch authenticated user information.
- **Repositories** – List repositories of the authenticated user.
- **Issues** – Retrieve and create issues.
- **Pull Requests** – Create pull requests.
- **Commits** – Fetch commits for a repository.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/acrobyte007/GitHub-Cloud-Connector
cd GitHub-Cloud-Connector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your GitHub OAuth client ID and secret:
```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=client_secret
```

### 3. Run the Application
```bash
uvicorn main:app --reload --port 8000
```


# GitHub API Endpoints

| Method | Path                              | Headers                          | Request Body                                      | Description                                      |
|--------|-----------------------------------|----------------------------------|---------------------------------------------------|--------------------------------------------------|
| POST   | `/auth/token`                     | None                             | `{ "code": "<oauth_code>" }`                      | Exchange GitHub OAuth code for access token      |
| GET    | `/user`                           | `Authorization: Bearer <token>`  | None                                              | Get authenticated GitHub user info               |
| GET    | `/repos`                          | `Authorization: Bearer <token>`  | None                                              | List repositories of authenticated user          |
| GET    | `/repos/{owner}/{repo}/issues`    | `Authorization: Bearer <token>`  | None                                              | Get issues for a repository                      |
| POST   | `/repos/{owner}/{repo}/issues`    | `Authorization: Bearer <token>`  | `{ "title": "Issue title", "body": "Issue description" }` | Create a new issue                  |
| POST   | `/repos/{owner}/{repo}/pulls`     | `Authorization: Bearer <token>`  | `{ "title": "PR title", "head": "feature-branch", "base": "main", "body": "PR description" }` | Create a pull request |
| GET    | `/repos/{owner}/{repo}/commits`   | `Authorization: Bearer <token>`  | None                                              | List commits of a repository                     |

             |
