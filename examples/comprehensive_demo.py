#!/usr/bin/env python3
"""
Comprehensive perplSDK Demo

This script demonstrates all major features of the perplSDK:
- Research automation
- Market intelligence analysis
- Trend monitoring
- Report scheduling
- GitHub integration
- Markdown formatting

Usage:
    python comprehensive_demo.py
    
Environment Variables Required:
    PERPLEXITY_API_KEY: Your Perplexity API key
    GITHUB_TOKEN: GitHub token (optional)
    GITHUB_REPO: GitHub repository (optional, format: owner/repo)
"""

import os
import sys
import asyncio
from datetime import datetime
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
from perplSDK.research.market_intelligence import MarketIntelligence, MarketSector
from perplSDK.research.trend_monitor import TrendMonitor


async def demo_basic_client():
    """Demo basic Perplexity client functionality."""
    print("\n🔍 Demo 1: Basic Perplexity Client")
    print("-" * 40)
    
    config = Config.from_env()
    client = PerplexityClient(config)
    
    # Simple search
    print("Performing search query...")
    result = client.search(
        "What are the latest developments in electric vehicle battery technology?",
        max_tokens=500
    )
    
    print(f"✅ Search completed:")
    print(f"   Model: {result.model}")
    print(f"   Content length: {len(result.content)} characters")
    print(f"   Sources: {len(result.sources)}")
    
    if result.sources:
        print(f"   Sample source: {result.sources[0]}")
    
    # Demonstrate async search
    print("\nPerforming async search...")
    async_result = await client.async_search(
        "What are the key players in the EV charging infrastructure market?",
        max_tokens=300
    )
    
    print(f"✅ Async search completed:")
    print(f"   Content length: {len(async_result.content)} characters")
    
    client.close()


def demo_research_automation():
    """Demo research automation capabilities."""
    print("\n📚 Demo 2: Research Automation")
    print("-" * 40)
    
    config = Config.from_env()
    research = ResearchAutomation(config)
    
    # Create research project
    project = research.create_project(
        "EV Market Demo",
        "Demonstration of research automation capabilities"
    )
    
    # Add research queries
    queries = [
        "Current state of electric vehicle adoption worldwide",
        "Major challenges facing EV manufacturers in 2024",
        "Emerging trends in EV charging infrastructure",
        "Government policies supporting electric vehicle adoption"
    ]
    
    for query in queries:
        project.add_query(query, category="demo", priority=1)
    
    print(f"Created project with {len(project.queries)} queries")
    
    # Conduct research
    print("Conducting research (parallel execution)...")
    research.conduct_research(project.name, parallel=True)
    
    print(f"✅ Research completed:")
    print(f"   Total results: {len(project.results)}")
    print(f"   Successful results: {len([r for r in project.results if r.model != 'error'])}")
    
    # Analyze results
    analysis = research.analyze_results(project.name)
    print(f"   Unique sources: {analysis['unique_sources']}")
    print(f"   Average content length: {analysis['content_stats']['average_content_length']:.0f} chars")
    
    # Save project
    project_file = research.save_project(project.name)
    print(f"   Project saved: {project_file}")
    
    return project


def demo_market_intelligence():
    """Demo market intelligence capabilities."""
    print("\n📊 Demo 3: Market Intelligence")
    print("-" * 40)
    
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    
    # Conduct market analysis
    print("Conducting EV market analysis...")
    analysis = market_intel.conduct_market_analysis(
        sector=MarketSector.ELECTRIC_VEHICLES,
        analysis_name="demo_ev_analysis",
        analysis_type="trends",
        time_frame="current",
        geographic_focus="global"
    )
    
    insights = analysis.get('insights', [])
    print(f"✅ Market analysis completed:")
    print(f"   Total insights: {len(insights)}")
    
    if insights:
        high_impact = [i for i in insights if i.get('impact_level') == 'high']
        print(f"   High-impact insights: {len(high_impact)}")
        
        if high_impact:
            print(f"   Sample high-impact insight: {high_impact[0].get('title', 'N/A')}")
    
    # Get EV MAX specific insights
    print("\nGetting EV MAX specific insights...")
    ev_max_insights = market_intel.get_ev_max_insights(
        focus_area="electric vehicle market trends"
    )
    
    recommendations = ev_max_insights.get('recommendations', [])
    print(f"✅ EV MAX insights generated:")
    print(f"   Strategic recommendations: {len(recommendations)}")
    
    if recommendations:
        print(f"   Sample recommendation: {recommendations[0]}")
    
    return analysis


def demo_trend_monitoring():
    """Demo trend monitoring capabilities."""
    print("\n📈 Demo 4: Trend Monitoring")
    print("-" * 40)
    
    config = Config.from_env()
    trend_monitor = TrendMonitor(config)
    
    # Detect emerging trends
    print("Detecting emerging trends...")
    trends = trend_monitor.detect_emerging_trends(
        search_domains=["electric vehicles", "battery technology"],
        time_window="month"
    )
    
    print(f"✅ Trend detection completed:")
    print(f"   Total trends identified: {len(trends)}")
    
    if trends:
        emerging_trends = [t for t in trends if t.get('trend_type') == 'emerging']
        print(f"   Emerging trends: {len(emerging_trends)}")
        
        if emerging_trends:
            top_trend = emerging_trends[0]
            print(f"   Top emerging trend: {top_trend.get('topic', 'N/A')}")
            print(f"   Confidence: {top_trend.get('confidence_score', 0):.1%}")
    
    # Monitor trend evolution
    if trends:
        sample_topic = trends[0].get('topic', 'electric vehicle adoption')
        print(f"\nMonitoring evolution of: {sample_topic}")
        
        evolution = trend_monitor.monitor_trend_evolution(sample_topic, days_back=30)
        evolution_data = evolution.get('evolution_data', {})
        
        print(f"✅ Trend evolution analysis:")
        print(f"   Momentum: {evolution_data.get('momentum', 'N/A')}")
        print(f"   Key developments: {len(evolution_data.get('key_developments', []))}")
    
    return trends


def demo_report_formatting(project, market_analysis, trends):
    """Demo report formatting capabilities."""
    print("\n📝 Demo 5: Report Formatting")
    print("-" * 40)
    
    formatter = MarkdownFormatter()
    config = Config.from_env()
    
    # Format research report
    print("Formatting research report...")
    research_report = formatter.format_research_report(
        project_name=project.name,
        results=project.results,
        metadata={
            'description': project.description,
            'total_queries': len(project.queries),
            'analysis_type': 'Demo Research Report'
        }
    )
    
    # Save research report
    research_report_path = formatter.save_report(
        research_report,
        "demo_research_report",
        config.default_output_dir
    )
    print(f"✅ Research report saved: {research_report_path}")
    
    # Format market intelligence report
    print("Formatting market intelligence report...")
    market_report = formatter.format_market_intelligence_report(
        market_analysis,
        include_recommendations=True
    )
    
    market_report_path = formatter.save_report(
        market_report,
        "demo_market_intelligence_report",
        config.default_output_dir
    )
    print(f"✅ Market intelligence report saved: {market_report_path}")
    
    # Format trend report
    print("Formatting trend analysis report...")
    trend_report = formatter.format_trend_report(
        trends,
        "Demo Trend Analysis Report",
        include_detailed_analysis=True
    )
    
    trend_report_path = formatter.save_report(
        trend_report,
        "demo_trend_analysis_report",
        config.default_output_dir
    )
    print(f"✅ Trend analysis report saved: {trend_report_path}")
    
    return {
        "research_report": research_report_path,
        "market_report": market_report_path,
        "trend_report": trend_report_path
    }


def demo_github_integration(report_paths):
    """Demo GitHub integration capabilities."""
    print("\n🚀 Demo 6: GitHub Integration")
    print("-" * 40)
    
    config = Config.from_env()
    
    if not config.github_token or not config.github_repo:
        print("⚠️ GitHub integration not configured (GITHUB_TOKEN and GITHUB_REPO required)")
        print("Skipping GitHub demo...")
        return
    
    try:
        github_publisher = GitHubPublisher(config)
        
        # Get repository info
        repo_info = github_publisher.get_repository_info()
        print(f"✅ Connected to GitHub repository:")
        print(f"   Repository: {repo_info['full_name']}")
        print(f"   Stars: {repo_info['stars']}")
        print(f"   Language: {repo_info['language']}")
        
        # Publish one of the reports
        research_report_path = report_paths["research_report"]
        
        print(f"\nPublishing report to GitHub...")
        result = github_publisher.publish_file(
            local_file_path=research_report_path,
            github_file_path=f"demo_reports/{Path(research_report_path).name}",
            commit_message="Demo: Research report from perplSDK"
        )
        
        print(f"✅ Report published to GitHub:")
        print(f"   Action: {result['action']}")
        print(f"   File URL: {result['content_url']}")
        print(f"   Commit URL: {result['commit_url']}")
        
        # Create an issue
        print("\nCreating demo issue...")
        issue_result = github_publisher.create_issue(
            title="perplSDK Demo Completed",
            body=f"""# perplSDK Demo Results

This issue was automatically created to demonstrate the GitHub integration capabilities of perplSDK.

## Demo Summary
- Research automation: ✅
- Market intelligence: ✅  
- Trend monitoring: ✅
- Report formatting: ✅
- GitHub integration: ✅

## Generated Reports
- Research Report: [View Report]({result['content_url']})
- Market Intelligence Report: Generated locally
- Trend Analysis Report: Generated locally

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""",
            labels=["demo", "automation", "perplSDK"]
        )
        
        print(f"✅ Demo issue created:")
        print(f"   Issue #: {issue_result['issue_number']}")
        print(f"   URL: {issue_result['issue_url']}")
        
    except Exception as e:
        print(f"❌ GitHub integration demo failed: {e}")


def demo_report_scheduling():
    """Demo report scheduling capabilities."""
    print("\n⏰ Demo 7: Report Scheduling")
    print("-" * 40)
    
    config = Config.from_env()
    scheduler = ReportScheduler(config)
    
    # Schedule a demo report
    print("Scheduling demo report...")
    report_id = scheduler.schedule_report(
        name="Demo Daily Trend Monitor",
        report_type="trend_analysis",
        frequency="daily",
        config={
            "search_domains": ["electric vehicles", "clean energy"],
            "time_window": "day",
            "include_detailed_analysis": False
        },
        publish_to_github=False  # Don't actually publish for demo
    )
    
    print(f"✅ Report scheduled:")
    print(f"   Report ID: {report_id}")
    
    # List scheduled reports
    scheduled_reports = scheduler.list_scheduled_reports()
    print(f"   Total scheduled reports: {len(scheduled_reports)}")
    
    # Get report status
    status = scheduler.get_report_status(report_id)
    if status:
        report_info = status["report"]
        print(f"   Next run: {report_info['next_run']}")
        print(f"   Enabled: {report_info['enabled']}")
    
    # Run report immediately for demo
    print("\nRunning report immediately for demo...")
    execution_result = scheduler.run_report_now(report_id)
    
    if "error" not in execution_result:
        print(f"✅ Report executed successfully:")
        print(f"   Report path: {execution_result.get('report_path', 'N/A')}")
        print(f"   Total trends: {execution_result.get('total_trends', 0)}")
    else:
        print(f"❌ Report execution failed: {execution_result['error']}")
    
    # Clean up - disable the demo report
    scheduler.disable_report(report_id)
    print(f"✅ Demo report disabled")


async def main():
    """Run comprehensive perplSDK demo."""
    print("🎯 perplSDK Comprehensive Demo")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Demo 1: Basic client functionality
        await demo_basic_client()
        
        # Demo 2: Research automation
        project = demo_research_automation()
        
        # Demo 3: Market intelligence
        market_analysis = demo_market_intelligence()
        
        # Demo 4: Trend monitoring
        trends = demo_trend_monitoring()
        
        # Demo 5: Report formatting
        report_paths = demo_report_formatting(project, market_analysis, trends)
        
        # Demo 6: GitHub integration
        demo_github_integration(report_paths)
        
        # Demo 7: Report scheduling
        demo_report_scheduling()
        
        # Summary
        print("\n🎉 Demo Summary")
        print("=" * 30)
        print("✅ All perplSDK features demonstrated successfully!")
        print("\nFeatures demonstrated:")
        print("  1. ✅ Basic Perplexity API client (sync & async)")
        print("  2. ✅ Research automation and project management")
        print("  3. ✅ Market intelligence analysis")
        print("  4. ✅ Trend monitoring and detection")
        print("  5. ✅ Professional report formatting")
        print("  6. ✅ GitHub integration and publishing")
        print("  7. ✅ Automated report scheduling")
        
        print(f"\nGenerated reports:")
        for report_type, path in report_paths.items():
            print(f"  - {report_type.replace('_', ' ').title()}: {path}")
        
        print(f"\n🚗 Ready for EV MAX INC production use!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return 1


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv('PERPLEXITY_API_KEY'):
        print("❌ Error: PERPLEXITY_API_KEY environment variable is required")
        print("\nPlease set your Perplexity API key:")
        print("export PERPLEXITY_API_KEY='your-api-key-here'")
        print("\nOptional GitHub integration:")
        print("export GITHUB_TOKEN='your-github-token'")
        print("export GITHUB_REPO='owner/repo-name'")
        sys.exit(1)
    
    # Run comprehensive demo
    exit_code = asyncio.run(main())
    sys.exit(exit_code)