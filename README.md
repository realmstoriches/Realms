# Agentic Swarm Workforce Engine: Project Jules

Welcome to Project Jules, a production-grade, modular agentic swarm system designed to automate complex business workflows, from marketing and sales to financial analysis and legal drafting. This system is built on a "Tri-Hemisphere" agent architecture and is designed to be scalable, intelligent, and eventually, interactive through a live UI.

## Table of Contents
1.  [Project Architecture](#project-architecture)
2.  [The Agentic Workforce](#the-agentic-workforce)
3.  [Getting Started: Setup & Configuration](#getting-started-setup--configuration)
4.  [How to Run the System](#how-to-run-the-system)
5.  [Key Features](#key-features)
6.  [Future Development](#future-development)

---

## Project Architecture

The system is built on a modular Python backend with a clear separation of concerns:

-   `main.py`: The central orchestrator that simulates a "9 AM SHARP" daily workflow, activating various agent crews to perform their tasks in sequence.
-   `src/`: Contains the core logic for the application.
    -   `agent.py`: Defines the foundational Tri-Hemisphere agent architecture.
    -   `company.py`: Defines the organizational chart, including all agent roles and their skills.
    -   `knowledge.py`: Manages the ChromaDB knowledge bases for the agents.
    -   `ingestion.py`: Handles the ingestion of data, from raw product lists to brand voice text.
    -   `tasks.py`: Contains the logic for specific agent tasks like content generation and social media posting.
    -   `business_logic.py`: Contains tasks for the Business Advisory crew, such as generating financial and legal documents.
    -   `social/`: Placeholder modules for interacting with social media APIs.
    -   `integrations/`: Modules for connecting to external services like Shopify.
    -   `payments.py`: Placeholder module for Stripe integration.
    -   `throttling.py`: A smart rate-limiter to ensure safe and reliable API usage.
-   `scripts/`: Contains utility scripts for setup, validation, and data parsing.
-   `data/`: Contains raw data for ingestion.
-   `products/`: The destination for structured, parsed product data.
-   `knowledge/`: Contains text files used to "teach" the agents (e.g., brand voice, marketing principles).
-   `output/`: The destination for simulated social media posts.
-   `logs/`: Contains performance logs for the learning mechanism.
-   `tests/`: A comprehensive suite of unit tests.

---

## The Agentic Workforce

Our workforce is composed of specialized agents, each with a defined role and set of skills.

### Marketing Crew
-   **Campaign Strategist:** Designs high-level, multi-platform marketing campaigns.
-   **Marketing Content Creator:** Generates engaging social media copy based on the strategist's plan.
-   **Social Media Manager:** Executes the posting of content across all platforms in parallel.

### Business Advisory Crew
-   **CFO Agent:** Generates financial projections and business valuations.
-   **Legal Counsel Agent:** Drafts standard legal documents, like a Founders' Agreement.
-   **Market Analyst Agent:** Develops detailed target audience personas and anti-personas.

---

## Getting Started: Setup & Configuration

### 1. Installation

Clone the repository and install the required Python dependencies:

```bash
git clone <repository_url>
cd agentic-swarm-workforce
pip install -r requirements.txt
```

### 2. Credential Management

This system requires API credentials for various social media platforms and services. We use a `.env` file to handle these securely.

**Automated Setup (Recommended):**

Run the interactive setup script. It will prompt you for each required key and create the `.env` file for you.

```bash
python3 scripts/setup_credentials.py
```

**Manual Setup:**

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file in a text editor and replace the placeholder values with your actual API keys and secrets.

**Validating Your Credentials:**

After setting up your `.env` file, you can run the validation script to check for missing keys and test the authentication for each service:

```bash
python3 scripts/validate_credentials.py
```

**Finding Your Keys (Tool Signup Links):**

If you don't have developer accounts for the required platforms, run this script to get a list of direct links to their developer portals:

```bash
python3 scripts/get_tool_signup_links.py
```

---

## How to Run the System

To fire up the beast and run the complete, end-to-end daily workflow, simply execute the main script from the root of the project:

```bash
python3 main.py
```

This will trigger the full sequence:
1.  **9 AM Role Call:** The system will announce the start of the day.
2.  **Data Ingestion:** It will parse the product catalog.
3.  **Campaign Strategy:** The Campaign Strategist will design a marketing plan.
4.  **Content Creation:** The Content Creator will generate social media posts.
5.  **Payment Link Generation:** A Stripe payment link will be created for the product.
6.  **Social Media Posting:** The Social Media Manager will post the content in parallel to all configured platforms (writing to `output/` files for now).
7.  **Founder's Packet Generation:** The Business Advisory crew will generate the valuation, legal docs, and pitch deck outline.

---

## Key Features

-   **Autonomous Agent Swarm:** A multi-agent system where specialized agents collaborate to achieve complex business objectives.
-   **"Wow Feature" - Founder's Packet:** The Business Advisory crew can generate a complete set of strategic documents on demand.
-   **Self-Refining Campaigns:** A simple learning mechanism allows the Campaign Strategist to review past performance and adjust its strategy.
-   **Robust Credential Management:** Securely handles API keys and provides tools for easy setup and validation.
-   **Rate Limiting:** A smart throttling engine ensures the system operates safely within the API limits of all platforms.
-   **Comprehensive Testing:** The entire system is covered by a suite of unit tests to ensure reliability.

---

## Future Development

-   **Full OAuth2 Integration:** Implement the `docs/OAUTH_FLOW.md` blueprint to create a user-friendly, secure authentication system.
-   **Live Web Dashboard:** Develop the `dashboard/whiteboard.html` into a live, interactive 3D interface powered by the `app/` Flask server.
-   **Real API Integration:** Replace the placeholder functions in the `src/social/`, `src/integrations/`, and `src/payments/` modules with real API calls.
-   **Advanced Learning:** Enhance the learning mechanism to use more sophisticated analysis of performance metrics.