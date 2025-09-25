#!/usr/bin/env python3
"""
Automated Workflow Improvement for EV MAX INC

This script demonstrates how to use perplSDK to automate research workflows,
improve operational efficiency, and generate insights for strategic decision-making.

Usage:
    python automated_workflow_improvement.py
    
Environment Variables Required:
    PERPLEXITY_API_KEY: Your Perplexity API key
    GITHUB_TOKEN: GitHub token for publishing updates (optional)
    GITHUB_REPO: GitHub repository for publishing (optional, format: owner/repo)
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from perplSDK import (
    PerplexityClient,
    ResearchAutomation,
    ReportScheduler,
    MarkdownFormatter,
    GitHubPublisher
)
from perplSDK.core.config import Config
from perplSDK.research.trend_monitor import TrendMonitor
from perplSDK.research.market_intelligence import MarketIntelligence


class EVMaxWorkflowAutomation:
    """Automated workflow improvement system for EV MAX INC."""
    
    def __init__(self, config: Config):
        self.config = config
        self.research = ResearchAutomation(config)
        self.trend_monitor = TrendMonitor(config)
        self.market_intel = MarketIntelligence(config)
        self.formatter = MarkdownFormatter()
        self.scheduler = ReportScheduler(config)
        
        # EV MAX specific workflow areas
        self.workflow_areas = [
            "supply_chain_optimization",
            "customer_experience_improvement", 
            "manufacturing_efficiency",
            "quality_assurance_processes",
            "sustainability_initiatives",
            "technology_integration",
            "market_expansion_strategies",
            "competitive_positioning"
        ]
    
    def analyze_workflow_improvement_opportunities(self) -> dict:
        """Analyze current industry best practices for workflow improvements."""
        print("🔍 Analyzing workflow improvement opportunities...")
        
        # Create research project for workflow analysis
        project = self.research.create_project(
            "ev_max_workflow_improvement",
            "Analysis of workflow improvement opportunities for EV manufacturing and operations"
        )
        
        # Generate workflow improvement queries
        workflow_queries = []
        for area in self.workflow_areas:
            area_name = area.replace("_", " ")
            workflow_queries.extend([
                f"Best practices for {area_name} in electric vehicle manufacturing",
                f"Latest innovations in {area_name} for automotive companies",
                f"Workflow automation opportunities in {area_name}",
                f"Digital transformation strategies for {area_name}",
                f"Cost reduction techniques in {area_name} for EV companies"
            ])
        
        # Add general EV industry workflow queries
        workflow_queries.extend([
            "Lean manufacturing principles for electric vehicle production",
            "Digital twin technology applications in EV manufacturing",
            "IoT integration for smart EV manufacturing workflows",
            "AI and machine learning applications in automotive operations",
            "Sustainable manufacturing practices for electric vehicles",
            "Supply chain digitization in the EV industry",
            "Customer journey optimization for EV sales and service",
            "Quality management systems for EV manufacturing"
        ])
        
        # Add queries to project
        for i, query in enumerate(workflow_queries[:20]):  # Limit to top 20
            project.add_query(
                query,
                category="workflow_improvement",
                priority=len(workflow_queries) - i
            )
        
        # Execute research
        project = self.research.conduct_research(project.name, parallel=True)
        
        # Generate workflow improvement insights
        insights = self._extract_workflow_insights(project)
        
        return {
            "project_name": project.name,
            "total_queries": len(project.queries),
            "successful_results": len([r for r in project.results if r.model != "error"]),
            "workflow_insights": insights,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _extract_workflow_insights(self, project) -> list:
        """Extract actionable workflow insights from research results."""
        insights = []
        
        for i, result in enumerate(project.results):
            if result.model == "error":
                continue
            
            # Extract key recommendations and action items
            content = result.content
            
            # Simple keyword-based insight extraction
            actionable_keywords = [
                "implement", "adopt", "integrate", "optimize", "automate",
                "streamline", "improve", "enhance", "reduce", "increase"
            ]
            
            improvement_keywords = [
                "efficiency", "productivity", "cost savings", "quality",
                "automation", "digitization", "optimization", "innovation"
            ]
            
            # Score content for actionability
            actionable_score = sum(1 for keyword in actionable_keywords if keyword.lower() in content.lower())
            improvement_score = sum(1 for keyword in improvement_keywords if keyword.lower() in content.lower())
            
            if actionable_score >= 2 or improvement_score >= 2:
                # Extract key points
                key_points = self.formatter.extract_key_points(content, max_points=3)
                
                insight = {
                    "insight_id": f"workflow_insight_{i+1}",
                    "actionability_score": actionable_score + improvement_score,
                    "key_recommendations": key_points,
                    "full_content": content[:500] + "..." if len(content) > 500 else content,
                    "sources": result.sources,
                    "confidence_level": "high" if actionable_score >= 3 else "medium",
                    "implementation_priority": self._assess_implementation_priority(content)
                }
                insights.append(insight)
        
        # Sort by actionability score and implementation priority
        insights.sort(key=lambda x: (x["actionability_score"], x["implementation_priority"]), reverse=True)
        
        return insights[:15]  # Return top 15 insights
    
    def _assess_implementation_priority(self, content: str) -> int:
        """Assess implementation priority based on content analysis."""
        high_priority_indicators = [
            "immediate", "urgent", "critical", "quick win", "low cost",
            "easy to implement", "high impact", "competitive advantage"
        ]
        
        medium_priority_indicators = [
            "medium term", "gradual", "planned", "strategic", "investment required"
        ]
        
        content_lower = content.lower()
        
        high_count = sum(1 for indicator in high_priority_indicators if indicator in content_lower)
        medium_count = sum(1 for indicator in medium_priority_indicators if indicator in content_lower)
        
        if high_count >= 2:
            return 3  # High priority
        elif medium_count >= 2 or high_count >= 1:
            return 2  # Medium priority
        else:
            return 1  # Low priority
    
    def generate_implementation_roadmap(self, workflow_insights: list) -> dict:
        """Generate an implementation roadmap based on workflow insights."""
        print("🗺️ Generating implementation roadmap...")
        
        # Categorize insights by implementation timeline
        roadmap = {
            "immediate_actions": [],  # 0-3 months
            "short_term_initiatives": [],  # 3-12 months  
            "long_term_projects": [],  # 12+ months
            "resource_requirements": {},
            "expected_benefits": [],
            "success_metrics": []
        }
        
        for insight in workflow_insights:
            priority = insight.get("implementation_priority", 1)
            confidence = insight.get("confidence_level", "medium")
            
            roadmap_item = {
                "title": f"Implement {insight['key_recommendations'][0] if insight['key_recommendations'] else 'workflow improvement'}",
                "description": insight.get("full_content", "")[:200] + "...",
                "confidence_level": confidence,
                "expected_impact": "high" if priority >= 3 else "medium",
                "implementation_complexity": self._assess_complexity(insight["full_content"]),
                "sources": insight.get("sources", [])[:3]  # Top 3 sources
            }
            
            # Categorize by priority and complexity
            if priority >= 3 and roadmap_item["implementation_complexity"] == "low":
                roadmap["immediate_actions"].append(roadmap_item)
            elif priority >= 2:
                roadmap["short_term_initiatives"].append(roadmap_item)
            else:
                roadmap["long_term_projects"].append(roadmap_item)
        
        # Generate resource requirements and success metrics
        roadmap["resource_requirements"] = self._estimate_resource_requirements(workflow_insights)
        roadmap["success_metrics"] = self._define_success_metrics()
        roadmap["expected_benefits"] = self._identify_expected_benefits(workflow_insights)
        
        return roadmap
    
    def _assess_complexity(self, content: str) -> str:
        """Assess implementation complexity based on content."""
        high_complexity_indicators = [
            "major overhaul", "significant investment", "complex integration",
            "enterprise-wide", "substantial changes", "long-term commitment"
        ]
        
        low_complexity_indicators = [
            "simple", "easy", "straightforward", "minimal changes",
            "quick implementation", "plug-and-play", "off-the-shelf"
        ]
        
        content_lower = content.lower()
        
        high_count = sum(1 for indicator in high_complexity_indicators if indicator in content_lower)
        low_count = sum(1 for indicator in low_complexity_indicators if indicator in content_lower)
        
        if high_count >= 2:
            return "high"
        elif low_count >= 2:
            return "low"
        else:
            return "medium"
    
    def _estimate_resource_requirements(self, insights: list) -> dict:
        """Estimate resource requirements for implementation."""
        return {
            "human_resources": {
                "technical_staff": "2-4 engineers for automation implementation",
                "project_managers": "1-2 project managers for coordination",
                "training_requirements": "Staff training on new processes and tools"
            },
            "technology_investments": {
                "software_tools": "Workflow automation and monitoring tools",
                "hardware_upgrades": "IoT sensors and manufacturing equipment upgrades",
                "integration_costs": "System integration and API development"
            },
            "timeline_estimates": {
                "immediate_actions": "1-3 months",
                "short_term_initiatives": "3-12 months",
                "long_term_projects": "12-24 months"
            },
            "budget_considerations": [
                "Software licensing and subscription costs",
                "Hardware procurement and installation",
                "Training and change management",
                "Consultant and external service costs"
            ]
        }
    
    def _define_success_metrics(self) -> list:
        """Define success metrics for workflow improvements."""
        return [
            {
                "category": "Operational Efficiency",
                "metrics": [
                    "Production cycle time reduction (%)",
                    "Defect rate reduction (%)",
                    "Overall Equipment Effectiveness (OEE) improvement",
                    "Inventory turnover improvement"
                ]
            },
            {
                "category": "Cost Optimization",
                "metrics": [
                    "Operating cost reduction (%)",
                    "Labor cost per unit reduction",
                    "Energy consumption reduction (%)",
                    "Waste reduction (%)"
                ]
            },
            {
                "category": "Quality Improvement",
                "metrics": [
                    "Customer satisfaction scores",
                    "Return/warranty claim reduction (%)",
                    "First-pass yield improvement",
                    "Compliance score improvement"
                ]
            },
            {
                "category": "Innovation & Growth",
                "metrics": [
                    "Time-to-market reduction for new products",
                    "Employee productivity improvement (%)",
                    "Process automation coverage (%)",
                    "Digital transformation readiness score"
                ]
            }
        ]
    
    def _identify_expected_benefits(self, insights: list) -> list:
        """Identify expected benefits from workflow improvements."""
        benefits = []
        
        # Analyze insights for benefit keywords
        all_content = " ".join([insight.get("full_content", "") for insight in insights])
        
        benefit_categories = {
            "Cost Savings": ["cost reduction", "savings", "efficiency", "waste reduction"],
            "Quality Improvement": ["quality", "defect reduction", "accuracy", "reliability"],
            "Speed & Efficiency": ["faster", "quicker", "streamlined", "automated", "optimized"],
            "Innovation": ["innovation", "competitive advantage", "market leadership", "differentiation"],
            "Sustainability": ["sustainable", "green", "environmental", "carbon reduction"],
            "Customer Experience": ["customer satisfaction", "service quality", "responsiveness"]
        }
        
        for category, keywords in benefit_categories.items():
            keyword_count = sum(1 for keyword in keywords if keyword in all_content.lower())
            if keyword_count >= 2:
                benefits.append({
                    "category": category,
                    "confidence": "high" if keyword_count >= 4 else "medium",
                    "supporting_evidence": f"{keyword_count} related indicators found in analysis"
                })
        
        return benefits
    
    def setup_continuous_monitoring(self) -> dict:
        """Set up continuous monitoring for workflow improvements."""
        print("📊 Setting up continuous workflow monitoring...")
        
        # Schedule regular workflow analysis reports
        workflow_report_id = self.scheduler.schedule_report(
            name="EV MAX Workflow Improvement Monitor",
            report_type="research",
            frequency="weekly",
            config={
                "topic": "EV manufacturing workflow optimization",
                "research_type": "comprehensive",
                "industry": "automotive",
                "time_horizon": "current"
            },
            publish_to_github=bool(self.config.github_token and self.config.github_repo),
            github_config={
                "path": "reports/workflow/weekly_improvements.md",
                "commit_message": "Weekly Workflow Improvement Analysis"
            }
        )
        
        # Schedule trend monitoring for automation technologies
        tech_trends_id = self.scheduler.schedule_report(
            name="Manufacturing Technology Trends",
            report_type="trend_analysis",
            frequency="daily",
            config={
                "search_domains": [
                    "manufacturing automation",
                    "industrial IoT",
                    "lean manufacturing",
                    "digital twin technology",
                    "AI in manufacturing"
                ],
                "time_window": "week",
                "include_detailed_analysis": True
            },
            publish_to_github=bool(self.config.github_token and self.config.github_repo),
            github_config={
                "path": "reports/trends/manufacturing_tech.md",
                "commit_message": "Daily Manufacturing Technology Trends"
            }
        )
        
        return {
            "workflow_monitor_id": workflow_report_id,
            "tech_trends_id": tech_trends_id,
            "monitoring_frequency": "Daily trend analysis, Weekly workflow reports",
            "status": "active"
        }


def main():
    """Run automated workflow improvement analysis."""
    print("🏭 EV MAX INC Automated Workflow Improvement")
    print("=" * 50)
    
    # Load configuration
    try:
        config = Config.from_env()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return 1
    
    # Initialize workflow automation system
    workflow_automation = EVMaxWorkflowAutomation(config)
    
    # 1. Analyze workflow improvement opportunities
    print("\n🔍 Step 1: Analyzing workflow improvement opportunities...")
    try:
        workflow_analysis = workflow_automation.analyze_workflow_improvement_opportunities()
        
        insights_count = len(workflow_analysis.get("workflow_insights", []))
        successful_queries = workflow_analysis.get("successful_results", 0)
        
        print(f"✅ Workflow analysis completed:")
        print(f"   - Successful queries: {successful_queries}")
        print(f"   - Actionable insights identified: {insights_count}")
        
    except Exception as e:
        print(f"❌ Workflow analysis failed: {e}")
        return 1
    
    # 2. Generate implementation roadmap
    print("\n🗺️ Step 2: Generating implementation roadmap...")
    try:
        roadmap = workflow_automation.generate_implementation_roadmap(
            workflow_analysis["workflow_insights"]
        )
        
        immediate_actions = len(roadmap.get("immediate_actions", []))
        short_term = len(roadmap.get("short_term_initiatives", []))
        long_term = len(roadmap.get("long_term_projects", []))
        
        print(f"✅ Implementation roadmap generated:")
        print(f"   - Immediate actions (0-3 months): {immediate_actions}")
        print(f"   - Short-term initiatives (3-12 months): {short_term}")
        print(f"   - Long-term projects (12+ months): {long_term}")
        
    except Exception as e:
        print(f"❌ Roadmap generation failed: {e}")
        return 1
    
    # 3. Generate comprehensive report
    print("\n📝 Step 3: Generating workflow improvement report...")
    try:
        # Create comprehensive workflow improvement report
        report_content = workflow_automation.formatter.format_research_report(
            project_name="EV MAX Workflow Improvement Analysis",
            results=[],  # We'll create a custom report
            metadata={
                "description": "Comprehensive analysis of workflow improvement opportunities for EV MAX INC",
                "total_queries": workflow_analysis.get("total_queries", 0),
                "analysis_type": "Workflow Optimization"
            }
        )
        
        # Add roadmap section to report
        roadmap_section = f"""
## Implementation Roadmap

### Immediate Actions (0-3 months)
{chr(10).join([f"- {action['title']}" for action in roadmap.get('immediate_actions', [])])}

### Short-term Initiatives (3-12 months)
{chr(10).join([f"- {initiative['title']}" for initiative in roadmap.get('short_term_initiatives', [])])}

### Long-term Projects (12+ months)
{chr(10).join([f"- {project['title']}" for project in roadmap.get('long_term_projects', [])])}

## Expected Benefits
{chr(10).join([f"- **{benefit['category']}**: {benefit['supporting_evidence']}" for benefit in roadmap.get('expected_benefits', [])])}

## Success Metrics
{chr(10).join([f"### {metric_cat['category']}{chr(10)}{chr(10).join([f'- {metric}' for metric in metric_cat['metrics']])}" for metric_cat in roadmap.get('success_metrics', [])])}
"""
        
        # Combine report content
        full_report = report_content + roadmap_section
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"ev_max_workflow_improvement_analysis_{timestamp}"
        
        report_path = workflow_automation.formatter.save_report(
            content=full_report,
            filename=report_filename,
            output_dir=config.default_output_dir
        )
        
        print(f"✅ Workflow improvement report saved: {report_path}")
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return 1
    
    # 4. Set up continuous monitoring
    print("\n📊 Step 4: Setting up continuous monitoring...")
    try:
        monitoring_setup = workflow_automation.setup_continuous_monitoring()
        
        print(f"✅ Continuous monitoring configured:")
        print(f"   - Workflow monitor ID: {monitoring_setup['workflow_monitor_id']}")
        print(f"   - Technology trends ID: {monitoring_setup['tech_trends_id']}")
        print(f"   - Frequency: {monitoring_setup['monitoring_frequency']}")
        
    except Exception as e:
        print(f"❌ Continuous monitoring setup failed: {e}")
        return 1
    
    # 5. Publish to GitHub (if configured)
    if config.github_token and config.github_repo:
        print("\n🚀 Step 5: Publishing to GitHub...")
        try:
            github_publisher = GitHubPublisher(config)
            
            github_path = f"reports/workflow_improvement/{report_filename}.md"
            
            publish_result = github_publisher.publish_file(
                local_file_path=report_path,
                github_file_path=github_path,
                commit_message=f"EV MAX Workflow Improvement Analysis - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            print(f"✅ Report published to GitHub:")
            print(f"   - URL: {publish_result['content_url']}")
            
        except Exception as e:
            print(f"⚠️ GitHub publishing failed (continuing...): {e}")
    
    # 6. Display summary and recommendations
    print("\n📋 Workflow Improvement Summary")
    print("=" * 40)
    
    print(f"Analysis Results:")
    print(f"- Total workflow insights: {len(workflow_analysis.get('workflow_insights', []))}")
    print(f"- Immediate action items: {len(roadmap.get('immediate_actions', []))}")
    print(f"- Expected benefit categories: {len(roadmap.get('expected_benefits', []))}")
    
    # Display top immediate actions
    immediate_actions = roadmap.get('immediate_actions', [])
    if immediate_actions:
        print(f"\n🚀 Top Immediate Actions:")
        for i, action in enumerate(immediate_actions[:3], 1):
            print(f"   {i}. {action['title']}")
            print(f"      Impact: {action['expected_impact']}, Complexity: {action['implementation_complexity']}")
    
    # Display expected benefits
    benefits = roadmap.get('expected_benefits', [])
    if benefits:
        print(f"\n💰 Expected Benefits:")
        for benefit in benefits[:5]:
            print(f"   - {benefit['category']}: {benefit['confidence']} confidence")
    
    print(f"\n✅ Workflow improvement automation completed successfully!")
    print(f"Report saved to: {report_path}")
    
    return 0


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv('PERPLEXITY_API_KEY'):
        print("❌ Error: PERPLEXITY_API_KEY environment variable is required")
        print("\nPlease set your Perplexity API key:")
        print("export PERPLEXITY_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Run workflow improvement automation
    exit_code = main()
    sys.exit(exit_code)