"""Tests for research automation."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from perplSDK.research.automation import ResearchAutomation, ResearchProject
from perplSDK.core.client import SearchResult
from perplSDK.core.config import Config


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return Config(perplexity_api_key="test-key")


@pytest.fixture
def research_automation(mock_config):
    """Create research automation instance."""
    return ResearchAutomation(mock_config)


def test_research_project_creation():
    """Test research project creation."""
    project = ResearchProject("Test Project", "Test description")
    
    assert project.name == "Test Project"
    assert project.description == "Test description"
    assert len(project.queries) == 0
    assert len(project.results) == 0
    assert isinstance(project.created_at, datetime)


def test_research_project_add_query():
    """Test adding queries to research project."""
    project = ResearchProject("Test Project")
    
    project.add_query("Test query 1", category="test", priority=1)
    project.add_query("Test query 2", category="test", priority=2)
    
    assert len(project.queries) == 2
    assert project.queries[0]["query"] == "Test query 1"
    assert project.queries[1]["priority"] == 2


def test_create_project(research_automation):
    """Test creating a research project."""
    project = research_automation.create_project("Test Project", "Description")
    
    assert project.name == "Test Project"
    assert project.description == "Description"
    assert "Test Project" in research_automation.projects


def test_get_project(research_automation):
    """Test retrieving a research project."""
    # Create project
    research_automation.create_project("Test Project")
    
    # Retrieve project
    retrieved = research_automation.get_project("Test Project")
    assert retrieved is not None
    assert retrieved.name == "Test Project"
    
    # Test non-existent project
    missing = research_automation.get_project("Missing Project")
    assert missing is None


def test_list_projects(research_automation):
    """Test listing projects."""
    # Initially empty
    assert len(research_automation.list_projects()) == 0
    
    # Add projects
    research_automation.create_project("Project 1")
    research_automation.create_project("Project 2")
    
    projects = research_automation.list_projects()
    assert len(projects) == 2
    assert "Project 1" in projects
    assert "Project 2" in projects


@patch('perplSDK.research.automation.ResearchAutomation._conduct_sequential_research')
def test_conduct_research_sequential(mock_sequential, research_automation):
    """Test conducting research sequentially."""
    # Create project with queries
    project = research_automation.create_project("Test Project")
    project.add_query("Test query")
    
    # Mock results
    mock_results = [SearchResult(content="Test result", model="test-model")]
    mock_sequential.return_value = mock_results
    
    # Conduct research
    result_project = research_automation.conduct_research("Test Project", parallel=False)
    
    assert result_project is not None
    assert len(result_project.results) == 1
    mock_sequential.assert_called_once()


@patch('perplSDK.research.automation.ResearchAutomation._conduct_parallel_research')
def test_conduct_research_parallel(mock_parallel, research_automation):
    """Test conducting research in parallel."""
    # Create project with queries
    project = research_automation.create_project("Test Project")
    project.add_query("Test query")
    
    # Mock results
    mock_results = [SearchResult(content="Test result", model="test-model")]
    mock_parallel.return_value = mock_results
    
    # Conduct research
    result_project = research_automation.conduct_research("Test Project", parallel=True)
    
    assert result_project is not None
    assert len(result_project.results) == 1
    mock_parallel.assert_called_once()


def test_conduct_research_with_custom_queries(research_automation):
    """Test conducting research with custom queries."""
    # Create empty project
    research_automation.create_project("Test Project")
    
    with patch.object(research_automation, '_conduct_sequential_research') as mock_sequential:
        mock_sequential.return_value = [SearchResult(content="Test", model="test")]
        
        # Conduct research with custom queries
        research_automation.conduct_research(
            "Test Project", 
            queries=["Custom query 1", "Custom query 2"],
            parallel=False
        )
        
        # Should have been called with custom queries
        call_args = mock_sequential.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["query"] == "Custom query 1"


def test_generate_research_plan(research_automation):
    """Test research plan generation."""
    queries = research_automation.generate_research_plan(
        topic="electric vehicles",
        research_type="comprehensive",
        industry="automotive"
    )
    
    assert isinstance(queries, list)
    assert len(queries) > 0
    
    # Check that queries contain the topic
    topic_mentioned = any("electric vehicles" in query.lower() for query in queries)
    assert topic_mentioned


def test_analyze_results(research_automation):
    """Test results analysis."""
    # Create project with results
    project = research_automation.create_project("Test Project")
    project.results = [
        SearchResult(
            content="Test content 1",
            sources=["http://example1.com", "http://example2.com"],
            model="test-model"
        ),
        SearchResult(
            content="Test content 2",
            sources=["http://example2.com", "http://example3.com"],
            model="test-model"
        )
    ]
    
    analysis = research_automation.analyze_results("Test Project")
    
    assert analysis["project_name"] == "Test Project"
    assert analysis["total_results"] == 2
    assert analysis["successful_results"] == 2
    assert analysis["error_rate"] == 0.0
    assert analysis["total_sources"] == 4
    assert analysis["unique_sources"] == 3


def test_project_to_dict():
    """Test project serialization."""
    project = ResearchProject("Test Project", "Description")
    project.add_query("Test query")
    project.results = [SearchResult(content="Test", model="test")]
    
    project_dict = project.to_dict()
    
    assert project_dict["name"] == "Test Project"
    assert project_dict["description"] == "Description"
    assert len(project_dict["queries"]) == 1
    assert len(project_dict["results"]) == 1
    assert "created_at" in project_dict
    assert "updated_at" in project_dict