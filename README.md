# Autonomous Multimodal Security Pipeline

An enterprise-grade, containerized AI agent architecture built to automatically analyze software repositories for security vulnerabilities, cross-reference them with system architecture diagrams, execute automated patches, and log production telemetry.

## 🏗️ System Architecture

This project is built as a microservice framework that separates execution environments from logging and user interaction.

### The Factory Blueprint
┌────────────────────────────────────────────────────────────────────────┐
│                              LOCAL MACHINE                             │
│                                                                        │
│  1. THE CLIENT (Trigger)     2. THE FACTORY (Docker Container)          │
│   ┌─────────────────┐         ┌─────────────────────────────────────┐  │
│   │  curl Command   ├────────►│  FastAPI Gateway (The Front Desk)   │  │
│   └─────────────────┘         └──────────────────┬──────────────────┘  │
│                                                  │                     │
│                                       LangGraph Orchestrator           │
│                                                  │                     │
│                                                  ▼                     │
│                               ┌─────────────────────────────────────┐  │
│                               │  Auditor Agent (Finds the flaw)     │  │
│                               └──────────────────┬──────────────────┘  │
│                                                  │                     │
│                                                  ▼                     │
│                               ┌─────────────────────────────────────┐  │
│                               │  Patch Agent (Fixes the code)       │  │
│                               └──────────────────┬──────────────────┘  │
│                                                  │                     │
│                                                  ▼                     │
│  3. THE MANAGER (Dashboard)   ┌─────────────────────────────────────┐  │
│   ┌─────────────────┐         │  OpenAI API (The AI Brainpower)     │  │
│   │  MLflow Server  │◄────────┤                                     │  │
│   └─────────────────┘         └─────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
1. **The Client Trigger (`curl`):** Initiates a secure payload request over the network bridge with target directory details and structural system assets.
2. **The App Factory (Docker Sandbox):** Houses a **FastAPI** web framework running an isolated **LangGraph** workflow.
   * **Auditor Agent:** Scans raw code repositories and utilizes multimodal vision LLMs to compare code against the system's structural architecture diagram.
   * **Patch Agent:** Automatically rewrites files to apply secure software updates based on vulnerabilities discovered during auditing.
3. **The Supervisor Dashboard (MLflow):** An independent telemetry engine monitoring operational efficiency, execution runtime, token consumption metrics, and agentic decision states.

---

## 🛠️ Tech Stack & Engineering Tooling
* **Framework Core:** Python 3.12, FastAPI, Pydantic v2
* **Agent Orchestration:** LangGraph (Stateful multi-agent runtimes)
* **AI Engine:** OpenAI API (`gpt-4o-mini` / multimodal capabilities)
* **DevOps & Containerization:** Docker (Isolated Linux Alpine/Slim baseline environment)
* **Observability & MLOps:** MLflow Tracking (Telemetry and metric capture)

---

## 🚀 Quick Start & Deployment Sequence

### 1. Initialize the MLflow Telemetry Server
Launch the supervisor tracking dashboard natively on your local environment loop:
```bash
mlflow server --host 0.0.0.0 --port 8080
