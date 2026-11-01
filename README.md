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
    └── secrets.toml   # APP_PASSWORD (not in the repo: create it locally)
```

## Prerequisites

- Python 3.10+
- An AWS account with access to **Llama 3.3 70B Instruct** in Amazon Bedrock, region `us-east-1`
- A Bedrock API key (see below)

### Bedrock API key

The app authenticates to Amazon Bedrock with a Bedrock API key. No keys are stored in this repo.

1. Sign in to the AWS console and open the **Amazon Bedrock** console in region **us-east-1**.
2. In the left menu, choose **API keys**, then the **Long-term API keys** tab.
3. Choose **Generate long-term API keys**, select an expiration (30 days is fine for testing), and generate the key.
4. Copy the key and keep it private. Never commit it or paste it into code.
5. Set it as an environment variable in the terminal you'll run the app from:
   - **Windows (PowerShell, this session only):**
     ```powershell
     $env:AWS_BEARER_TOKEN_BEDROCK = "your-key"
     ```
   - **Windows (saved for future sessions):** run `setx AWS_BEARER_TOKEN_BEDROCK "your-key"`, then open a new terminal.
   - **macOS/Linux:** `export AWS_BEARER_TOKEN_BEDROCK="your-key"`
6. Make sure Llama 3.3 70B Instruct is enabled under Bedrock model access for `us-east-1`.

Long-term keys expire and are for exploration. For a longer-lived deployment, use short-term keys or IAM roles instead. If a key is ever exposed, deactivate or delete it in the Bedrock console.

## Setup

```bash
pip install strands-agents streamlit boto3
```

Create `.streamlit/secrets.toml`:

```toml
APP_PASSWORD = "your-password-here"
```

Make sure `.streamlit/` is listed in `.gitignore` so the password is never committed.

## Running the app

```bash
streamlit run app.py
```

Enter the password, describe your idea, and click **Evaluate Idea**.

## Configuration

- **Model:** `us.meta.llama3-3-70b-instruct-v1:0` in `agents.py`
- **Region:** `us-east-1`, set via `AWS_DEFAULT_REGION` in `agents.py`
- **Logging:** INFO-level logs are printed to stdout

## Known limitations

- The VC agent is asked for JSON, but the model may not always return valid JSON. The output is displayed as-is.
- Errors during evaluation are returned as text and shown in the output area.
- The password check is a simple shared password, not user accounts. Don't rely on it for sensitive data.
- Results are estimates from an LLM, not financial advice.

## License

Add your license here.
