"""Report scheduling system for automated research and intelligence reports."""

import schedule
import time
import json
import threading
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

from ..core.config import Config
from ..research.automation import ResearchAutomation
from ..research.market_intelligence import MarketIntelligence, MarketSector
from ..research.trend_monitor import TrendMonitor
from .formatter import MarkdownFormatter
from ..github_integration.publisher import GitHubPublisher


class ReportFrequency(Enum):
    """Report frequency options."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class ReportType(Enum):
    """Types of reports that can be scheduled."""
    RESEARCH = "research"
    MARKET_INTELLIGENCE = "market_intelligence"
    TREND_ANALYSIS = "trend_analysis"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    CUSTOM = "custom"


@dataclass
class ScheduledReport:
    """Configuration for a scheduled report."""
    id: str
    name: str
    report_type: ReportType
    frequency: ReportFrequency
    config: Dict[str, Any]
    next_run: datetime
    last_run: Optional[datetime] = None
    enabled: bool = True
    output_format: str = "markdown"
    publish_to_github: bool = False
    github_config: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class ReportScheduler:
    """Schedule and manage automated research reports."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize report scheduler.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config.from_env()
        self.research = ResearchAutomation(self.config)
        self.market_intel = MarketIntelligence(self.config)
        self.trend_monitor = TrendMonitor(self.config)
        self.formatter = MarkdownFormatter()
        self.github_publisher = GitHubPublisher(self.config) if self.config.github_token else None
        
        # Report storage
        self.scheduled_reports: Dict[str, ScheduledReport] = {}
        self.report_history: List[Dict[str, Any]] = []
        
        # Scheduler state
        self._scheduler_thread = None
        self._is_running = False
        self._stop_event = threading.Event()
    
    def schedule_report(
        self,
        name: str,
        report_type: ReportType,
        frequency: ReportFrequency,
        config: Dict[str, Any],
        custom_schedule: Optional[str] = None,
        publish_to_github: bool = False,
        github_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Schedule a new report.
        
        Args:
            name: Report name
            report_type: Type of report
            frequency: How often to run the report
            config: Report-specific configuration
            custom_schedule: Custom cron-like schedule (for CUSTOM frequency)
            publish_to_github: Whether to publish to GitHub
            github_config: GitHub publishing configuration
            
        Returns:
            Report ID
        """
        report_id = f"{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate next run time
        next_run = self._calculate_next_run(frequency, custom_schedule)
        
        scheduled_report = ScheduledReport(
            id=report_id,
            name=name,
            report_type=report_type,
            frequency=frequency,
            config=config,
            next_run=next_run,
            publish_to_github=publish_to_github,
            github_config=github_config
        )
        
        self.scheduled_reports[report_id] = scheduled_report
        
        # Add to scheduler
        self._add_to_scheduler(scheduled_report, custom_schedule)
        
        return report_id
    
    def _calculate_next_run(self, frequency: ReportFrequency, custom_schedule: Optional[str] = None) -> datetime:
        """Calculate next run time based on frequency."""
        now = datetime.now()
        
        if frequency == ReportFrequency.HOURLY:
            return now + timedelta(hours=1)
        elif frequency == ReportFrequency.DAILY:
            return now + timedelta(days=1)
        elif frequency == ReportFrequency.WEEKLY:
            return now + timedelta(weeks=1)
        elif frequency == ReportFrequency.MONTHLY:
            return now + timedelta(days=30)  # Approximate
        else:
            # Custom schedule - for now, default to daily
            return now + timedelta(days=1)
    
    def _add_to_scheduler(self, report: ScheduledReport, custom_schedule: Optional[str] = None):
        """Add report to the schedule system."""
        def run_report():
            self._execute_report(report.id)
        
        if report.frequency == ReportFrequency.HOURLY:
            schedule.every().hour.do(run_report)
        elif report.frequency == ReportFrequency.DAILY:
            schedule.every().day.do(run_report)
        elif report.frequency == ReportFrequency.WEEKLY:
            schedule.every().week.do(run_report)
        elif report.frequency == ReportFrequency.MONTHLY:
            schedule.every(30).days.do(run_report)  # Approximate
        # Custom schedules would require more sophisticated parsing
    
    def _execute_report(self, report_id: str) -> Dict[str, Any]:
        """Execute a scheduled report.
        
        Args:
            report_id: ID of the report to execute
            
        Returns:
            Execution results
        """
        if report_id not in self.scheduled_reports:
            return {"error": f"Report {report_id} not found"}
        
        report = self.scheduled_reports[report_id]
        
        if not report.enabled:
            return {"status": "skipped", "reason": "Report is disabled"}
        
        try:
            # Generate report based on type
            if report.report_type == ReportType.RESEARCH:
                result = self._execute_research_report(report)
            elif report.report_type == ReportType.MARKET_INTELLIGENCE:
                result = self._execute_market_intelligence_report(report)
            elif report.report_type == ReportType.TREND_ANALYSIS:
                result = self._execute_trend_analysis_report(report)
            else:
                result = {"error": f"Unsupported report type: {report.report_type}"}
                
            # Update report status
            report.last_run = datetime.now()
            report.next_run = self._calculate_next_run(report.frequency)
            
            # Save to history
            execution_record = {
                "report_id": report_id,
                "report_name": report.name,
                "executed_at": report.last_run.isoformat(),
                "result": result,
                "status": "success" if "error" not in result else "error"
            }
            self.report_history.append(execution_record)
            
            return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "report_id": report_id,
                "executed_at": datetime.now().isoformat()
            }
            
            # Log error to history
            execution_record = {
                "report_id": report_id,
                "report_name": report.name,
                "executed_at": datetime.now().isoformat(),
                "result": error_result,
                "status": "error"
            }
            self.report_history.append(execution_record)
            
            return error_result
    
    def _execute_research_report(self, report: ScheduledReport) -> Dict[str, Any]:
        """Execute a research report."""
        config = report.config
        
        # Create research project
        project_name = f"{report.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project = self.research.create_project(project_name, config.get('description', ''))
        
        # Add queries
        queries = config.get('queries', [])
        if not queries and config.get('topic'):
            # Generate queries from topic
            queries = self.research.generate_research_plan(
                topic=config['topic'],
                research_type=config.get('research_type', 'comprehensive'),
                industry=config.get('industry'),
                time_horizon=config.get('time_horizon', 'current')
            )
        
        for query in queries:
            project.add_query(query, category=config.get('category', 'scheduled'))
        
        # Conduct research
        project = self.research.conduct_research(project_name, parallel=True)
        
        # Generate report
        markdown_content = self.formatter.format_research_report(
            project_name=project.name,
            results=project.results,
            metadata={
                'description': project.description,
                'total_queries': len(project.queries),
                'analysis_type': 'Scheduled Research Report'
            }
        )
        
        # Save report
        filename = f"{project.name}.md"
        filepath = self.formatter.save_report(markdown_content, filename, self.config.default_output_dir)
        
        result = {
            "project_name": project.name,
            "report_path": filepath,
            "total_results": len(project.results),
            "successful_results": len([r for r in project.results if r.model != "error"]),
            "generated_at": datetime.now().isoformat()
        }
        
        # Publish to GitHub if configured
        if report.publish_to_github and self.github_publisher:
            try:
                github_result = self._publish_to_github(report, filepath, markdown_content)
                result["github_publication"] = github_result
            except Exception as e:
                result["github_error"] = str(e)
        
        return result
    
    def _execute_market_intelligence_report(self, report: ScheduledReport) -> Dict[str, Any]:
        """Execute a market intelligence report."""
        config = report.config
        
        # Get sector
        sector_name = config.get('sector', 'electric_vehicles')
        try:
            sector = MarketSector(sector_name)
        except ValueError:
            sector = MarketSector.ELECTRIC_VEHICLES
        
        # Conduct market analysis
        analysis_data = self.market_intel.conduct_market_analysis(
            sector=sector,
            analysis_name=f"{report.name}_{datetime.now().strftime('%Y%m%d')}",
            analysis_type=config.get('analysis_type', 'comprehensive'),
            time_frame=config.get('time_frame', 'current'),
            geographic_focus=config.get('geographic_focus')
        )
        
        # Generate report
        markdown_content = self.formatter.format_market_intelligence_report(
            analysis_data=analysis_data,
            include_recommendations=config.get('include_recommendations', True)
        )
        
        # Save report
        filename = f"market_intelligence_{sector.value}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.formatter.save_report(markdown_content, filename, self.config.default_output_dir)
        
        result = {
            "analysis_name": analysis_data["analysis_name"],
            "sector": sector.value,
            "report_path": filepath,
            "total_insights": len(analysis_data.get("insights", [])),
            "generated_at": datetime.now().isoformat()
        }
        
        # Publish to GitHub if configured
        if report.publish_to_github and self.github_publisher:
            try:
                github_result = self._publish_to_github(report, filepath, markdown_content)
                result["github_publication"] = github_result
            except Exception as e:
                result["github_error"] = str(e)
        
        return result
    
    def _execute_trend_analysis_report(self, report: ScheduledReport) -> Dict[str, Any]:
        """Execute a trend analysis report."""
        config = report.config
        
        # Detect trends
        search_domains = config.get('search_domains', [
            "electric vehicles",
            "battery technology",
            "clean energy"
        ])
        
        trends = self.trend_monitor.detect_emerging_trends(
            search_domains=search_domains,
            time_window=config.get('time_window', 'month')
        )
        
        # Generate report
        report_title = f"Trend Analysis Report - {datetime.now().strftime('%Y-%m-%d')}"
        markdown_content = self.formatter.format_trend_report(
            trends=trends,
            report_title=report_title,
            include_detailed_analysis=config.get('include_detailed_analysis', True)
        )
        
        # Save report
        filename = f"trend_analysis_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.formatter.save_report(markdown_content, filename, self.config.default_output_dir)
        
        result = {
            "report_title": report_title,
            "report_path": filepath,
            "total_trends": len(trends),
            "emerging_trends": len([t for t in trends if t.get('trend_type') == 'emerging']),
            "generated_at": datetime.now().isoformat()
        }
        
        # Publish to GitHub if configured
        if report.publish_to_github and self.github_publisher:
            try:
                github_result = self._publish_to_github(report, filepath, markdown_content)
                result["github_publication"] = github_result
            except Exception as e:
                result["github_error"] = str(e)
        
        return result
    
    def _publish_to_github(self, report: ScheduledReport, filepath: str, content: str) -> Dict[str, Any]:
        """Publish report to GitHub."""
        if not self.github_publisher:
            raise Exception("GitHub publisher not configured")
        
        github_config = report.github_config or {}
        
        # Default GitHub path
        github_path = github_config.get('path', f"reports/{Path(filepath).name}")
        commit_message = github_config.get('commit_message', f"Automated report: {report.name}")
        branch = github_config.get('branch', self.config.github_branch)
        
        return self.github_publisher.publish_content(
            content=content,
            file_path=github_path,
            commit_message=commit_message,
            branch=branch
        )
    
    def start_scheduler(self):
        """Start the report scheduler in a background thread."""
        if self._is_running:
            return
        
        self._is_running = True
        self._stop_event.clear()
        
        def scheduler_loop():
            while not self._stop_event.is_set():
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self._scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self._scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the report scheduler."""
        if not self._is_running:
            return
        
        self._is_running = False
        self._stop_event.set()
        
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
    
    def list_scheduled_reports(self) -> List[Dict[str, Any]]:
        """List all scheduled reports.
        
        Returns:
            List of report information
        """
        reports = []
        for report_id, report in self.scheduled_reports.items():
            report_info = {
                "id": report_id,
                "name": report.name,
                "type": report.report_type.value,
                "frequency": report.frequency.value,
                "enabled": report.enabled,
                "next_run": report.next_run.isoformat() if report.next_run else None,
                "last_run": report.last_run.isoformat() if report.last_run else None,
                "created_at": report.created_at.isoformat() if report.created_at else None
            }
            reports.append(report_info)
        
        return reports
    
    def get_report_status(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific report.
        
        Args:
            report_id: Report ID
            
        Returns:
            Report status information
        """
        if report_id not in self.scheduled_reports:
            return None
        
        report = self.scheduled_reports[report_id]
        
        # Get recent history
        recent_history = [
            h for h in self.report_history[-10:]
            if h["report_id"] == report_id
        ]
        
        return {
            "report": asdict(report),
            "recent_executions": recent_history,
            "scheduler_running": self._is_running
        }
    
    def enable_report(self, report_id: str) -> bool:
        """Enable a scheduled report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if successful
        """
        if report_id in self.scheduled_reports:
            self.scheduled_reports[report_id].enabled = True
            return True
        return False
    
    def disable_report(self, report_id: str) -> bool:
        """Disable a scheduled report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if successful
        """
        if report_id in self.scheduled_reports:
            self.scheduled_reports[report_id].enabled = False
            return True
        return False
    
    def delete_report(self, report_id: str) -> bool:
        """Delete a scheduled report.
        
        Args:
            report_id: Report ID
            
        Returns:
            True if successful
        """
        if report_id in self.scheduled_reports:
            del self.scheduled_reports[report_id]
            # Remove from schedule (would need to track schedule jobs)
            return True
        return False
    
    def run_report_now(self, report_id: str) -> Dict[str, Any]:
        """Run a report immediately.
        
        Args:
            report_id: Report ID
            
        Returns:
            Execution results
        """
        return self._execute_report(report_id)
    
    def save_scheduler_state(self, filepath: Optional[str] = None) -> str:
        """Save scheduler state to file.
        
        Args:
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if not filepath:
            output_dir = Path(self.config.default_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            filepath = output_dir / f"scheduler_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to serializable format
        state_data = {
            "scheduled_reports": {},
            "report_history": self.report_history,
            "saved_at": datetime.now().isoformat()
        }
        
        for report_id, report in self.scheduled_reports.items():
            report_dict = asdict(report)
            # Convert datetime objects
            report_dict["next_run"] = report.next_run.isoformat() if report.next_run else None
            report_dict["last_run"] = report.last_run.isoformat() if report.last_run else None
            report_dict["created_at"] = report.created_at.isoformat() if report.created_at else None
            report_dict["report_type"] = report.report_type.value
            report_dict["frequency"] = report.frequency.value
            
            state_data["scheduled_reports"][report_id] = report_dict
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)