"""
Process Message Use Case - AI Chat Assistant
"""

import uuid
from typing import Dict, Any, List
from src.core.entities.chat_message import ChatMessage
from src.infrastructure.database.postgres_repository import ChatRepository


class ProcessMessageUseCase:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo
    
    async def execute(self, user_id: str, message: str) -> Dict[str, Any]:
        """Process user message and return AI response"""
        # Save user message
        user_msg = ChatMessage(
            id=str(uuid.uuid4()),
            user_id=user_id,
            role="user",
            content=message
        )
        await self.chat_repo.save_message(user_msg)
        
        # Generate response based on message content
        response_text = self._generate_response(message)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(message)
        
        # Save bot response
        bot_msg = ChatMessage(
            id=str(uuid.uuid4()),
            user_id=user_id,
            role="assistant",
            content=response_text
        )
        await self.chat_repo.save_message(bot_msg)
        
        return {
            "message": response_text,
            "suggestions": suggestions,
            "conversation_id": user_id  # Using user_id as conversation_id for simplicity
        }
    
    def _generate_response(self, message: str) -> str:
        """Generate AI response based on user message"""
        msg_lower = message.lower()
        
        if "create" in msg_lower and "workflow" in msg_lower:
            return """To create a workflow:

1. Go to the **Workflows** page
2. Click **New Workflow**
3. Give it a name and choose a trigger type (schedule, webhook, or event)
4. Add your actions (e.g., Send Slack message, Create Notion page)
5. Save and activate!

Would you like me to guide you through any specific step?"""
        
        elif "api key" in msg_lower or "openai" in msg_lower:
            return """To get an OpenAI API key:

1. Go to **platform.openai.com**
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create new secret key**
5. Copy and store it securely

⚠️ Never share your API key publicly!"""
        
        elif "slack" in msg_lower:
            return """To connect Slack:

1. Go to **Settings → Integrations**
2. Click **Connect** next to Slack
3. You'll need a Slack Bot Token (starts with `xoxb-`)
4. Create one at **api.slack.com/apps**
5. Paste the token and connect

Need help with a specific step?"""
        
        elif "github" in msg_lower:
            return """To connect GitHub:

1. Go to **Settings → Integrations**
2. Click **Connect** next to GitHub
3. Generate a **Personal Access Token** at github.com/settings/tokens
4. Required scopes: `repo`, `workflow`
5. Paste the token and connect

What would you like to automate with GitHub?"""
        
        elif "price" in msg_lower or "cost" in msg_lower or "plan" in msg_lower:
            return """**Pricing Plans:**

🆓 **Free**: 100 executions/month, 5 workflows
💎 **Pro**: $29/month - Unlimited executions, all integrations
🏢 **Enterprise**: Contact us for custom pricing

Which plan interests you?"""
        
        elif "help" in msg_lower or "how" in msg_lower:
            return """I can help you with:

- 🔧 **Creating workflows** - Step-by-step guidance
- 🔗 **Connecting integrations** - OpenAI, Slack, GitHub, etc.
- 🔑 **API keys** - Where to find and how to use
- ⏰ **Triggers** - Schedule, webhook, or event-based
- 💡 **Best practices** - Security and optimization tips

What would you like to know more about?"""
        
        else:
            return """I'm here to help with your Automatic Workflow questions!

I can assist with:
- Creating and managing workflows
- Setting up integrations
- API key management
- Troubleshooting issues

What would you like to do today?"""
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Generate suggested follow-up questions"""
        suggestions = [
            "How to create my first workflow?",
            "Connect OpenAI integration",
            "Set up a webhook trigger",
            "View pricing plans"
        ]
        
        msg_lower = message.lower()
        
        if "openai" in msg_lower or "api" in msg_lower:
            suggestions = [
                "How to create my first workflow?",
                "Connect Slack integration",
                "Best practices for API keys"
            ]
        elif "slack" in msg_lower or "github" in msg_lower:
            suggestions = [
                "Create a workflow with this integration",
                "Add another integration",
                "View all available integrations"
            ]
        
        return suggestions
