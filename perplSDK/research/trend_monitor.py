"""Trend monitoring and analysis for technology and market developments."""

import json
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path

from ..core.client import PerplexityClient
from ..core.config import Config
from .automation import ResearchAutomation
from ..utils.formatters import TextFormatter


@dataclass
class TrendData:
    """Data structure for trend information."""
    topic: str
    trend_type: str  # emerging, growing, declining, stable
    confidence_score: float
    momentum: str  # accelerating, steady, slowing
    timeframe: str  # short_term, medium_term, long_term
    key_indicators: List[str]
    related_topics: List[str]
    sources: List[str]
    first_detected: datetime
    last_updated: datetime
    impact_assessment: str  # high, medium, low
    geographic_scope: str  # global, regional, local


class TrendMonitor:
    """Monitor and analyze technology and market trends."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize trend monitor.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config.from_env()
        self.client = PerplexityClient(self.config)
        self.research = ResearchAutomation(self.config)
        self.formatter = TextFormatter()
        
        # Storage for tracked trends
        self.tracked_trends: Dict[str, TrendData] = {}
        self.trend_history: List[Dict[str, Any]] = []
        
        # Default trend categories for EV industry
        self.ev_trend_categories = [
            "battery_technology",
            "charging_infrastructure", 
            "autonomous_driving",
            "ev_adoption",
            "policy_regulations",
            "market_competition",
            "sustainability",
            "supply_chain"
        ]
    
    def add_trend_to_monitor(
        self,
        topic: str,
        category: Optional[str] = None,
        monitoring_frequency: str = "weekly"
    ) -> None:
        """Add a new trend topic to monitor.
        
        Args:
            topic: Trend topic to monitor
            category: Category classification
            monitoring_frequency: How often to check (daily, weekly, monthly)
        """
        trend_id = self._generate_trend_id(topic)
        
        initial_trend = TrendData(
            topic=topic,
            trend_type="unknown",
            confidence_score=0.0,
            momentum="unknown",
            timeframe="unknown",
            key_indicators=[],
            related_topics=[],
            sources=[],
            first_detected=datetime.now(),
            last_updated=datetime.now(),
            impact_assessment="unknown",
            geographic_scope="unknown"
        )
        
        self.tracked_trends[trend_id] = initial_trend
    
    def detect_emerging_trends(
        self,
        search_domains: Optional[List[str]] = None,
        time_window: str = "month"
    ) -> List[Dict[str, Any]]:
        """Detect emerging trends in specified domains.
        
        Args:
            search_domains: Domains to search for trends
            time_window: Time window for trend detection
            
        Returns:
            List of detected emerging trends
        """
        if not search_domains:
            search_domains = [
                "electric vehicles",
                "battery technology", 
                "clean energy",
                "automotive innovation",
                "mobility technology"
            ]
        
        emerging_trends = []
        
        for domain in search_domains:
            try:
                # Generate trend detection queries
                queries = self._generate_trend_detection_queries(domain, time_window)
                
                # Create research project
                project_name = f"trend_detection_{domain.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
                project = self.research.create_project(
                    project_name,
                    f"Trend detection for {domain}"
                )
                
                # Add queries
                for query in queries:
                    project.add_query(
                        query,
                        category="trend_detection",
                        recency_filter=time_window
                    )
                
                # Conduct research
                project = self.research.conduct_research(project_name, parallel=True)
                
                # Analyze results for trends
                domain_trends = self._analyze_trend_signals(project, domain)
                emerging_trends.extend(domain_trends)
                
            except Exception as e:
                print(f"Error detecting trends for {domain}: {e}")
                continue
        
        # Deduplicate and rank trends
        return self._rank_and_filter_trends(emerging_trends)
    
    def _generate_trend_detection_queries(self, domain: str, time_window: str) -> List[str]:
        """Generate queries for trend detection."""
        time_modifier = {
            "week": "this week",
            "month": "this month", 
            "quarter": "this quarter",
            "year": "this year"
        }.get(time_window, "recently")
        
        queries = [
            f"What are the latest breakthrough innovations in {domain} {time_modifier}?",
            f"Emerging technologies and trends in {domain} industry {time_modifier}",
            f"New developments and announcements in {domain} {time_modifier}",
            f"Rising companies and startups in {domain} space {time_modifier}",
            f"Investment and funding trends in {domain} {time_modifier}",
            f"Research breakthroughs and scientific advances in {domain} {time_modifier}",
            f"Patent activity and intellectual property trends in {domain} {time_modifier}",
            f"Consumer behavior changes related to {domain} {time_modifier}"
        ]
        
        return queries
    
    def _analyze_trend_signals(self, project, domain: str) -> List[Dict[str, Any]]:
        """Analyze research results for trend signals."""
        trends = []
        
        # Combine all content for analysis
        all_content = " ".join([result.content for result in project.results if result.model != "error"])
        all_sources = []
        for result in project.results:
            all_sources.extend(result.sources)
        
        if not all_content:
            return trends
        
        # Extract potential trend topics
        trend_indicators = self._extract_trend_indicators(all_content)
        
        for indicator in trend_indicators:
            trend = {
                "topic": indicator["topic"],
                "domain": domain,
                "trend_type": indicator["type"],
                "confidence_score": indicator["confidence"],
                "key_signals": indicator["signals"],
                "sources": list(set(all_sources))[:10],  # Top 10 unique sources
                "detected_at": datetime.now().isoformat(),
                "context": indicator["context"]
            }
            trends.append(trend)
        
        return trends
    
    def _extract_trend_indicators(self, content: str) -> List[Dict[str, Any]]:
        """Extract trend indicators from content."""
        indicators = []
        
        # Keywords that indicate emerging trends
        emerging_keywords = [
            "breakthrough", "revolutionary", "game-changing", "disruptive",
            "emerging", "rising", "growing", "increasing", "surge",
            "boom", "expansion", "adoption", "mainstream"
        ]
        
        # Keywords that indicate declining trends
        declining_keywords = [
            "declining", "decreasing", "dropping", "falling", "slowing",
            "obsolete", "replaced", "discontinued", "phase out"
        ]
        
        # Split content into sentences for analysis
        sentences = content.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip().lower()
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            # Check for trend indicators
            confidence = 0.0
            trend_type = "stable"
            signals = []
            
            for keyword in emerging_keywords:
                if keyword in sentence:
                    confidence += 0.1
                    trend_type = "emerging"
                    signals.append(keyword)
            
            for keyword in declining_keywords:
                if keyword in sentence:
                    confidence += 0.1
                    trend_type = "declining"
                    signals.append(keyword)
            
            # Extract potential topic (simplified extraction)
            if confidence > 0.2:
                # Try to extract the main topic from the sentence
                topic = self._extract_topic_from_sentence(sentence)
                if topic:
                    indicators.append({
                        "topic": topic,
                        "type": trend_type,
                        "confidence": min(confidence, 1.0),
                        "signals": list(set(signals)),
                        "context": sentence[:200]
                    })
        
        return indicators[:10]  # Return top 10 indicators
    
    def _extract_topic_from_sentence(self, sentence: str) -> Optional[str]:
        """Extract main topic from a sentence (simplified)."""
        # Remove common words
        common_words = {
            "the", "is", "are", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "this", "that", "these", "those"
        }
        
        words = sentence.split()
        filtered_words = [w for w in words if w.lower() not in common_words and len(w) > 3]
        
        if len(filtered_words) >= 2:
            return " ".join(filtered_words[:3])  # Take first 3 meaningful words
        
        return None
    
    def _rank_and_filter_trends(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank and filter detected trends."""
        # Remove duplicates based on similar topics
        unique_trends = {}
        
        for trend in trends:
            topic_key = trend["topic"].lower().replace(" ", "_")
            
            if topic_key not in unique_trends:
                unique_trends[topic_key] = trend
            else:
                # Keep the one with higher confidence
                if trend["confidence_score"] > unique_trends[topic_key]["confidence_score"]:
                    unique_trends[topic_key] = trend
        
        # Sort by confidence score
        ranked_trends = sorted(
            unique_trends.values(),
            key=lambda x: x["confidence_score"],
            reverse=True
        )
        
        return ranked_trends[:20]  # Return top 20 trends
    
    def monitor_trend_evolution(self, trend_topic: str, days_back: int = 30) -> Dict[str, Any]:
        """Monitor how a specific trend has evolved over time.
        
        Args:
            trend_topic: Topic to monitor
            days_back: Number of days to look back
            
        Returns:
            Trend evolution analysis
        """
        queries = [
            f"{trend_topic} developments in the last {days_back} days",
            f"Recent progress and updates on {trend_topic}",
            f"Latest news and announcements about {trend_topic}",
            f"Market response and adoption of {trend_topic}",
            f"Expert opinions and analysis on {trend_topic} trend"
        ]
        
        # Create research project
        project_name = f"trend_evolution_{trend_topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        project = self.research.create_project(
            project_name,
            f"Evolution analysis for {trend_topic}"
        )
        
        # Add queries
        for query in queries:
            project.add_query(
                query,
                category="trend_evolution",
                recency_filter="month"
            )
        
        # Conduct research
        project = self.research.conduct_research(project_name, parallel=True)
        
        # Analyze evolution
        evolution_data = self._analyze_trend_evolution(project, trend_topic)
        
        return {
            "trend_topic": trend_topic,
            "analysis_period": f"{days_back} days",
            "analyzed_at": datetime.now().isoformat(),
            "evolution_data": evolution_data,
            "project_data": project.to_dict()
        }
    
    def _analyze_trend_evolution(self, project, trend_topic: str) -> Dict[str, Any]:
        """Analyze trend evolution from research results."""
        all_content = " ".join([result.content for result in project.results if result.model != "error"])
        
        if not all_content:
            return {"error": "No content to analyze"}
        
        # Extract key developments
        key_points = self.formatter.extract_key_points(all_content, max_points=10)
        
        # Assess momentum
        momentum_indicators = {
            "accelerating": ["accelerating", "rapid", "fast", "quick", "surge", "boom"],
            "steady": ["steady", "consistent", "stable", "gradual", "continuous"],
            "slowing": ["slowing", "declining", "reduced", "dropping", "stagnant"]
        }
        
        momentum_scores = {}
        content_lower = all_content.lower()
        
        for momentum, indicators in momentum_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            momentum_scores[momentum] = score
        
        current_momentum = max(momentum_scores, key=momentum_scores.get)
        
        return {
            "key_developments": key_points,
            "momentum": current_momentum,
            "momentum_confidence": momentum_scores[current_momentum] / sum(momentum_scores.values()) if sum(momentum_scores.values()) > 0 else 0,
            "content_summary": self.formatter.create_summary(all_content, max_length=500),
            "analysis_depth": len(project.results),
            "source_diversity": len(set([source for result in project.results for source in result.sources]))
        }
    
    def generate_trend_report(self, trends: List[Dict[str, Any]], report_type: str = "summary") -> str:
        """Generate a formatted trend report.
        
        Args:
            trends: List of trend data
            report_type: Type of report (summary, detailed, executive)
            
        Returns:
            Formatted report string
        """
        if not trends:
            return "No trends to report."
        
        report_lines = []
        
        # Header
        report_lines.append(f"# Trend Analysis Report")
        report_lines.append(f"Generated: {self.formatter.format_timestamp()}")
        report_lines.append(f"Total Trends Analyzed: {len(trends)}")
        report_lines.append("")
        
        # Executive Summary
        if report_type in ["summary", "executive"]:
            emerging_count = len([t for t in trends if t.get("trend_type") == "emerging"])
            declining_count = len([t for t in trends if t.get("trend_type") == "declining"])
            
            report_lines.append("## Executive Summary")
            report_lines.append(f"- Emerging Trends: {emerging_count}")
            report_lines.append(f"- Declining Trends: {declining_count}")
            report_lines.append(f"- Stable Trends: {len(trends) - emerging_count - declining_count}")
            report_lines.append("")
        
        # Trend Details
        report_lines.append("## Trend Analysis")
        
        for i, trend in enumerate(trends[:10], 1):  # Top 10 trends
            report_lines.append(f"### {i}. {trend.get('topic', 'Unknown Topic')}")
            report_lines.append(f"**Type:** {trend.get('trend_type', 'Unknown')}")
            report_lines.append(f"**Confidence:** {trend.get('confidence_score', 0):.1%}")
            
            if report_type == "detailed":
                if trend.get('key_signals'):
                    report_lines.append(f"**Key Signals:** {', '.join(trend['key_signals'])}")
                
                if trend.get('context'):
                    context = self.formatter.truncate_text(trend['context'], 200)
                    report_lines.append(f"**Context:** {context}")
            
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _generate_trend_id(self, topic: str) -> str:
        """Generate a unique ID for a trend topic."""
        return topic.lower().replace(" ", "_").replace("-", "_")
    
    def save_trends(self, filepath: Optional[str] = None) -> str:
        """Save tracked trends to file.
        
        Args:
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if not filepath:
            output_dir = Path(self.config.default_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            filepath = output_dir / f"trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert trends to serializable format
        trends_data = {}
        for trend_id, trend_data in self.tracked_trends.items():
            trends_data[trend_id] = asdict(trend_data)
            # Convert datetime objects to ISO strings
            trends_data[trend_id]["first_detected"] = trend_data.first_detected.isoformat()
            trends_data[trend_id]["last_updated"] = trend_data.last_updated.isoformat()
        
        save_data = {
            "trends": trends_data,
            "history": self.trend_history,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)