#!/usr/bin/env python3
"""
Command-line interface for perplSDK.

This module provides a CLI for interacting with perplSDK functionality.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime

from .core.config import Config
from .core.client import PerplexityClient
from .research.automation import ResearchAutomation
from .research.market_intelligence import MarketIntelligence, MarketSector
from .research.trend_monitor import TrendMonitor
from .reports.scheduler import ReportScheduler
from .reports.formatter import MarkdownFormatter
from .github_integration.publisher import GitHubPublisher


def cmd_search(args):
    """Execute a simple search query."""
    config = Config.from_env()
    client = PerplexityClient(config)
    
    try:
        result = client.search(
            args.query,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            recency_filter=args.recency
        )
        
        print(f"Query: {args.query}")
        print(f"Model: {result.model}")
        print(f"Content Length: {len(result.content)} characters")
        print(f"Sources: {len(result.sources)}")
        print("\n" + "="*50)
        print("CONTENT:")
        print("="*50)
        print(result.content)
        
        if args.show_sources and result.sources:
            print("\n" + "="*50)
            print("SOURCES:")
            print("="*50)
            for i, source in enumerate(result.sources, 1):
                print(f"{i}. {source}")
                
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        client.close()
    
    return 0


def cmd_research(args):
    """Execute research automation."""
    config = Config.from_env()
    research = ResearchAutomation(config)
    formatter = MarkdownFormatter()
    
    try:
        # Create project
        project = research.create_project(args.name, args.description or "")
        
        # Add queries
        if args.queries:
            for query in args.queries:
                project.add_query(query)
        elif args.topic:
            # Generate queries from topic
            queries = research.generate_research_plan(
                topic=args.topic,
                research_type=args.research_type,
                industry=args.industry
            )
            for query in queries:
                project.add_query(query)
        else:
            print("Error: Either --queries or --topic is required")
            return 1
        
        print(f"Created project '{args.name}' with {len(project.queries)} queries")
        
        # Conduct research
        print("Conducting research...")
        research.conduct_research(args.name, parallel=args.parallel)
        
        # Generate report
        if args.output:
            report_content = formatter.format_research_report(
                project_name=project.name,
                results=project.results,
                metadata={
                    'description': project.description,
                    'total_queries': len(project.queries),
                    'analysis_type': 'CLI Research Report'
                }
            )
            
            report_path = formatter.save_report(
                report_content,
                args.output,
                args.output_dir
            )
            print(f"Report saved: {report_path}")
        
        # Display summary
        successful = len([r for r in project.results if r.model != "error"])
        print(f"\nResearch completed:")
        print(f"  Total results: {len(project.results)}")
        print(f"  Successful: {successful}")
        print(f"  Error rate: {(len(project.results) - successful) / len(project.results) * 100:.1f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_market_intel(args):
    """Execute market intelligence analysis."""
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    formatter = MarkdownFormatter()
    
    try:
        # Parse sector
        try:
            sector = MarketSector(args.sector)
        except ValueError:
            print(f"Error: Invalid sector '{args.sector}'")
            print(f"Available sectors: {[s.value for s in MarketSector]}")
            return 1
        
        # Conduct analysis
        print(f"Conducting {args.analysis_type} analysis for {sector.value}...")
        analysis = market_intel.conduct_market_analysis(
            sector=sector,
            analysis_type=args.analysis_type,
            time_frame=args.time_frame,
            geographic_focus=args.geographic_focus
        )
        
        # Generate report
        if args.output:
            report_content = formatter.format_market_intelligence_report(
                analysis,
                include_recommendations=True
            )
            
            report_path = formatter.save_report(
                report_content,
                args.output,
                args.output_dir
            )
            print(f"Report saved: {report_path}")
        
        # Display summary
        insights = analysis.get('insights', [])
        high_impact = [i for i in insights if i.get('impact_level') == 'high']
        
        print(f"\nMarket intelligence analysis completed:")
        print(f"  Total insights: {len(insights)}")
        print(f"  High-impact insights: {len(high_impact)}")
        print(f"  Recommendations: {len(analysis.get('recommendations', []))}")
        
        if high_impact:
            print(f"\nTop high-impact insights:")
            for i, insight in enumerate(high_impact[:3], 1):
                print(f"  {i}. {insight.get('title', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_trends(args):
    """Execute trend monitoring."""
    config = Config.from_env()
    trend_monitor = TrendMonitor(config)
    formatter = MarkdownFormatter()
    
    try:
        if args.command == "detect":
            # Detect emerging trends
            print(f"Detecting trends in: {', '.join(args.domains)}")
            trends = trend_monitor.detect_emerging_trends(
                search_domains=args.domains,
                time_window=args.time_window
            )
            
            print(f"\nTrend detection completed:")
            print(f"  Total trends: {len(trends)}")
            
            emerging = [t for t in trends if t.get('trend_type') == 'emerging']
            print(f"  Emerging trends: {len(emerging)}")
            
            if trends:
                print(f"\nTop trends:")
                for i, trend in enumerate(trends[:5], 1):
                    confidence = trend.get('confidence_score', 0)
                    print(f"  {i}. {trend.get('topic', 'N/A')} (Confidence: {confidence:.1%})")
            
            # Generate report if requested
            if args.output:
                report_content = formatter.format_trend_report(
                    trends,
                    f"Trend Analysis - {datetime.now().strftime('%Y-%m-%d')}",
                    include_detailed_analysis=True
                )
                
                report_path = formatter.save_report(
                    report_content,
                    args.output,
                    args.output_dir
                )
                print(f"\nReport saved: {report_path}")
                
        elif args.command == "monitor":
            # Monitor trend evolution
            print(f"Monitoring trend evolution: {args.topic}")
            evolution = trend_monitor.monitor_trend_evolution(
                args.topic,
                days_back=args.days_back
            )
            
            evolution_data = evolution.get('evolution_data', {})
            
            print(f"\nTrend evolution analysis:")
            print(f"  Topic: {args.topic}")
            print(f"  Momentum: {evolution_data.get('momentum', 'N/A')}")
            print(f"  Key developments: {len(evolution_data.get('key_developments', []))}")
            
            developments = evolution_data.get('key_developments', [])
            if developments:
                print(f"\nKey developments:")
                for i, dev in enumerate(developments[:3], 1):
                    print(f"  {i}. {dev}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_schedule(args):
    """Manage report scheduling."""
    config = Config.from_env()
    scheduler = ReportScheduler(config)
    
    try:
        if args.command == "list":
            reports = scheduler.list_scheduled_reports()
            print(f"Scheduled reports ({len(reports)}):")
            for report in reports:
                status = "✅" if report["enabled"] else "❌"
                print(f"  {status} {report['name']} ({report['type']}, {report['frequency']})")
                print(f"     ID: {report['id']}")
                print(f"     Next run: {report['next_run']}")
                
        elif args.command == "add":
            report_id = scheduler.schedule_report(
                name=args.name,
                report_type=args.type,
                frequency=args.frequency,
                config={"topic": args.topic} if args.topic else {},
                publish_to_github=args.github
            )
            print(f"Report scheduled: {report_id}")
            
        elif args.command == "run":
            result = scheduler.run_report_now(args.report_id)
            if "error" in result:
                print(f"Error: {result['error']}")
                return 1
            else:
                print(f"Report executed successfully")
                print(f"  Report path: {result.get('report_path', 'N/A')}")
                
        elif args.command == "enable":
            success = scheduler.enable_report(args.report_id)
            print(f"Report {'enabled' if success else 'not found'}")
            
        elif args.command == "disable":
            success = scheduler.disable_report(args.report_id)
            print(f"Report {'disabled' if success else 'not found'}")
            
        elif args.command == "delete":
            success = scheduler.delete_report(args.report_id)
            print(f"Report {'deleted' if success else 'not found'}")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_github(args):
    """Manage GitHub integration."""
    config = Config.from_env()
    
    if not config.github_token or not config.github_repo:
        print("Error: GitHub integration not configured")
        print("Set GITHUB_TOKEN and GITHUB_REPO environment variables")
        return 1
    
    try:
        github = GitHubPublisher(config)
        
        if args.command == "info":
            info = github.get_repository_info()
            print(f"Repository: {info['full_name']}")
            print(f"Description: {info['description']}")
            print(f"Language: {info['language']}")
            print(f"Stars: {info['stars']}")
            print(f"Forks: {info['forks']}")
            print(f"Open Issues: {info['open_issues']}")
            
        elif args.command == "publish":
            result = github.publish_file(
                local_file_path=args.file,
                github_file_path=args.path,
                commit_message=args.message or f"Upload {Path(args.file).name}"
            )
            print(f"File published: {result['content_url']}")
            
        elif args.command == "setup":
            result = github.setup_automated_reporting()
            print("Automated reporting workflow set up:")
            for instruction in result['instructions']:
                print(f"  - {instruction}")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="perplSDK - Python SDK for AI-powered research automation"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Execute a search query')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-tokens', type=int, default=1000, help='Maximum tokens')
    search_parser.add_argument('--temperature', type=float, default=0.2, help='Temperature')
    search_parser.add_argument('--recency', help='Recency filter (day, week, month)')
    search_parser.add_argument('--show-sources', action='store_true', help='Show sources')
    search_parser.set_defaults(func=cmd_search)
    
    # Research command
    research_parser = subparsers.add_parser('research', help='Execute research automation')
    research_parser.add_argument('name', help='Project name')
    research_parser.add_argument('--description', help='Project description')
    research_parser.add_argument('--queries', nargs='+', help='Research queries')
    research_parser.add_argument('--topic', help='Research topic (auto-generate queries)')
    research_parser.add_argument('--research-type', default='comprehensive', 
                                help='Research type (comprehensive, competitive, market, technical)')
    research_parser.add_argument('--industry', help='Industry context')
    research_parser.add_argument('--parallel', action='store_true', default=True, help='Parallel execution')
    research_parser.add_argument('--output', help='Output report filename')
    research_parser.add_argument('--output-dir', default='./reports', help='Output directory')
    research_parser.set_defaults(func=cmd_research)
    
    # Market intelligence command
    market_parser = subparsers.add_parser('market', help='Market intelligence analysis')
    market_parser.add_argument('sector', help='Market sector')
    market_parser.add_argument('--analysis-type', default='comprehensive',
                              help='Analysis type (comprehensive, trends, competitive, opportunities, risks)')
    market_parser.add_argument('--time-frame', default='current', help='Time frame')
    market_parser.add_argument('--geographic-focus', help='Geographic focus')
    market_parser.add_argument('--output', help='Output report filename')
    market_parser.add_argument('--output-dir', default='./reports', help='Output directory')
    market_parser.set_defaults(func=cmd_market_intel)
    
    # Trends command
    trends_parser = subparsers.add_parser('trends', help='Trend monitoring')
    trends_subparsers = trends_parser.add_subparsers(dest='command')
    
    # Trends detect
    detect_parser = trends_subparsers.add_parser('detect', help='Detect emerging trends')
    detect_parser.add_argument('domains', nargs='+', help='Search domains')
    detect_parser.add_argument('--time-window', default='month', help='Time window')
    detect_parser.add_argument('--output', help='Output report filename')
    detect_parser.add_argument('--output-dir', default='./reports', help='Output directory')
    
    # Trends monitor
    monitor_parser = trends_subparsers.add_parser('monitor', help='Monitor trend evolution')
    monitor_parser.add_argument('topic', help='Trend topic to monitor')
    monitor_parser.add_argument('--days-back', type=int, default=30, help='Days to look back')
    
    trends_parser.set_defaults(func=cmd_trends)
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Manage report scheduling')
    schedule_subparsers = schedule_parser.add_subparsers(dest='command')
    
    # Schedule list
    schedule_subparsers.add_parser('list', help='List scheduled reports')
    
    # Schedule add
    add_parser = schedule_subparsers.add_parser('add', help='Add scheduled report')
    add_parser.add_argument('name', help='Report name')
    add_parser.add_argument('type', help='Report type')
    add_parser.add_argument('frequency', help='Frequency (daily, weekly, monthly)')
    add_parser.add_argument('--topic', help='Research topic')
    add_parser.add_argument('--github', action='store_true', help='Publish to GitHub')
    
    # Schedule run
    run_parser = schedule_subparsers.add_parser('run', help='Run report now')
    run_parser.add_argument('report_id', help='Report ID')
    
    # Schedule enable/disable
    enable_parser = schedule_subparsers.add_parser('enable', help='Enable report')
    enable_parser.add_argument('report_id', help='Report ID')
    
    disable_parser = schedule_subparsers.add_parser('disable', help='Disable report')
    disable_parser.add_argument('report_id', help='Report ID')
    
    delete_parser = schedule_subparsers.add_parser('delete', help='Delete report')
    delete_parser.add_argument('report_id', help='Report ID')
    
    schedule_parser.set_defaults(func=cmd_schedule)
    
    # GitHub command
    github_parser = subparsers.add_parser('github', help='GitHub integration')
    github_subparsers = github_parser.add_subparsers(dest='command')
    
    # GitHub info
    github_subparsers.add_parser('info', help='Show repository info')
    
    # GitHub publish
    publish_parser = github_subparsers.add_parser('publish', help='Publish file')
    publish_parser.add_argument('file', help='Local file path')
    publish_parser.add_argument('path', help='GitHub file path')
    publish_parser.add_argument('--message', help='Commit message')
    
    # GitHub setup
    github_subparsers.add_parser('setup', help='Set up automated reporting')
    
    github_parser.set_defaults(func=cmd_github)
    
    # Parse arguments and execute
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())