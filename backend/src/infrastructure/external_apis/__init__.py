"""
External API Clients
"""

import httpx
from typing import Dict, Any, Optional


class OpenAIClient:
    """OpenAI API Client"""
    
    def __init__(self):
        self.base_url = "https://api.openai.com/v1"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute OpenAI action"""
        if action == "chat":
            return await self.chat(params)
        elif action == "completion":
            return await self.completion(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def chat(self, params: Dict[str, Any]) -> Dict:
        """Send chat completion request"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=params,
                headers={"Authorization": f"Bearer {params.get('api_key')}"}
            )
            return response.json()
    
    async def completion(self, params: Dict[str, Any]) -> Dict:
        """Send text completion request"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/completions",
                json=params,
                headers={"Authorization": f"Bearer {params.get('api_key')}"}
            )
            return response.json()


class SlackClient:
    """Slack API Client"""
    
    def __init__(self):
        self.base_url = "https://slack.com/api"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute Slack action"""
        if action == "send_message":
            return await self.send_message(params)
        elif action == "post_channel":
            return await self.post_to_channel(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def send_message(self, params: Dict[str, Any]) -> Dict:
        """Send Slack message"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat.postMessage",
                json={
                    "channel": params.get("channel"),
                    "text": params.get("message"),
                    "token": params.get("token")
                }
            )
            return response.json()
    
    async def post_to_channel(self, params: Dict[str, Any]) -> Dict:
        """Post to Slack channel"""
        return await self.send_message(params)


class DiscordClient:
    """Discord API Client"""
    
    def __init__(self):
        self.base_url = "https://discord.com/api/v10"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute Discord action"""
        if action == "send_message":
            return await self.send_message(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def send_message(self, params: Dict[str, Any]) -> Dict:
        """Send Discord message"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/channels/{params.get('channel_id')}/messages",
                json={"content": params.get("message")},
                headers={"Authorization": f"Bot {params.get('token')}"}
            )
            return response.json()


class GitHubClient:
    """GitHub API Client"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute GitHub action"""
        if action == "create_issue":
            return await self.create_issue(params)
        elif action == "create_pr":
            return await self.create_pr(params)
        elif action == "add_comment":
            return await self.add_comment(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def create_issue(self, params: Dict[str, Any]) -> Dict:
        """Create GitHub issue"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{params.get('repo')}/issues",
                json={
                    "title": params.get("title"),
                    "body": params.get("body", "")
                },
                headers={
                    "Authorization": f"token {params.get('token')}",
                    "Accept": "application/vnd.github+json"
                }
            )
            return response.json()
    
    async def create_pr(self, params: Dict[str, Any]) -> Dict:
        """Create pull request"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{params.get('repo')}/pulls",
                json={
                    "title": params.get("title"),
                    "head": params.get("head"),
                    "base": params.get("base", "main")
                },
                headers={
                    "Authorization": f"token {params.get('token')}",
                    "Accept": "application/vnd.github+json"
                }
            )
            return response.json()
    
    async def add_comment(self, params: Dict[str, Any]) -> Dict:
        """Add comment to issue/PR"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{params.get('repo')}/issues/{params.get('issue_number')}/comments",
                json={"body": params.get("comment")},
                headers={
                    "Authorization": f"token {params.get('token')}",
                    "Accept": "application/vnd.github+json"
                }
            )
            return response.json()


class NotionClient:
    """Notion API Client"""
    
    def __init__(self):
        self.base_url = "https://api.notion.com/v1"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute Notion action"""
        if action == "create_page":
            return await self.create_page(params)
        elif action == "query_database":
            return await self.query_database(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def create_page(self, params: Dict[str, Any]) -> Dict:
        """Create Notion page"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/pages",
                json=params.get("page_data", {}),
                headers={
                    "Authorization": f"Bearer {params.get('token')}",
                    "Notion-Version": "2022-06-28"
                }
            )
            return response.json()
    
    async def query_database(self, params: Dict[str, Any]) -> Dict:
        """Query Notion database"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/databases/{params.get('database_id')}/query",
                json=params.get("query", {}),
                headers={
                    "Authorization": f"Bearer {params.get('token')}",
                    "Notion-Version": "2022-06-28"
                }
            )
            return response.json()


class GoogleClient:
    """Google API Client"""
    
    def __init__(self):
        self.base_url = "https://sheets.googleapis.com/v4"
    
    async def execute(self, action: str, params: Dict[str, Any], context: Optional[Dict] = None) -> Dict:
        """Execute Google action"""
        if action == "update_sheet":
            return await self.update_sheet(params)
        elif action == "read_sheet":
            return await self.read_sheet(params)
        return {"success": False, "error": f"Unknown action: {action}"}
    
    async def update_sheet(self, params: Dict[str, Any]) -> Dict:
        """Update Google Sheet"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/spreadsheets/{params.get('spreadsheet_id')}/values/{params.get('range')}:append",
                json={"values": params.get("values", [[]])},
                headers={"Authorization": f"Bearer {params.get('token')}"}
            )
            return response.json()
    
    async def read_sheet(self, params: Dict[str, Any]) -> Dict:
        """Read Google Sheet"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/spreadsheets/{params.get('spreadsheet_id')}/values/{params.get('range')}",
                headers={"Authorization": f"Bearer {params.get('token')}"}
            )
            return response.json()
