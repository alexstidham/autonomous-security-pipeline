# RepoSentry - Autonomous Multimodal Security Pipeline

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

Follow these steps to run the autonomous auditing and patching pipeline locally in an isolated sandbox.

### 1. Prerequisites & Environment Setup
Clone the repository, create an environment file to store your credentials, and configure your local pathing:

```bash
git clone https://github.com/alexstidham/autonomous-security-pipeline.git
cd autonomous-security-pipeline
touch .env
```
Open `.env` and add your OpenAI API key and the MLflow local network route:
```env
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
MLFLOW_TRACKING_URI=http://host.docker.internal:8080
```

### 2. Launch the MLflow Telemetry Server
Before spinning up the container ecosystem, install MLflow and start the tracking server on your host machine so the container can stream execution telemetry to it:
```bash
pip install mlflow
mlflow server --host 0.0.0.0 --port 8080
```
_The visualization dashboard will be live at http://localhost:8080._

### 3. Build and Run the Docker Sandbox
Build the isolated environment image. This packages your FastAPI app and LangGraph state engine inside a secure container sandbox. We use a volume mount (-v) to give the container temporary, restricted access to the target repository you want to scan.
```bash
# Build the production image
docker build -t reposentry-pipeline:latest .

# Spin up the container sandbox, mapping port 8000 and mounting your target local repository
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  -v /path/to/your/local/target/repo:/app/target_repo \
  --name reposentry-agent-container \
  reposentry-pipeline:latest
```
## ⚡ Triggering an Autonomous Audit
Once the container is healthy and running on port 8000, you can dispatch the pipeline using a standard network payload from your host machine.

### Execution Payload

Execute this `curl` command from your host terminal to trigger the LangGraph orchestration loop over your volume-mounted target repository:

```bash
curl -X POST "http://localhost:8000/api/v1/audit" \
     -H "Content-Type: application/json" \
     -d '{
       "repo_path": "/app/target_repo",
       "architecture_diagram_path": "/app/target_repo/docs/arch_diagram.png",
       "auto_patch": true
     }'
```

### What Happens Behind the Scenes:
1. **FastAPI Gateway** captures the request asynchronously and instantiates the graph runtime memory.
2. **Auditor Agent** evaluates the raw code blocks alongside your system's `arch_diagram.png` file to check for physical layout vs. code standard drift.
3. If an OWASP exposure is flagged, the graph routes the file context to the Patch Agent, which updates the target code inside the Docker volume mount sandbox.
4. The pipeline routes changes to an internal Validator Node to lint/test the code. If it catches a compiler break, the state loops backwards into the Patch node automatically to self-correct.
5. All execution trace branches, latency metrics, and API token counts are streamed live to your host ** MLflow ** dashboard.
