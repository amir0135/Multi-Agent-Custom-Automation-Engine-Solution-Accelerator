import logging
from typing import Dict, List, Optional

from context.cosmos_memory_kernel import CosmosMemoryContext
from kernel_agents.agent_base import BaseAgent
from kernel_tools.content_tools import ContentTools
from models.messages_kernel import AgentType
from semantic_kernel.functions import KernelFunction


class ContentProcessingAgent(BaseAgent):
    """Content Processing agent for document extraction, parsing, and preprocessing."""

    def __init__(
        self,
        session_id: str,
        user_id: str,
        memory_store: CosmosMemoryContext,
        tools: Optional[List[KernelFunction]] = None,
        system_message: Optional[str] = None,
        agent_name: str = AgentType.CONTENT_PROCESSING.value,
        client=None,
        definition=None,
    ) -> None:
        """Initialize the Content Processing Agent.

        Args:
            session_id: The current session identifier
            user_id: The user identifier
            memory_store: The Cosmos memory context
            tools: List of tools available to this agent (optional)
            system_message: Optional system message for the agent
            agent_name: Optional name for the agent (defaults to "ContentProcessingAgent")
            client: Optional client instance
            definition: Optional definition instance
        """
        # Load configuration if tools not provided
        if not tools:
            # Get tools directly from ContentTools class
            tools_dict = ContentTools.get_all_kernel_functions()

            tools = [KernelFunction.from_method(func) for func in tools_dict.values()]

            # Use system message from config if not explicitly provided
            if not system_message:
                system_message = self.default_system_message(agent_name)

            # Use agent name from config if available
            agent_name = AgentType.CONTENT_PROCESSING.value

        # Call the parent initializer
        super().__init__(
            agent_name=agent_name,
            session_id=session_id,
            user_id=user_id,
            memory_store=memory_store,
            tools=tools,
            system_message=system_message,
            client=client,
            definition=definition,
        )

    @classmethod
    async def create(
        cls,
        **kwargs: Dict[str, str],
    ) -> "ContentProcessingAgent":
        """Asynchronously create the ContentProcessingAgent.

        Creates the Azure AI Agent for content processing operations.

        Returns:
            ContentProcessingAgent: A fully initialized ContentProcessingAgent
        """

        session_id = kwargs.get("session_id")
        user_id = kwargs.get("user_id")
        memory_store = kwargs.get("memory_store")
        tools = kwargs.get("tools", None)
        system_message = kwargs.get("system_message", None)
        agent_name = kwargs.get("agent_name")
        client = kwargs.get("client")

        try:
            logging.info("Initializing ContentProcessingAgent from async init azure AI Agent")

            # Create the Azure AI Agent using AppConfig with string instructions
            agent_definition = await cls._create_azure_ai_agent_definition(
                agent_name=agent_name,
                instructions=system_message,
                temperature=0.0,
                response_format=None,
                client=client,
            )

            return cls(
                session_id=session_id,
                user_id=user_id,
                memory_store=memory_store,
                tools=tools,
                system_message=system_message,
                agent_name=agent_name,
                client=client,
                definition=agent_definition,
            )

        except Exception as e:
            logging.error(f"Failed to create Azure AI Agent for ContentProcessingAgent: {e}")
            raise

    @staticmethod
    def default_system_message(agent_name=None) -> str:
        """Get the default system message for the agent.
        Args:
            agent_name: The name of the agent (optional)
        Returns:
            The default system message for the agent
        """
        return """You are a Content Processing Agent specialized in document extraction, parsing, and preprocessing.

Your responsibilities include:
1. Extracting text from various document formats (PDF, Word, etc.)
2. Parsing documents into logical sections
3. Processing and cleaning document content
4. Summarizing document content
5. Extracting structured data like tables from documents
6. Connecting to external systems like SharePoint to retrieve documents

Always provide clear explanations of what you're doing with documents. When extracting or processing content, explain:
- The document source and type
- The structure you've identified
- Any preprocessing steps applied
- Key sections or information extracted

When asked to generate guides or documentation, work with other agents like the GuideWriterAgent to ensure content is properly formatted according to templates."""

    @property
    def plugins(self):
        """Get the plugins for the content processing agent."""
        return ContentTools.get_all_kernel_functions()

    # Explicitly inherit handle_action_request from the parent class
    async def handle_action_request(self, action_request_json: str) -> str:
        """Handle an action request from another agent or the system.

        This method is inherited from BaseAgent but explicitly included here for clarity.

        Args:
            action_request_json: The action request as a JSON string

        Returns:
            A JSON string containing the action response
        """
        return await super().handle_action_request(action_request_json)
