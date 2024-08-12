from enum import StrEnum

from community.tools import (
    ArxivRetriever,
    Category,
    ClinicalTrials,
    ConnectorRetriever,
    LlamaIndexUploadPDFRetriever,
    ManagedTool,
    PubMedRetriever,
    WolframAlpha,
    LoanRefinanceCalculator
)


class CommunityToolName(StrEnum):
    Arxiv = ArxivRetriever.NAME
    Connector = ConnectorRetriever.NAME
    Pub_Med = PubMedRetriever.NAME
    File_Upload_LlamaIndex = LlamaIndexUploadPDFRetriever.NAME
    Wolfram_Alpha = WolframAlpha.NAME
    ClinicalTrials = ClinicalTrials.NAME
    LoanRefinanceCalculator = LoanRefinanceCalculator.NAME


COMMUNITY_TOOLS = {
    CommunityToolName.Arxiv: ManagedTool(
        display_name="Arxiv",
        implementation=ArxivRetriever,
        parameter_definitions={
            "query": {
                "description": "Query for retrieval.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=ArxivRetriever.is_available(),
        error_message="ArxivRetriever is not available.",
        category=Category.DataLoader,
        description="Retrieves documents from Arxiv.",
    ),
    CommunityToolName.Connector: ManagedTool(
        display_name="Example Connector",
        implementation=ConnectorRetriever,
        is_visible=True,
        is_available=ConnectorRetriever.is_available(),
        error_message="ConnectorRetriever is not available.",
        category=Category.DataLoader,
        description="Connects to a data source.",
    ),
    CommunityToolName.Pub_Med: ManagedTool(
        display_name="PubMed",
        implementation=PubMedRetriever,
        parameter_definitions={
            "query": {
                "description": "Query for retrieval.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=PubMedRetriever.is_available(),
        error_message="PubMedRetriever is not available.",
        category=Category.DataLoader,
        description="Retrieves documents from Pub Med.",
    ),
    CommunityToolName.File_Upload_LlamaIndex: ManagedTool(
        display_name="File Reader",
        implementation=LlamaIndexUploadPDFRetriever,
        is_visible=True,
        is_available=LlamaIndexUploadPDFRetriever.is_available(),
        error_message="LlamaIndexUploadPDFRetriever is not available.",
        category=Category.FileLoader,
        description="Retrieves documents from a file using LlamaIndex.",
    ),
    CommunityToolName.Wolfram_Alpha: ManagedTool(
        display_name="Wolfram Alpha",
        implementation=WolframAlpha,
        is_visible=False,
        is_available=WolframAlpha.is_available(),
        error_message="WolframAlphaFunctionTool is not available, please set the WOLFRAM_APP_ID environment variable.",
        category=Category.Function,
        description="Evaluate arithmetic expressions.",
    ),
    CommunityToolName.ClinicalTrials: ManagedTool(
        display_name="Clinical Trials",
        implementation=ClinicalTrials,
        is_visible=True,
        is_available=ClinicalTrials.is_available(),
        error_message="ClinicalTrialsTool is not available.",
        category=Category.Function,
        description="Retrieves clinical studies from ClinicalTrials.gov.",
        parameter_definitions={
            "condition": {
                "description": "Filters clinical studies to a specified disease or condition",
                "type": "str",
                "required": False,
            },
            "location": {
                "description": "Filters clinical studies to a specified city, state, or country.",
                "type": "str",
                "required": False,
            },
            "intervention": {
                "description": "Filters clinical studies to a specified drug or treatment.",
                "type": "str",
                "required": False,
            },
            "is_recruiting": {
                "description": "Filters clinical studies to those that are actively recruiting.",
                "type": "bool",
                "required": False,
            },
        },
    ),
CommunityToolName.LoanRefinanceCalculator: ManagedTool(
    display_name="Loan Refinance Calculator",
    implementation=LoanRefinanceCalculator,
    parameter_definitions={
        "original_loan_amount": {
            "description": "The original amount of the loan in dollars.",
            "type": "int",
            "required": True,
        },
        "original_term": {
            "description": "The original term of the loan in years.",
            "type": "int",
            "required": True,
        },
        "years_paid": {
            "description": "The number of years already paid on the original loan.",
            "type": "int",
            "required": True,
        },
        "original_interest_rate": {
            "description": "The original interest rate of the loan as a percentage.",
            "type": "float",
            "required": True,
        },
        "refi_term": {
            "description": "The term of the refinanced loan in years.",
            "type": "int",
            "required": True,
        },
        "refi_interest_rate": {
            "description": "The interest rate of the refinanced loan as a percentage.",
            "type": "float",
            "required": True,
        },
        "closing_costs_percent": {
            "description": "The closing costs as a percentage of the new loan amount.",
            "type": "float",
            "required": True,
        },
        "finance_closing_costs": {
            "description": "Whether to finance the closing costs in the new loan amount.",
            "type": "bool",
            "required": True,
        },
        "cash_out_amount": {
            "description": "The amount of cash to be taken out in the refinance, in dollars.",
            "type": "int",
            "required": True,
        },
    },
    is_visible=True,
    is_available=LoanRefinanceCalculator.is_available(),
    error_message="Loan Refinance Calculator tool not available.",
    category=Category.Function,
    description="This tool calculates loan refinancing options based on current loan details and refinancing parameters. If the full parameters are not given you MUST ASK FOR THEM! Only ask for the parameters in the description.",
),
}

# For main.py cli setup script
COMMUNITY_TOOLS_SETUP = {
    CommunityToolName.Wolfram_Alpha: {
        "secrets": {
            "WOLFRAM_APP_ID": None,  # default value
        },
    },
}
