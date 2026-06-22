"""
Execute Workflow Use Case
"""

from typing import Dict, Any, Optional
from src.core.entities.workflow import Workflow


class ExecuteWorkflowUseCase:
    def __init__(self):
        self.service_handlers = {}
    
    async def execute(
        self, 
        workflow: Workflow, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a workflow"""
        try:
            # Execute each action in order
            results = []
            for action in workflow.actions:
                result = await self._execute_action(action, parameters)
                results.append(result)
                
                # If action fails, stop execution
                if not result.get("success", False):
                    return {
                        "success": False,
                        "message": f"Action '{action.action}' failed",
                        "results": results
                    }
            
            return {
                "success": True,
                "message": "Workflow executed successfully",
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Workflow execution failed: {str(e)}",
                "results": []
            }
    
    async def _execute_action(self, action, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a single action"""
        # Get service handler
        handler = self._get_handler(action.service)
        
        if handler is None:
            return {
                "success": False,
                "message": f"Service '{action.service}' not supported"
            }
        
        try:
            result = await handler.execute(action.action, action.parameters, parameters)
            return {
                "success": True,
                "service": action.service,
                "action": action.action,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "service": action.service,
                "action": action.action,
                "error": str(e)
            }
    
    def _get_handler(self, service: str):
        """Get service handler"""
        if service in self.service_handlers:
            return self.service_handlers[service]
        
        # Lazy load handlers
        from src.infrastructure.external_apis import (
            OpenAIClient,
            SlackClient,
            DiscordClient,
            GitHubClient,
            NotionClient,
            GoogleClient
        )
        
        handlers = {
            "openai": OpenAIClient(),
            "slack": SlackClient(),
            "discord": DiscordClient(),
            "github": GitHubClient(),
            "notion": NotionClient(),
            "google": GoogleClient()
        }
        
        return handlers.get(service)
    
    def register_handler(self, service: str, handler):
        """Register a custom service handler"""
        self.service_handlers[service] = handler
