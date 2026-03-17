#!/usr/bin/env python3
"""
Jira Assistant - Direct REST API Integration
Manage Jira issues without external MCP servers.
"""

import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, List

# Load environment variables
load_dotenv()

class JiraClient:
    """Simple Jira REST API client"""
    
    def __init__(self):
        self.base_url = os.getenv('JIRA_URL', 'https://ebury.atlassian.net')
        self.email = os.getenv('JIRA_EMAIL')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY', 'EPT')
        
        if not self.email or not self.api_token:
            raise ValueError("JIRA_EMAIL and JIRA_API_TOKEN must be set in .env")
        
        self.auth = (self.email, self.api_token)
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search issues using JQL"""
        url = f"{self.base_url}/rest/api/3/search"
        params = {
            'jql': jql,
            'maxResults': max_results,
            'fields': 'summary,status,assignee,priority,created,updated'
        }
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json().get('issues', [])
    
    def create_issue(self, summary: str, description: str = "", 
                    issue_type: str = "Task", priority: str = "Medium") -> Dict:
        """Create a new Jira issue"""
        url = f"{self.base_url}/rest/api/3/issue"
        
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type},
                "priority": {"name": priority}
            }
        }
        
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_issue(self, issue_key: str) -> Dict:
        """Get issue details"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def update_issue(self, issue_key: str, fields: Dict) -> None:
        """Update issue fields"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        payload = {"fields": fields}
        
        response = requests.put(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
    
    def transition_issue(self, issue_key: str, transition_name: str) -> None:
        """Transition issue to new status"""
        # Get available transitions
        trans_url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        response = requests.get(trans_url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        transitions = response.json().get('transitions', [])
        
        # Find matching transition
        transition_id = None
        for trans in transitions:
            if trans['name'].lower() == transition_name.lower():
                transition_id = trans['id']
                break
        
        if not transition_id:
            available = [t['name'] for t in transitions]
            raise ValueError(f"Transition '{transition_name}' not found. Available: {available}")
        
        # Execute transition
        payload = {"transition": {"id": transition_id}}
        response = requests.post(trans_url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
    
    def add_comment(self, issue_key: str, comment: str) -> Dict:
        """Add comment to issue"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ]
            }
        }
        
        response = requests.post(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


def main():
    """Example usage"""
    try:
        client = JiraClient()
        
        print("🔍 Jira Assistant - Direct REST API")
        print(f"Connected to: {client.base_url}")
        print(f"Project: {client.project_key}\n")
        
        # Example: Search my open issues
        print("📋 My open issues:")
        jql = f"project = {client.project_key} AND assignee = currentUser() AND status != Done"
        issues = client.search_issues(jql, max_results=5)
        
        if not issues:
            print("  No open issues found")
        else:
            for issue in issues:
                key = issue['key']
                summary = issue['fields']['summary']
                status = issue['fields']['status']['name']
                print(f"  • {key}: {summary} [{status}]")
        
        print("\n✓ API connection successful")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nRequired environment variables:")
        print("  - JIRA_URL (default: https://ebury.atlassian.net)")
        print("  - JIRA_EMAIL (your Atlassian email)")
        print("  - JIRA_API_TOKEN (from https://id.atlassian.com/manage-profile/security/api-tokens)")
        print("  - JIRA_PROJECT_KEY (default: EPT)")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ API error: {e}")
        if e.response.status_code == 401:
            print("Authentication failed. Check JIRA_EMAIL and JIRA_API_TOKEN")
        elif e.response.status_code == 404:
            print(f"Project '{client.project_key}' not found or no access")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
