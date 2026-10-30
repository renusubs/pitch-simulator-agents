# AI Startup Idea Validator

A Streamlit app that evaluates a startup idea with a team of AI agents running on Amazon Bedrock. A lead orchestrator sends the idea through three specialist agents in turn: a market analyst, a financial modeler, and a skeptical venture capitalist. The result is an investor-style memo.

Powered by AWS Bedrock, Llama 3.3 70B, and the Strands Agents SDK.

## How it works

1. The user describes a business idea in the web app.
2. The **Market Analyst** identifies competitors, estimates market size, and names two key differentiators.
3. The **Financial Modeler** estimates unit economics, platform take rate, and Year 1 GMV, using the market analysis.
4. The **VC Partner** identifies the top three risks, scores total risk from 1 to 10, and returns a structured JSON evaluation.

The specialists are attached to the orchestrator as tools ("agents as tools"), so the orchestrator decides when to call each one.

## Project structure

```
.
├── agents.py          # Model setup, specialist agents, orchestrator, run_evaluation()
├── app.py             # Streamlit UI with password gate
└── .streamlit/
    └── secrets.toml   # APP_PASSWORD (not committed)
```

## Prerequisites

- Python 3.10+
- An AWS account with access to **Llama 3.3 70B Instruct** in Amazon Bedrock, region `us-east-1`
- AWS credentials configured locally (for example, via `aws configure`)

## Setup

```bash
pip install strands-agents streamlit boto3
```

Create `.streamlit/secrets.toml`:

```toml
APP_PASSWORD = "your-password-here"
```

Add this file to `.gitignore` so the password is never committed.

## Running the app

```bash
streamlit run app.py
```

Enter the password, describe your idea, and click **Evaluate Idea**.

## Configuration

- **Model:** `us.meta.llama3-3-70b-instruct-v1:0` in `agents.py`
- **Region:** set to `us-east-1` via `AWS_DEFAULT_REGION` in `agents.py`
- **Logging:** INFO-level logs are printed to stdout

## Known limitations

- The VC agent is asked for JSON, but the model may not always return valid JSON. The output is displayed as-is.
- Errors during evaluation are returned as text and shown in the output area.
- `st.set_page_config()` should be the first Streamlit call in `app.py`. It currently runs after `st.title()`, which Streamlit will reject. Move it to the top of the file.
- The password check is a simple shared password, not user accounts. Don't rely on it for sensitive data.
- Results are estimates from an LLM, not financial advice.

## License

Add your license here.
