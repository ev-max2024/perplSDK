"""GitHub integration for publishing reports and updates."""

import base64
from typing import Dict, Optional, Any, List
from datetime import datetime
from pathlib import Path

from github import Github, GithubException
from github.Repository import Repository
from github.ContentFile import ContentFile

from ..core.config import Config
from ..core.exceptions import PerplSDKError


class GitHubPublishingError(PerplSDKError):
    """Exception raised for GitHub publishing errors."""
    pass


class GitHubPublisher:
    """Publish research reports and updates to GitHub repositories."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize GitHub publisher.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config.from_env()
        
        if not self.config.github_token:
            raise GitHubPublishingError("GitHub token is required for publishing")
        
        if not self.config.github_repo:
            raise GitHubPublishingError("GitHub repository is required for publishing")
        
        try:
            self.github = Github(self.config.github_token)
            self.repo = self.github.get_repo(self.config.github_repo)
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to connect to GitHub repository: {e}")
    
    def publish_content(
        self,
        content: str,
        file_path: str,
        commit_message: str,
        branch: Optional[str] = None,
        create_pr: bool = False,
        pr_title: Optional[str] = None,
        pr_body: Optional[str] = None
    ) -> Dict[str, Any]:
        """Publish content to GitHub repository.
        
        Args:
            content: Content to publish
            file_path: Path in repository where to publish
            commit_message: Git commit message
            branch: Target branch (defaults to config default)
            create_pr: Whether to create a pull request
            pr_title: Pull request title
            pr_body: Pull request body
            
        Returns:
            Publishing results
        """
        if not branch:
            branch = self.config.github_branch
        
        try:
            # Check if file exists
            file_exists = self._file_exists(file_path, branch)
            
            if file_exists:
                # Update existing file
                existing_file = self.repo.get_contents(file_path, ref=branch)
                result = self.repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha,
                    branch=branch
                )
                action = "updated"
            else:
                # Create new file
                result = self.repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    branch=branch
                )
                action = "created"
            
            # Create pull request if requested
            pr_info = None
            if create_pr and branch != self.config.github_branch:
                pr_info = self._create_pull_request(
                    head_branch=branch,
                    base_branch=self.config.github_branch,
                    title=pr_title or f"Automated update: {Path(file_path).name}",
                    body=pr_body or f"Automated content update via perplSDK\n\nCommit: {commit_message}"
                )
            
            return {
                "action": action,
                "file_path": file_path,
                "branch": branch,
                "commit_sha": result["commit"].sha,
                "commit_url": result["commit"].html_url,
                "content_url": result["content"].html_url,
                "pull_request": pr_info,
                "published_at": datetime.now().isoformat()
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to publish content: {e}")
    
    def publish_file(
        self,
        local_file_path: str,
        github_file_path: str,
        commit_message: str,
        branch: Optional[str] = None,
        create_pr: bool = False,
        pr_title: Optional[str] = None,
        pr_body: Optional[str] = None
    ) -> Dict[str, Any]:
        """Publish a local file to GitHub repository.
        
        Args:
            local_file_path: Path to local file
            github_file_path: Path in GitHub repository
            commit_message: Git commit message
            branch: Target branch
            create_pr: Whether to create a pull request
            pr_title: Pull request title
            pr_body: Pull request body
            
        Returns:
            Publishing results
        """
        local_path = Path(local_file_path)
        
        if not local_path.exists():
            raise GitHubPublishingError(f"Local file not found: {local_file_path}")
        
        try:
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.publish_content(
                content=content,
                file_path=github_file_path,
                commit_message=commit_message,
                branch=branch,
                create_pr=create_pr,
                pr_title=pr_title,
                pr_body=pr_body
            )
            
        except Exception as e:
            raise GitHubPublishingError(f"Failed to read local file: {e}")
    
    def publish_multiple_files(
        self,
        files: List[Dict[str, str]],
        commit_message: str,
        branch: Optional[str] = None,
        create_pr: bool = False,
        pr_title: Optional[str] = None,
        pr_body: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Publish multiple files in separate commits.
        
        Args:
            files: List of file info dicts with 'local_path' and 'github_path'
            commit_message: Base commit message
            branch: Target branch
            create_pr: Whether to create a pull request
            pr_title: Pull request title
            pr_body: Pull request body
            
        Returns:
            List of publishing results
        """
        results = []
        
        for i, file_info in enumerate(files):
            try:
                file_commit_message = f"{commit_message} ({i+1}/{len(files)}): {Path(file_info['github_path']).name}"
                
                result = self.publish_file(
                    local_file_path=file_info['local_path'],
                    github_file_path=file_info['github_path'],
                    commit_message=file_commit_message,
                    branch=branch,
                    create_pr=create_pr if i == len(files) - 1 else False,  # Only create PR for last file
                    pr_title=pr_title,
                    pr_body=pr_body
                )
                results.append(result)
                
            except Exception as e:
                results.append({
                    "error": str(e),
                    "file_path": file_info.get('github_path', 'unknown'),
                    "failed_at": datetime.now().isoformat()
                })
        
        return results
    
    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create an issue in the GitHub repository.
        
        Args:
            title: Issue title
            body: Issue body
            labels: List of label names
            assignees: List of usernames to assign
            
        Returns:
            Issue information
        """
        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
                assignees=assignees or []
            )
            
            return {
                "issue_number": issue.number,
                "issue_url": issue.html_url,
                "title": issue.title,
                "state": issue.state,
                "created_at": issue.created_at.isoformat(),
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees]
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to create issue: {e}")
    
    def update_readme(
        self,
        content: str,
        commit_message: str = "Update README",
        branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update repository README file.
        
        Args:
            content: New README content
            commit_message: Commit message
            branch: Target branch
            
        Returns:
            Update results
        """
        readme_paths = ["README.md", "readme.md", "README.txt", "readme.txt"]
        
        # Find existing README
        readme_path = None
        for path in readme_paths:
            if self._file_exists(path, branch):
                readme_path = path
                break
        
        # Default to README.md if none found
        if not readme_path:
            readme_path = "README.md"
        
        return self.publish_content(
            content=content,
            file_path=readme_path,
            commit_message=commit_message,
            branch=branch
        )
    
    def create_release(
        self,
        tag_name: str,
        name: str,
        body: str,
        draft: bool = False,
        prerelease: bool = False,
        target_commitish: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a release in the GitHub repository.
        
        Args:
            tag_name: Git tag name
            name: Release name
            body: Release description
            draft: Whether this is a draft release
            prerelease: Whether this is a prerelease
            target_commitish: Target branch or commit SHA
            
        Returns:
            Release information
        """
        try:
            release = self.repo.create_git_release(
                tag=tag_name,
                name=name,
                message=body,
                draft=draft,
                prerelease=prerelease,
                target_commitish=target_commitish or self.config.github_branch
            )
            
            return {
                "release_id": release.id,
                "release_url": release.html_url,
                "tag_name": release.tag_name,
                "name": release.title,
                "draft": release.draft,
                "prerelease": release.prerelease,
                "created_at": release.created_at.isoformat(),
                "published_at": release.published_at.isoformat() if release.published_at else None
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to create release: {e}")
    
    def _file_exists(self, file_path: str, branch: Optional[str] = None) -> bool:
        """Check if a file exists in the repository.
        
        Args:
            file_path: Path to check
            branch: Branch to check (defaults to config default)
            
        Returns:
            True if file exists
        """
        try:
            self.repo.get_contents(file_path, ref=branch or self.config.github_branch)
            return True
        except GithubException:
            return False
    
    def _create_pull_request(
        self,
        head_branch: str,
        base_branch: str,
        title: str,
        body: str
    ) -> Dict[str, Any]:
        """Create a pull request.
        
        Args:
            head_branch: Source branch
            base_branch: Target branch
            title: PR title
            body: PR body
            
        Returns:
            Pull request information
        """
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            return {
                "pr_number": pr.number,
                "pr_url": pr.html_url,
                "title": pr.title,
                "state": pr.state,
                "head_branch": pr.head.ref,
                "base_branch": pr.base.ref,
                "created_at": pr.created_at.isoformat()
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to create pull request: {e}")
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get information about the configured repository.
        
        Returns:
            Repository information
        """
        try:
            return {
                "name": self.repo.name,
                "full_name": self.repo.full_name,
                "description": self.repo.description,
                "url": self.repo.html_url,
                "default_branch": self.repo.default_branch,
                "private": self.repo.private,
                "language": self.repo.language,
                "stars": self.repo.stargazers_count,
                "forks": self.repo.forks_count,
                "open_issues": self.repo.open_issues_count,
                "created_at": self.repo.created_at.isoformat(),
                "updated_at": self.repo.updated_at.isoformat()
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to get repository info: {e}")
    
    def list_branches(self) -> List[Dict[str, Any]]:
        """List all branches in the repository.
        
        Returns:
            List of branch information
        """
        try:
            branches = []
            for branch in self.repo.get_branches():
                branches.append({
                    "name": branch.name,
                    "protected": branch.protected,
                    "commit_sha": branch.commit.sha,
                    "commit_url": branch.commit.html_url
                })
            return branches
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to list branches: {e}")
    
    def create_branch(self, branch_name: str, source_branch: Optional[str] = None) -> Dict[str, Any]:
        """Create a new branch in the repository.
        
        Args:
            branch_name: Name of new branch
            source_branch: Source branch (defaults to repository default)
            
        Returns:
            Branch creation results
        """
        try:
            if not source_branch:
                source_branch = self.repo.default_branch
            
            # Get source branch reference
            source_ref = self.repo.get_branch(source_branch)
            
            # Create new branch
            new_ref = self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_ref.commit.sha
            )
            
            return {
                "branch_name": branch_name,
                "source_branch": source_branch,
                "commit_sha": new_ref.object.sha,
                "ref_url": new_ref.url,
                "created_at": datetime.now().isoformat()
            }
            
        except GithubException as e:
            raise GitHubPublishingError(f"Failed to create branch: {e}")
    
    def setup_automated_reporting(
        self,
        reports_directory: str = "reports",
        workflow_schedule: str = "0 9 * * 1"  # Monday at 9 AM UTC
    ) -> Dict[str, Any]:
        """Set up GitHub Actions workflow for automated reporting.
        
        Args:
            reports_directory: Directory for reports in repository
            workflow_schedule: Cron schedule for workflow
            
        Returns:
            Setup results
        """
        workflow_content = f"""name: Automated Research Reports

on:
  schedule:
    - cron: '{workflow_schedule}'
  workflow_dispatch:

jobs:
  generate-reports:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install perplSDK
    
    - name: Generate reports
      env:
        PERPLEXITY_API_KEY: ${{{{ secrets.PERPLEXITY_API_KEY }}}}
        GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
      run: |
        python -m perplSDK.examples.automated_reporting
    
    - name: Commit and push reports
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add {reports_directory}/
        git diff --staged --quiet || git commit -m "Automated research report update"
        git push
"""
        
        try:
            result = self.publish_content(
                content=workflow_content,
                file_path=".github/workflows/automated-reports.yml",
                commit_message="Set up automated reporting workflow"
            )
            
            return {
                "workflow_setup": result,
                "reports_directory": reports_directory,
                "schedule": workflow_schedule,
                "instructions": [
                    "Add PERPLEXITY_API_KEY to repository secrets",
                    "Ensure GITHUB_TOKEN has appropriate permissions",
                    f"Reports will be generated in {reports_directory}/ directory",
                    "Workflow runs on schedule or can be triggered manually"
                ]
            }
            
        except Exception as e:
            raise GitHubPublishingError(f"Failed to set up automated reporting: {e}")