import sys
import os
import logging

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

from strands import Agent, Orchestrator
from strands.models import BedrockModel

print("-> Initializing Llama 3.3 70B model configuration...")
model = BedrockModel(
    model_id="us.meta.llama3-3-70b-instruct-v1:0",
    streaming=False
)

print("-> Initializing Specialized Agents...")

# 1. Market Analyst Agent
market_agent = Agent(
    name="MarketAnalyst",
    model=model,
    system_prompt=(
        "You are an expert Market Research Analyst. Your job is to analyze competitors, "
        "target market size, and identify 2 key differentiators for the given startup idea."
    )
)

# 2. Financial Modeler Agent
financial_agent = Agent(
    name="FinancialModeler",
    model=model,
    system_prompt=(
        "You are a startup CFO and Financial Modeler. Using the market analysis provided, "
        "estimate unit economics, platform take rate (%), and Year 1 GMV."
    )
)

# 3. VC Risk Evaluation Agent
vc_agent = Agent(
    name="VCPartner",
    model=model,
    system_prompt=(
        "You are a cynical, pattern-matching Tier-1 Venture Capitalist. Using the market and financial data, "
        "identify the top 3 critical risks, score total risk from 1 to 10, and output "
        "the final comprehensive evaluation in a clean, structured JSON format."
    )
)

# Set up the Orchestrator as a Sequential Pipeline
evaluation_pipeline = Orchestrator(
    mode="sequential",
    agents=[market_agent, financial_agent, vc_agent],
    supervisor_prompt=(
        "Coordinate the startup evaluation pipeline across the team:\n"
        "1. Pass the startup idea to MarketAnalyst for the market and competitor breakdown.\n"
        "2. Pass the market results to FinancialModeler to construct unit economics and projections.\n"
        "3. Pass both market and financial insights to VCPartner for final risk analysis and JSON output formatting."
    )
)

def run_evaluation(business_idea: str):
    """Function called by Streamlit to evaluate any dynamic idea."""
    try:
        logger.info(f"Running multi-agent evaluation for: {business_idea}")
        result = evaluation_pipeline.run(input=f"Evaluate startup idea: {business_idea}")
        return result
    except Exception as e:
        logger.error(f"Error during evaluation: {e}")
        return f"Error during evaluation: {e}"
EOF