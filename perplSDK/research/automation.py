"""Research automation for conducting comprehensive AI-powered research."""

import asyncio
from typing import List, Dict, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import json

from ..core.client import PerplexityClient, SearchResult
from ..core.config import Config
from ..utils.templates import ResearchTemplate


class ResearchProject:
    """Represents a research project with multiple queries and results."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.queries: List[Dict[str, Any]] = []
        self.results: List[SearchResult] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.metadata: Dict[str, Any] = {}
    
    def add_query(self, query: str, category: str = "general", priority: int = 1, **kwargs):
        """Add a research query to the project."""
        self.queries.append({
            "query": query,
            "category": category,
            "priority": priority,
            "kwargs": kwargs,
            "added_at": datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "queries": self.queries,
            "results": [
                {
                    "content": result.content,
                    "sources": result.sources,
                    "citations": result.citations,
                    "model": result.model,
                    "usage": result.usage
                } for result in self.results
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }


class ResearchAutomation:
    """Main class for automating research workflows."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize research automation.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config.from_env()
        self.client = PerplexityClient(self.config)
        self.projects: Dict[str, ResearchProject] = {}
        self.templates = ResearchTemplate()
    
    def create_project(self, name: str, description: str = "") -> ResearchProject:
        """Create a new research project.
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            ResearchProject instance
        """
        project = ResearchProject(name, description)
        self.projects[name] = project
        return project
    
    def get_project(self, name: str) -> Optional[ResearchProject]:
        """Get a research project by name."""
        return self.projects.get(name)
    
    def list_projects(self) -> List[str]:
        """List all project names."""
        return list(self.projects.keys())
    
    def conduct_research(
        self,
        project_name: str,
        queries: Optional[List[str]] = None,
        parallel: bool = True,
        save_results: bool = True
    ) -> ResearchProject:
        """Conduct research for a project.
        
        Args:
            project_name: Name of the research project
            queries: Optional list of queries to execute (uses project queries if None)
            parallel: Whether to execute queries in parallel
            save_results: Whether to save results to project
            
        Returns:
            Updated ResearchProject
        """
        project = self.projects.get(project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' not found")
        
        # Use provided queries or project queries
        if queries:
            query_list = [{"query": q, "category": "adhoc", "priority": 1, "kwargs": {}} for q in queries]
        else:
            query_list = project.queries
        
        if not query_list:
            raise ValueError("No queries to execute")
        
        # Sort by priority
        query_list.sort(key=lambda x: x.get("priority", 1), reverse=True)
        
        if parallel:
            results = self._conduct_parallel_research(query_list)
        else:
            results = self._conduct_sequential_research(query_list)
        
        if save_results:
            project.results.extend(results)
            project.updated_at = datetime.now()
        
        return project
    
    def _conduct_sequential_research(self, queries: List[Dict[str, Any]]) -> List[SearchResult]:
        """Conduct research sequentially."""
        results = []
        for query_info in queries:
            try:
                result = self.client.search(
                    query_info["query"],
                    **query_info.get("kwargs", {})
                )
                results.append(result)
            except Exception as e:
                # Create error result
                error_result = SearchResult(
                    content=f"Error executing query '{query_info['query']}': {str(e)}",
                    sources=[],
                    citations=[],
                    model="error"
                )
                results.append(error_result)
        return results
    
    def _conduct_parallel_research(self, queries: List[Dict[str, Any]]) -> List[SearchResult]:
        """Conduct research in parallel using asyncio."""
        async def execute_queries():
            tasks = []
            for query_info in queries:
                task = asyncio.create_task(
                    self.client.async_search(
                        query_info["query"],
                        **query_info.get("kwargs", {})
                    )
                )
                tasks.append(task)
            
            results = []
            for i, task in enumerate(tasks):
                try:
                    result = await task
                    results.append(result)
                except Exception as e:
                    error_result = SearchResult(
                        content=f"Error executing query '{queries[i]['query']}': {str(e)}",
                        sources=[],
                        citations=[],
                        model="error"
                    )
                    results.append(error_result)
            return results
        
        return asyncio.run(execute_queries())
    
    def save_project(self, project_name: str, filepath: Optional[str] = None) -> str:
        """Save a research project to file.
        
        Args:
            project_name: Name of the project to save
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        project = self.projects.get(project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' not found")
        
        if not filepath:
            output_dir = Path(self.config.default_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            filepath = output_dir / f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_project(self, filepath: str) -> ResearchProject:
        """Load a research project from file.
        
        Args:
            filepath: Path to the project file
            
        Returns:
            Loaded ResearchProject
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Project file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = ResearchProject(data["name"], data["description"])
        project.queries = data["queries"]
        project.created_at = datetime.fromisoformat(data["created_at"])
        project.updated_at = datetime.fromisoformat(data["updated_at"])
        project.metadata = data.get("metadata", {})
        
        # Reconstruct results
        for result_data in data["results"]:
            result = SearchResult(
                content=result_data["content"],
                sources=result_data["sources"],
                citations=result_data["citations"],
                model=result_data["model"],
                usage=result_data.get("usage", {})
            )
            project.results.append(result)
        
        self.projects[project.name] = project
        return project
    
    def generate_research_plan(
        self,
        topic: str,
        research_type: str = "comprehensive",
        industry: Optional[str] = None,
        time_horizon: str = "current"
    ) -> List[str]:
        """Generate a research plan with relevant queries.
        
        Args:
            topic: Main research topic
            research_type: Type of research (comprehensive, competitive, market, technical)
            industry: Specific industry context
            time_horizon: Time focus (current, historical, future, trends)
            
        Returns:
            List of research queries
        """
        return self.templates.generate_queries(
            topic=topic,
            research_type=research_type,
            industry=industry,
            time_horizon=time_horizon
        )
    
    def analyze_results(self, project_name: str) -> Dict[str, Any]:
        """Analyze research results for insights and patterns.
        
        Args:
            project_name: Name of the project to analyze
            
        Returns:
            Analysis results
        """
        project = self.projects.get(project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' not found")
        
        if not project.results:
            return {"error": "No results to analyze"}
        
        # Basic analysis
        total_results = len(project.results)
        successful_results = len([r for r in project.results if r.model != "error"])
        total_sources = sum(len(r.sources) for r in project.results)
        
        # Content analysis
        total_content_length = sum(len(r.content) for r in project.results)
        avg_content_length = total_content_length / total_results if total_results > 0 else 0
        
        # Source analysis
        all_sources = []
        for result in project.results:
            all_sources.extend(result.sources)
        
        unique_sources = list(set(all_sources))
        
        return {
            "project_name": project.name,
            "analysis_date": datetime.now().isoformat(),
            "total_queries": len(project.queries),
            "total_results": total_results,
            "successful_results": successful_results,
            "error_rate": (total_results - successful_results) / total_results if total_results > 0 else 0,
            "total_sources": total_sources,
            "unique_sources": len(unique_sources),
            "top_sources": self._get_top_sources(all_sources)[:10],
            "content_stats": {
                "total_content_length": total_content_length,
                "average_content_length": avg_content_length,
            },
            "time_analysis": {
                "project_duration": (project.updated_at - project.created_at).total_seconds() / 3600,  # hours
                "created_at": project.created_at.isoformat(),
                "last_updated": project.updated_at.isoformat()
            }
        }
    
    def _get_top_sources(self, sources: List[str]) -> List[Dict[str, Any]]:
        """Get top sources by frequency."""
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return [
            {"source": source, "count": count}
            for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
        ]