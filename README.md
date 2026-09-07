# AI Email Analyzer API

A production-grade FastAPI backend integrated with Google Gemini AI for automated email analysis, categorization, priority tagging, sentiment analysis, and token tracking backed by PostgreSQL.

## 🚀 Tech Stack
- **Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL, SQLAlchemy, Alembic
- **AI Integration:** Google Gemini API (`gemini-2.5-flash`)
- **Validation:** Pydantic v2
- **Testing:** Pytest
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions

## 📋 Core Features
- **Authentication:** JWT-based secure user registration and login.
- **Email CRUD:** Create, read, delete, and filter emails by category, priority, and sentiment.
- **AI Analysis:** Automated analysis extracting category, priority, sentiment, intent, summary, and key information.
- **Token & Cost Tracking:** Monitors API token consumption per analysis.
- **Dashboard Stats:** Comprehensive statistics on email volumes, priority breakdowns, and category distribution.
- **Resilience:** Exponential backoff retry logic for handling API rate limits (`429`).

## 🛠️ Local Development & Docker Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Almas-Web/ai-email-analyzer-api.git](https://github.com/Almas-Web/ai-email-analyzer-api.git)
   cd ai-email-analyzer-api