#!/usr/bin/env python3
"""
COPILOT - Super Fast Performance Intelligence Demo

This example demonstrates how to use the COPILOT feature to conduct
super fast performance intelligence analysis across different contexts.

Usage:
    python examples/copilot_performance_intelligence.py
"""

from perplSDK.core.config import Config
from perplSDK.research.market_intelligence import MarketIntelligence
from perplSDK.reports.formatter import MarkdownFormatter
from datetime import datetime
import os


def demo_general_performance():
    """Demo: General high-performance technology analysis."""
    print("\n" + "="*70)
    print("🚀 DEMO 1: General Performance Intelligence")
    print("="*70)
    
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    
    print("\n📊 Conducting general performance intelligence analysis...")
    
    analysis = market_intel.conduct_performance_intelligence(
        context="general",
        time_frame="current",
        geographic_focus="global"
    )
    
    print_performance_summary(analysis)
    return analysis


def demo_ev_performance():
    """Demo: EV-specific performance intelligence."""
    print("\n" + "="*70)
    print("⚡ DEMO 2: EV Performance Intelligence")
    print("="*70)
    
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    
    print("\n📊 Conducting EV performance intelligence analysis...")
    
    analysis = market_intel.conduct_performance_intelligence(
        context="ev",
        time_frame="current",
        custom_queries=[
            "Latest EV 0-60 mph acceleration improvements",
            "Fast charging breakthrough technologies 2024"
        ]
    )
    
    print_performance_summary(analysis)
    return analysis


def demo_manufacturing_performance():
    """Demo: Manufacturing performance optimization."""
    print("\n" + "="*70)
    print("🏭 DEMO 3: Manufacturing Performance Intelligence")
    print("="*70)
    
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    
    print("\n📊 Conducting manufacturing performance intelligence analysis...")
    
    analysis = market_intel.conduct_performance_intelligence(
        context="manufacturing",
        time_frame="current",
        geographic_focus="north_america"
    )
    
    print_performance_summary(analysis)
    return analysis


def demo_operations_performance():
    """Demo: Operations and workflow performance."""
    print("\n" + "="*70)
    print("📈 DEMO 4: Operations Performance Intelligence")
    print("="*70)
    
    config = Config.from_env()
    market_intel = MarketIntelligence(config)
    
    print("\n📊 Conducting operations performance intelligence analysis...")
    
    analysis = market_intel.conduct_performance_intelligence(
        context="operations",
        time_frame="current",
        custom_queries=[
            "Rapid decision-making frameworks",
            "Workflow automation performance metrics"
        ]
    )
    
    print_performance_summary(analysis)
    return analysis


def print_performance_summary(analysis):
    """Print a summary of the performance analysis."""
    print("\n✅ Analysis Complete!")
    print(f"\n📋 Analysis Details:")
    print(f"   Intelligence Type: {analysis['intelligence_type']}")
    print(f"   Context: {analysis['context']}")
    print(f"   Time Frame: {analysis['time_frame']}")
    
    metrics = analysis.get('performance_metrics', {})
    print(f"\n📊 Performance Metrics:")
    print(f"   Total Insights: {metrics.get('total_insights', 0)}")
    print(f"   Super Fast: {metrics.get('super_fast_count', 0)} ({metrics.get('super_fast_percentage', 0)}%)")
    print(f"   Fast: {metrics.get('fast_count', 0)}")
    print(f"   High Impact: {metrics.get('high_impact_count', 0)}")
    print(f"   Avg Confidence: {metrics.get('average_confidence', 0):.1%}")
    
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")
    
    insights = analysis.get('insights', [])
    super_fast = [i for i in insights if i.get('performance_level') == 'super_fast']
    if super_fast:
        print(f"\n⚡ Super Fast Performance Highlights:")
        for i, insight in enumerate(super_fast[:2], 1):
            print(f"   {i}. {insight.get('title', 'N/A')}")
            tags = insight.get('tags', [])
            if tags:
                print(f"      Tags: {', '.join(tags[:3])}")


def save_performance_report(analysis, filename):
    """Save performance intelligence report to file."""
    formatter = MarkdownFormatter()
    
    # Create report content
    report_lines = []
    report_lines.append(f"# Super Fast Performance Intelligence Report")
    report_lines.append(f"")
    report_lines.append(f"**Analysis ID:** {analysis['analysis_name']}")
    report_lines.append(f"**Intelligence Type:** {analysis['intelligence_type']}")
    report_lines.append(f"**Context:** {analysis['context']}")
    report_lines.append(f"**Generated:** {analysis['generated_at']}")
    report_lines.append(f"")
    
    # Performance Metrics
    metrics = analysis.get('performance_metrics', {})
    report_lines.append(f"## 📊 Performance Metrics")
    report_lines.append(f"")
    report_lines.append(f"| Metric | Value |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Total Insights | {metrics.get('total_insights', 0)} |")
    report_lines.append(f"| Super Fast Insights | {metrics.get('super_fast_count', 0)} ({metrics.get('super_fast_percentage', 0)}%) |")
    report_lines.append(f"| Fast Insights | {metrics.get('fast_count', 0)} |")
    report_lines.append(f"| High Impact Insights | {metrics.get('high_impact_count', 0)} |")
    report_lines.append(f"| Average Confidence | {metrics.get('average_confidence', 0):.1%} |")
    report_lines.append(f"")
    
    # Recommendations
    recommendations = analysis.get('recommendations', [])
    report_lines.append(f"## 💡 Strategic Recommendations")
    report_lines.append(f"")
    for i, rec in enumerate(recommendations, 1):
        report_lines.append(f"{i}. {rec}")
    report_lines.append(f"")
    
    # Top Insights
    insights = analysis.get('insights', [])
    super_fast = [i for i in insights if i.get('performance_level') == 'super_fast']
    
    if super_fast:
        report_lines.append(f"## ⚡ Super Fast Performance Insights")
        report_lines.append(f"")
        for i, insight in enumerate(super_fast[:5], 1):
            report_lines.append(f"### {i}. {insight.get('title', 'N/A')}")
            report_lines.append(f"")
            report_lines.append(f"**Impact Level:** {insight.get('impact_level', 'N/A')}")
            report_lines.append(f"**Confidence:** {insight.get('confidence_score', 0):.1%}")
            report_lines.append(f"")
            report_lines.append(insight.get('content', 'N/A'))
            report_lines.append(f"")
            if insight.get('tags'):
                report_lines.append(f"*Tags: {', '.join(insight['tags'])}*")
                report_lines.append(f"")
    
    report_lines.append(f"---")
    report_lines.append(f"*Report generated by perplSDK COPILOT*")
    
    report_content = "\n".join(report_lines)
    
    # Save report
    os.makedirs("./reports", exist_ok=True)
    report_path = formatter.save_report(
        report_content,
        filename,
        "./reports"
    )
    
    return report_path


def main():
    """Main demo execution."""
    print("\n" + "="*70)
    print("🚀 COPILOT - Super Fast Performance Intelligence Demo")
    print("="*70)
    print("\nThis demo showcases the COPILOT feature for conducting")
    print("performance intelligence analysis across multiple contexts.")
    print("\nNote: This requires a valid Perplexity API key.")
    
    try:
        # Demo 1: General Performance
        general_analysis = demo_general_performance()
        
        # Demo 2: EV Performance
        ev_analysis = demo_ev_performance()
        
        # Demo 3: Manufacturing Performance
        mfg_analysis = demo_manufacturing_performance()
        
        # Demo 4: Operations Performance
        ops_analysis = demo_operations_performance()
        
        # Save comprehensive report
        print("\n" + "="*70)
        print("💾 Saving Comprehensive Performance Intelligence Report")
        print("="*70)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save each analysis
        reports = []
        reports.append(save_performance_report(
            general_analysis,
            f"copilot_general_{timestamp}"
        ))
        reports.append(save_performance_report(
            ev_analysis,
            f"copilot_ev_{timestamp}"
        ))
        reports.append(save_performance_report(
            mfg_analysis,
            f"copilot_manufacturing_{timestamp}"
        ))
        reports.append(save_performance_report(
            ops_analysis,
            f"copilot_operations_{timestamp}"
        ))
        
        print("\n✅ Reports saved:")
        for report in reports:
            print(f"   📄 {report}")
        
        print("\n" + "="*70)
        print("✅ COPILOT Demo Complete!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Set PERPLEXITY_API_KEY environment variable")
        print("  2. Installed perplSDK: pip install -e .")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
