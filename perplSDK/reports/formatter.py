"""Markdown formatting utilities for research reports."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from ..core.client import SearchResult
from ..utils.formatters import TextFormatter


class MarkdownFormatter:
    """Format research results and reports as Markdown."""
    
    def __init__(self):
        self.text_formatter = TextFormatter()
    
    def format_research_report(
        self,
        project_name: str,
        results: List[SearchResult],
        metadata: Optional[Dict[str, Any]] = None,
        include_sources: bool = True,
        include_citations: bool = True
    ) -> str:
        """Format research results as a comprehensive Markdown report.
        
        Args:
            project_name: Name of the research project
            results: List of search results
            metadata: Additional metadata for the report
            include_sources: Whether to include sources section
            include_citations: Whether to include citations
            
        Returns:
            Formatted Markdown report
        """
        lines = []
        
        # Header
        lines.append(f"# {project_name}")
        lines.append("")
        lines.append(f"**Generated:** {self.text_formatter.format_timestamp()}")
        
        if metadata:
            lines.append(f"**Description:** {metadata.get('description', 'N/A')}")
            lines.append(f"**Total Queries:** {metadata.get('total_queries', len(results))}")
            lines.append(f"**Analysis Type:** {metadata.get('analysis_type', 'Research')}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        if results:
            summary_content = self._generate_executive_summary(results)
            lines.append("## Executive Summary")
            lines.append("")
            lines.append(summary_content)
            lines.append("")
        
        # Key Findings
        lines.append("## Key Findings")
        lines.append("")
        
        for i, result in enumerate(results, 1):
            if result.model == "error":
                continue
                
            lines.append(f"### Finding {i}")
            lines.append("")
            
            # Format content
            content = self.text_formatter.clean_content(result.content)
            if len(content) > 1000:
                # Create summary for long content
                summary = self.text_formatter.create_summary(content, max_length=800)
                lines.append(summary)
                lines.append("")
                lines.append(f"<details>")
                lines.append(f"<summary>View Full Details</summary>")
                lines.append("")
                lines.append(content)
                lines.append("")
                lines.append(f"</details>")
            else:
                lines.append(content)
            
            lines.append("")
            
            # Add model info
            lines.append(f"*Source: {result.model}*")
            lines.append("")
        
        # Sources section
        if include_sources and any(result.sources for result in results):
            lines.append("## Sources")
            lines.append("")
            
            all_sources = []
            for result in results:
                all_sources.extend(result.sources)
            
            # Remove duplicates while preserving order
            unique_sources = []
            seen = set()
            for source in all_sources:
                if source not in seen:
                    unique_sources.append(source)
                    seen.add(source)
            
            for i, source in enumerate(unique_sources[:20], 1):  # Limit to top 20
                lines.append(f"{i}. {source}")
            
            lines.append("")
        
        # Citations section
        if include_citations and any(result.citations for result in results):
            lines.append("## Citations")
            lines.append("")
            
            citation_count = 1
            for result in results:
                for citation in result.citations:
                    lines.append(f"{citation_count}. {citation}")
                    citation_count += 1
            
            lines.append("")
        
        # Usage statistics
        if any(result.usage for result in results):
            lines.append("## Usage Statistics")
            lines.append("")
            
            total_tokens = sum(result.usage.get('total_tokens', 0) for result in results)
            total_completion_tokens = sum(result.usage.get('completion_tokens', 0) for result in results)
            
            lines.append(f"- **Total Tokens Used:** {total_tokens:,}")
            lines.append(f"- **Completion Tokens:** {total_completion_tokens:,}")
            lines.append(f"- **Successful Queries:** {len([r for r in results if r.model != 'error'])}/{len(results)}")
            lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(f"*Report generated by perplSDK on {self.text_formatter.format_timestamp()}*")
        
        return "\n".join(lines)
    
    def format_market_intelligence_report(
        self,
        analysis_data: Dict[str, Any],
        include_recommendations: bool = True
    ) -> str:
        """Format market intelligence analysis as Markdown report.
        
        Args:
            analysis_data: Market analysis data
            include_recommendations: Whether to include recommendations
            
        Returns:
            Formatted Markdown report
        """
        lines = []
        
        # Header
        lines.append(f"# Market Intelligence Report")
        lines.append(f"## {analysis_data.get('sector', 'Market').replace('_', ' ').title()} Analysis")
        lines.append("")
        
        # Metadata
        lines.append(f"**Generated:** {analysis_data.get('generated_at', 'N/A')}")
        lines.append(f"**Analysis Type:** {analysis_data.get('analysis_type', 'N/A')}")
        lines.append(f"**Time Frame:** {analysis_data.get('time_frame', 'N/A')}")
        lines.append(f"**Geographic Focus:** {analysis_data.get('geographic_focus', 'Global')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        insights = analysis_data.get('insights', [])
        if insights:
            high_impact = [i for i in insights if i.get('impact_level') == 'high']
            immediate = [i for i in insights if i.get('time_relevance') == 'immediate']
            
            lines.append("## Executive Summary")
            lines.append("")
            lines.append(f"This analysis identified **{len(insights)}** key market insights, including:")
            lines.append(f"- **{len(high_impact)}** high-impact developments")
            lines.append(f"- **{len(immediate)}** immediate-action items")
            lines.append("")
        
        # Key Insights
        if insights:
            lines.append("## Key Market Insights")
            lines.append("")
            
            # Group insights by impact level
            insight_groups = {
                'high': [i for i in insights if i.get('impact_level') == 'high'],
                'medium': [i for i in insights if i.get('impact_level') == 'medium'],
                'low': [i for i in insights if i.get('impact_level') == 'low']
            }
            
            for impact_level, level_insights in insight_groups.items():
                if level_insights:
                    lines.append(f"### {impact_level.title()} Impact Insights")
                    lines.append("")
                    
                    for i, insight in enumerate(level_insights, 1):
                        lines.append(f"#### {i}. {insight.get('title', f'Insight {i}')}")
                        lines.append("")
                        
                        content = insight.get('content', '')
                        if content:
                            summary = self.text_formatter.create_summary(content, max_length=400)
                            lines.append(summary)
                            lines.append("")
                        
                        # Metadata
                        lines.append(f"**Time Relevance:** {insight.get('time_relevance', 'N/A')}")
                        lines.append(f"**Confidence Score:** {insight.get('confidence_score', 0):.1%}")
                        
                        if insight.get('tags'):
                            lines.append(f"**Tags:** {', '.join(insight['tags'])}")
                        
                        lines.append("")
        
        # Recommendations
        recommendations = analysis_data.get('recommendations', [])
        if include_recommendations and recommendations:
            lines.append("## Strategic Recommendations")
            lines.append("")
            
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")
            
            lines.append("")
        
        # Data Summary
        lines.append("## Analysis Summary")
        lines.append("")
        lines.append(f"- **Total Queries Executed:** {analysis_data.get('total_queries', 'N/A')}")
        lines.append(f"- **Successful Results:** {analysis_data.get('total_results', 'N/A')}")
        lines.append(f"- **Analysis Scope:** {analysis_data.get('sector', 'N/A').replace('_', ' ').title()}")
        lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(f"*Market Intelligence Report generated by perplSDK*")
        lines.append(f"*Analysis conducted on {analysis_data.get('generated_at', 'N/A')}*")
        
        return "\n".join(lines)
    
    def format_trend_report(
        self,
        trends: List[Dict[str, Any]],
        report_title: str = "Trend Analysis Report",
        include_detailed_analysis: bool = True
    ) -> str:
        """Format trend analysis as Markdown report.
        
        Args:
            trends: List of trend data
            report_title: Title for the report
            include_detailed_analysis: Whether to include detailed analysis
            
        Returns:
            Formatted Markdown report
        """
        lines = []
        
        # Header
        lines.append(f"# {report_title}")
        lines.append("")
        lines.append(f"**Generated:** {self.text_formatter.format_timestamp()}")
        lines.append(f"**Total Trends Analyzed:** {len(trends)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        if not trends:
            lines.append("No trends identified in the analysis period.")
            return "\n".join(lines)
        
        # Trend Categories
        trend_types = {}
        for trend in trends:
            trend_type = trend.get('trend_type', 'unknown')
            if trend_type not in trend_types:
                trend_types[trend_type] = []
            trend_types[trend_type].append(trend)
        
        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        
        for trend_type, type_trends in trend_types.items():
            lines.append(f"- **{trend_type.title()} Trends:** {len(type_trends)}")
        
        lines.append("")
        
        # High-confidence trends
        high_confidence_trends = [t for t in trends if t.get('confidence_score', 0) > 0.7]
        if high_confidence_trends:
            lines.append(f"**High-Confidence Trends:** {len(high_confidence_trends)} trends identified with >70% confidence")
            lines.append("")
        
        # Detailed Trend Analysis
        lines.append("## Trend Analysis")
        lines.append("")
        
        # Sort trends by confidence score
        sorted_trends = sorted(trends, key=lambda x: x.get('confidence_score', 0), reverse=True)
        
        for i, trend in enumerate(sorted_trends[:15], 1):  # Top 15 trends
            lines.append(f"### {i}. {trend.get('topic', 'Unknown Trend')}")
            lines.append("")
            
            # Basic info
            lines.append(f"**Type:** {trend.get('trend_type', 'Unknown').title()}")
            lines.append(f"**Confidence:** {trend.get('confidence_score', 0):.1%}")
            lines.append(f"**Domain:** {trend.get('domain', 'N/A')}")
            
            if trend.get('detected_at'):
                lines.append(f"**Detected:** {trend['detected_at']}")
            
            lines.append("")
            
            # Key signals
            if trend.get('key_signals'):
                lines.append(f"**Key Signals:** {', '.join(trend['key_signals'])}")
                lines.append("")
            
            # Context
            if include_detailed_analysis and trend.get('context'):
                context = self.text_formatter.truncate_text(trend['context'], 300)
                lines.append(f"**Context:** {context}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Methodology
        lines.append("## Methodology")
        lines.append("")
        lines.append("This trend analysis was conducted using:")
        lines.append("- Automated content analysis from multiple sources")
        lines.append("- Confidence scoring based on signal strength and frequency")
        lines.append("- Real-time trend detection algorithms")
        lines.append("- Multi-domain trend correlation analysis")
        lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(f"*Trend Analysis Report generated by perplSDK*")
        
        return "\n".join(lines)
    
    def _generate_executive_summary(self, results: List[SearchResult]) -> str:
        """Generate executive summary from research results."""
        if not results:
            return "No research results available for analysis."
        
        # Combine all content
        all_content = " ".join([
            result.content for result in results 
            if result.model != "error" and result.content
        ])
        
        if not all_content:
            return "No valid content available for summary."
        
        # Extract key points
        key_points = self.text_formatter.extract_key_points(all_content, max_points=5)
        
        if not key_points:
            # Fallback to simple summary
            return self.text_formatter.create_summary(all_content, max_length=500)
        
        # Format as bullet points
        summary_lines = ["Based on comprehensive research analysis, key findings include:"]
        summary_lines.append("")
        
        for point in key_points:
            summary_lines.append(f"- {point.strip()}")
        
        return "\n".join(summary_lines)
    
    def save_report(
        self,
        content: str,
        filename: str,
        output_dir: Optional[str] = None
    ) -> str:
        """Save Markdown report to file.
        
        Args:
            content: Markdown content to save
            filename: Filename (without extension)
            output_dir: Output directory (optional)
            
        Returns:
            Path to saved file
        """
        if not output_dir:
            output_dir = "./reports"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Create a Markdown table.
        
        Args:
            headers: Table headers
            rows: Table data rows
            
        Returns:
            Formatted Markdown table
        """
        if not headers or not rows:
            return ""
        
        lines = []
        
        # Header row
        lines.append("| " + " | ".join(headers) + " |")
        
        # Separator row
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # Data rows
        for row in rows:
            # Pad row to match header length
            padded_row = row + [""] * (len(headers) - len(row))
            lines.append("| " + " | ".join(padded_row[:len(headers)]) + " |")
        
        return "\n".join(lines)
    
    def create_collapsible_section(self, title: str, content: str) -> str:
        """Create a collapsible section in Markdown.
        
        Args:
            title: Section title
            content: Section content
            
        Returns:
            Formatted collapsible section
        """
        return f"""<details>
<summary>{title}</summary>

{content}

</details>"""