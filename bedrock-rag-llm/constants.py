from zenml import Model
from zenml.model.model import ModelStages

CLAUDE_3_HAIKU_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
CLAUDE_3_HAIKU_MODEL_ARN = (
    f"arn:aws:bedrock:us-east-1::foundation-model/{CLAUDE_3_HAIKU_MODEL_ID}"
)

AWS_SERVICE_CONNECTOR_ID = "0b04bcae-efc9-4044-a1c2-b86281cb0820"

AWS_REGION = "us-east-1"
AWS_CUSTOM_MODEL_ROLE_ARN = (
    "arn:aws:iam::339712793861:role/AmazonBedrockCustomizationRole1"
)
AWS_CUSTOM_MODEL_CUSTOMIZATION_TYPE = "CONTINUED_PRE_TRAINING"
AWS_CUSTOM_MODEL_BUCKET_NAME = "bedrock-zenml-rag-docs"
AWS_CUSTOM_MODEL_PRETRAINING_DATA_FILENAME = "pretraining_inputs.jsonl"
AWS_BEDROCK_KB_EXECUTION_ROLE_ARN = (
    "AmazonBedrockExecutionRoleForKnowledgeBase_392"
    # "AmazonBedrockExecutionRoleForKnowledgeBase_96gjm"
)


MODEL_DEFINITION = Model(
    name="aws-bedrock",
    description="Bedrock use cases for GenAI",
    audience="Anyone interested in using Bedrock for RAG",
    use_cases="Use this model to answer questions about Bedrock use cases for GenAI",
    limitations="The dataset is limited to ZenML documentation",
    trade_offs="Some parts of this model and project are experimental",
    tags=["bedrock", "rag", "genai", "llm", "aws"],
    version=ModelStages.LATEST,
)
