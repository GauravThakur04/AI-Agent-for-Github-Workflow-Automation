from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'AI Agent for GitHub Workflow Automation', ln=True, align='C')
pdf.ln(5)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 8, '''
Project Objective:
Develop an AI-powered agent that understands natural language queries and performs routine to medium-complexity GitHub operations autonomously, enabling non-technical users to interact with GitHub without knowing git commands or the GitHub UI.

---

Finalized Requirements:

Core Functionalities:
- Natural Language Query Processing (e.g., "Create a bug for login failure.", "What PRs are pending review this week?", etc.)
- GitHub Operations:
  - Read: Fetch issues, pull requests, comments, commits. Filter by labels, assignees, milestones, dates.
  - Write: Create issues, update issues, add comments/labels, assign users.
- Agent Responsibilities:
  - Interpret user intent using LLM (OpenAI GPT-4o/4.5)
  - Call appropriate GitHub API endpoints
  - Log actions and feedback
  - Handle errors or ambiguous inputs gracefully
- Technical Requirements:
  - Language: Python (backend), TypeScript/React (frontend)
  - AI/LLM: OpenAI GPT-4o/4.5 (or Azure OpenAI)
  - Agentic Framework: AutoGen (preferred), LangGraph
  - APIs: GitHub REST API / GraphQL API
  - UI: Web UI for user interaction

---

GitHub API Exploration:
- Authentication: Personal Access Token (PAT) with repo scope, stored in backend .env
- Key Endpoints:
  - List Issues: GET /repos/{owner}/{repo}/issues
  - Create Issue: POST /repos/{owner}/{repo}/issues
  - List PRs: GET /repos/{owner}/{repo}/pulls
  - Update Issue: PATCH /repos/{owner}/{repo}/issues/{issue_number}
  - Add Comment: POST /repos/{owner}/{repo}/issues/{issue_number}/comments
  - Assign Users: POST /repos/{owner}/{repo}/issues/{issue_number}/assignees
- Example (Python):
  import httpx
  token = "ghp_..."
  repo = "owner/repo"
  headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
  resp = httpx.get(f"https://api.github.com/repos/{repo}/issues", headers=headers)
  print(resp.json())

---

Backend API Design:
- POST /query
  - Body: { "query": "<natural language request>" }
  - Response: { "result": "...", "data": ... }
- How it works: Receives query, uses OpenAI to interpret, calls GitHub API, returns result.

---

Postman Environment:
- base_url = http://localhost:8000
- Example requests: Show all open issues, Create a bug issue, Show all pull requests

---

Setup Instructions:
Backend:
1. cd backend
2. python -m venv venv && venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
3. pip install -r requirements.txt
4. Create .env with:
   OPENAI_API_KEY=sk-...
   GITHUB_TOKEN=ghp_...
   GITHUB_REPO=owner/repo
5. uvicorn main:app --reload
Frontend:
1. npm install
2. npm run dev
3. Access at http://localhost:5173/
)

print('PDF generated: AI_Agent_GitHub_Workflow_Documentation.pdf')
