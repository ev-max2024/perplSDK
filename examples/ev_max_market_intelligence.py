#!/usr/bin/env python3
"""
EV MAX INC Market Intelligence Automation Script

This script demonstrates how to use perplSDK for automated market intelligence
gathering specifically tailored for EV MAX INC's business needs.

Usage:
    python ev_max_market_intelligence.py
    
Environment Variables Required:
    PERPLEXITY_API_KEY: Your Perplexity API key
    GITHUB_TOKEN: GitHub token for publishing reports (optional)
    GITHUB_REPO: GitHub repository for publishing (optional, format: owner/repo)
"""

import os
import sys
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


def main():
    """Run EV MAX market intelligence automation."""
    print("🚗 EV MAX INC Market Intelligence Automation")
    print("=" * 50)
    
    # Load configuration
    try:
        config = Config.from_env()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure you have set the PERPLEXITY_API_KEY environment variable.")
        return 1
    
    # Initialize components
    market_intel = MarketIntelligence(config)
    formatter = MarkdownFormatter()
    
    print(f"🔍 Initializing market intelligence system...")
    
    # 1. Comprehensive EV Market Analysis
    print("\n📊 Conducting comprehensive EV market analysis...")
    
    try:
        ev_analysis = market_intel.conduct_market_analysis(
            sector=MarketSector.ELECTRIC_VEHICLES,
            analysis_name="ev_max_weekly_analysis",
            analysis_type="comprehensive",
            time_frame="current",
            geographic_focus="north_america"
        )
        
        print(f"✅ EV market analysis completed:")
        print(f"   - Total insights: {len(ev_analysis.get('insights', []))}")
        print(f"   - High-impact insights: {len([i for i in ev_analysis.get('insights', []) if i.get('impact_level') == 'high'])}")
        
    except Exception as e:
        print(f"❌ EV market analysis failed: {e}")
        return 1
    
    # 2. Battery Technology Trends
    print("\n🔋 Analyzing battery technology trends...")
    
    try:
        battery_analysis = market_intel.conduct_market_analysis(
            sector=MarketSector.BATTERY_TECHNOLOGY,
            analysis_name="battery_tech_trends",
            analysis_type="trends",
            time_frame="current"
        )
        
        print(f"✅ Battery technology analysis completed:")
        print(f"   - Total insights: {len(battery_analysis.get('insights', []))}")
        
    except Exception as e:
        print(f"❌ Battery technology analysis failed: {e}")
        return 1
    
    # 3. Charging Infrastructure Analysis
    print("\n⚡ Analyzing charging infrastructure market...")
    
    try:
        charging_analysis = market_intel.conduct_market_analysis(
            sector=MarketSector.CHARGING_INFRASTRUCTURE,
            analysis_name="charging_infrastructure_analysis",
            analysis_type="opportunities",
            time_frame="current",
            geographic_focus="north_america"
        )
        
        print(f"✅ Charging infrastructure analysis completed:")
        print(f"   - Total insights: {len(charging_analysis.get('insights', []))}")
        
    except Exception as e:
        print(f"❌ Charging infrastructure analysis failed: {e}")
        return 1
    
    # 4. Generate EV MAX Specific Insights
    print("\n🎯 Generating EV MAX specific strategic insights...")
    
    try:
        ev_max_insights = market_intel.get_ev_max_insights(
            time_frame="current"
        )
        
        print(f"✅ EV MAX insights generated:")
        print(f"   - Strategic insights: {len(ev_max_insights.get('insights', []))}")
        print(f"   - Recommendations: {len(ev_max_insights.get('recommendations', []))}")
        
        # Display key recommendations
        recommendations = ev_max_insights.get('recommendations', [])
        if recommendations:
            print("\n📋 Key Strategic Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
        
    except Exception as e:
        print(f"❌ EV MAX insights generation failed: {e}")
        return 1
    
    # 5. Generate Comprehensive Report
    print("\n📝 Generating comprehensive market intelligence report...")
    
    try:
        # Combine all analyses into a comprehensive report
        combined_report = formatter.format_market_intelligence_report(
            analysis_data={
                "sector": "comprehensive_ev_market",
                "analysis_type": "strategic_intelligence",
                "time_frame": "current",
                "geographic_focus": "north_america",
                "generated_at": datetime.now().isoformat(),
                "total_queries": (
                    ev_analysis.get('total_queries', 0) +
                    battery_analysis.get('total_queries', 0) +
                    charging_analysis.get('total_queries', 0)
                ),
                "total_results": (
                    ev_analysis.get('total_results', 0) +
                    battery_analysis.get('total_results', 0) +
                    charging_analysis.get('total_results', 0)
                ),
                "insights": (
                    ev_analysis.get('insights', []) +
                    battery_analysis.get('insights', []) +
                    charging_analysis.get('insights', [])
                ),
                "recommendations": ev_max_insights.get('recommendations', [])
            },
            include_recommendations=True
        )
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"ev_max_market_intelligence_{timestamp}"
        
        report_path = formatter.save_report(
            content=combined_report,
            filename=report_filename,
            output_dir=config.default_output_dir
        )
        
        print(f"✅ Market intelligence report saved: {report_path}")
        
        # 6. Publish to GitHub (if configured)
        if config.github_token and config.github_repo:
            print("\n🚀 Publishing report to GitHub...")
            
            try:
                github_publisher = GitHubPublisher(config)
                
                github_path = f"reports/market_intelligence/{report_filename}.md"
                
                publish_result = github_publisher.publish_file(
                    local_file_path=report_path,
                    github_file_path=github_path,
                    commit_message=f"EV MAX Market Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}"
                )
                
                print(f"✅ Report published to GitHub:")
                print(f"   - URL: {publish_result['content_url']}")
                print(f"   - Commit: {publish_result['commit_url']}")
                
            except Exception as e:
                print(f"⚠️ GitHub publishing failed (continuing...): {e}")
        
        # 7. Display Summary
        print("\n📈 Market Intelligence Summary")
        print("=" * 40)
        
        all_insights = (
            ev_analysis.get('insights', []) +
            battery_analysis.get('insights', []) +
            charging_analysis.get('insights', [])
        )
        
        high_impact = [i for i in all_insights if i.get('impact_level') == 'high']
        immediate_action = [i for i in all_insights if i.get('time_relevance') == 'immediate']
        
        print(f"Total Market Insights: {len(all_insights)}")
        print(f"High-Impact Opportunities: {len(high_impact)}")
        print(f"Immediate Action Items: {len(immediate_action)}")
        print(f"Strategic Recommendations: {len(ev_max_insights.get('recommendations', []))}")
        
        if high_impact:
            print(f"\n🔥 Top High-Impact Insights:")
            for i, insight in enumerate(high_impact[:3], 1):
                title = insight.get('title', f'Insight {i}')
                confidence = insight.get('confidence_score', 0)
                print(f"   {i}. {title} (Confidence: {confidence:.1%})")
        
        print(f"\n✅ Market intelligence automation completed successfully!")
        print(f"Report saved to: {report_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return 1


def setup_automated_schedule():
    """Set up automated scheduling for regular market intelligence reports."""
    print("\n⏰ Setting up automated market intelligence scheduling...")
    
    try:
        config = Config.from_env()
        scheduler = ReportScheduler(config)
        
        # Schedule weekly EV market analysis
        weekly_report_id = scheduler.schedule_report(
            name="EV MAX Weekly Market Intelligence",
            report_type="market_intelligence",
            frequency="weekly",
            config={
                "sector": "electric_vehicles",
                "analysis_type": "comprehensive",
                "time_frame": "current",
                "geographic_focus": "north_america",
                "include_recommendations": True
            },
            publish_to_github=bool(config.github_token and config.github_repo),
            github_config={
                "path": "reports/weekly/market_intelligence.md",
                "commit_message": "Weekly EV Market Intelligence Report"
            }
        )
        
        # Schedule daily trend monitoring
        daily_trends_id = scheduler.schedule_report(
            name="EV MAX Daily Trend Monitor",
            report_type="trend_analysis",
            frequency="daily",
            config={
                "search_domains": [
                    "electric vehicles",
                    "EV charging infrastructure",
                    "battery technology",
                    "EV policy and regulations"
                ],
                "time_window": "day",
                "include_detailed_analysis": False
            },
            publish_to_github=bool(config.github_token and config.github_repo),
            github_config={
                "path": "reports/daily/trend_monitor.md",
                "commit_message": "Daily EV Trend Monitoring Report"
            }
        )
        
        print(f"✅ Automated scheduling configured:")
        print(f"   - Weekly Market Intelligence: {weekly_report_id}")
        print(f"   - Daily Trend Monitor: {daily_trends_id}")
        
        # Start scheduler
        scheduler.start_scheduler()
        print(f"⏰ Scheduler started - reports will run automatically")
        
        # Save scheduler state
        scheduler_file = scheduler.save_scheduler_state()
        print(f"💾 Scheduler state saved: {scheduler_file}")
        
        return scheduler
        
    except Exception as e:
        print(f"❌ Automated scheduling setup failed: {e}")
        return None


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv('PERPLEXITY_API_KEY'):
        print("❌ Error: PERPLEXITY_API_KEY environment variable is required")
        print("\nPlease set your Perplexity API key:")
        print("export PERPLEXITY_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Run market intelligence automation
    exit_code = main()
    
    # Optionally set up automated scheduling
    if exit_code == 0:
        setup_choice = input("\n🤖 Set up automated scheduling? (y/n): ").lower().strip()
        if setup_choice in ['y', 'yes']:
            scheduler = setup_automated_schedule()
            if scheduler:
                try:
                    print("\n⏰ Scheduler is running. Press Ctrl+C to stop...")
                    while True:
                        import time
                        time.sleep(60)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping scheduler...")
                    scheduler.stop_scheduler()
                    print("✅ Scheduler stopped")
    
    sys.exit(exit_code)