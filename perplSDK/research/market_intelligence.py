"""Market intelligence module for EV MAX INC and other organizations."""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..core.client import PerplexityClient
from ..core.config import Config
from .automation import ResearchAutomation


class MarketSector(Enum):
    """Market sectors for analysis."""
    ELECTRIC_VEHICLES = "electric_vehicles"
    AUTOMOTIVE = "automotive"
    CLEAN_ENERGY = "clean_energy"
    BATTERY_TECHNOLOGY = "battery_technology"
    CHARGING_INFRASTRUCTURE = "charging_infrastructure"
    AUTONOMOUS_VEHICLES = "autonomous_vehicles"
    MOBILITY_SERVICES = "mobility_services"
    ENERGY_STORAGE = "energy_storage"
    PERFORMANCE = "performance"


@dataclass 
class MarketInsight:
    """Market insight data structure."""
    title: str
    content: str
    sector: MarketSector
    impact_level: str  # high, medium, low
    time_relevance: str  # immediate, short_term, long_term
    sources: List[str]
    confidence_score: float
    generated_at: datetime
    tags: List[str] = None


class MarketIntelligence:
    """Market intelligence automation for comprehensive market analysis."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize market intelligence system.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config.from_env()
        self.client = PerplexityClient(self.config)
        self.research = ResearchAutomation(self.config)
        
        # EV MAX INC specific focus areas
        self.ev_max_focus_areas = [
            "electric vehicle market trends",
            "EV charging infrastructure development", 
            "battery technology innovations",
            "EV policy and regulations",
            "competitive landscape in EV industry",
            "consumer adoption patterns for EVs",
            "EV market share analysis",
            "sustainability trends in automotive"
        ]
    
    def generate_market_queries(
        self,
        sector: MarketSector,
        analysis_type: str = "comprehensive",
        time_frame: str = "current",
        geographic_focus: Optional[str] = None
    ) -> List[str]:
        """Generate market research queries for specific sector.
        
        Args:
            sector: Market sector to analyze
            analysis_type: Type of analysis (trends, competitive, opportunities, risks)
            time_frame: Time frame for analysis (current, quarterly, yearly, 5year)
            geographic_focus: Geographic region (global, north_america, europe, asia, etc.)
            
        Returns:
            List of research queries
        """
        sector_name = sector.value.replace("_", " ")
        geo_modifier = f"in {geographic_focus}" if geographic_focus else "globally"
        
        base_queries = {
            "trends": [
                f"Latest trends in {sector_name} market {geo_modifier} {time_frame}",
                f"Emerging technologies in {sector_name} industry {time_frame}",
                f"Market growth projections for {sector_name} {geo_modifier}",
                f"Key drivers of {sector_name} market growth {time_frame}",
                f"Disruptions and innovations in {sector_name} {time_frame}"
            ],
            "competitive": [
                f"Top companies in {sector_name} market {geo_modifier}",
                f"Market leaders and their strategies in {sector_name}",
                f"New entrants in {sector_name} industry {time_frame}",
                f"Competitive landscape analysis {sector_name} {time_frame}",
                f"Market share analysis {sector_name} {geo_modifier}"
            ],
            "opportunities": [
                f"Investment opportunities in {sector_name} {time_frame}",
                f"Untapped markets in {sector_name} {geo_modifier}",
                f"Partnership opportunities {sector_name} industry",
                f"Regulatory opportunities {sector_name} {time_frame}",
                f"Technology gaps and opportunities {sector_name}"
            ],
            "risks": [
                f"Market risks in {sector_name} industry {time_frame}",
                f"Regulatory challenges {sector_name} {geo_modifier}",
                f"Supply chain risks {sector_name} market",
                f"Technology risks and challenges {sector_name}",
                f"Economic factors affecting {sector_name} market"
            ],
            "comprehensive": []
        }
        
        if analysis_type == "comprehensive":
            # Combine all query types for comprehensive analysis
            queries = []
            for query_type in ["trends", "competitive", "opportunities", "risks"]:
                queries.extend(base_queries[query_type][:3])  # Take top 3 from each
            return queries
        
        return base_queries.get(analysis_type, base_queries["trends"])
    
    def conduct_market_analysis(
        self,
        sector: MarketSector,
        analysis_name: Optional[str] = None,
        analysis_type: str = "comprehensive",
        time_frame: str = "current",
        geographic_focus: Optional[str] = None,
        custom_queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Conduct comprehensive market analysis.
        
        Args:
            sector: Market sector to analyze
            analysis_name: Custom name for the analysis
            analysis_type: Type of analysis
            time_frame: Time frame for analysis
            geographic_focus: Geographic focus
            custom_queries: Optional custom queries to include
            
        Returns:
            Market analysis results
        """
        if not analysis_name:
            analysis_name = f"{sector.value}_{analysis_type}_{datetime.now().strftime('%Y%m%d')}"
        
        # Generate queries
        queries = self.generate_market_queries(
            sector, analysis_type, time_frame, geographic_focus
        )
        
        if custom_queries:
            queries.extend(custom_queries)
        
        # Create research project
        project = self.research.create_project(
            analysis_name,
            f"Market analysis for {sector.value} sector"
        )
        
        # Add queries to project
        for i, query in enumerate(queries):
            project.add_query(
                query,
                category=analysis_type,
                priority=len(queries) - i,  # Higher priority for earlier queries
                recency_filter="month" if time_frame == "current" else None
            )
        
        # Conduct research
        project = self.research.conduct_research(analysis_name, parallel=True)
        
        # Generate insights
        insights = self._extract_market_insights(project, sector)
        
        return {
            "analysis_name": analysis_name,
            "sector": sector.value,
            "analysis_type": analysis_type,
            "time_frame": time_frame,
            "geographic_focus": geographic_focus,
            "generated_at": datetime.now().isoformat(),
            "total_queries": len(queries),
            "total_results": len(project.results),
            "insights": insights,
            "project_data": project.to_dict()
        }
    
    def _extract_market_insights(
        self,
        project,
        sector: MarketSector
    ) -> List[Dict[str, Any]]:
        """Extract structured insights from research results."""
        insights = []
        
        for i, result in enumerate(project.results):
            if result.model == "error":
                continue
                
            # Simple insight extraction (could be enhanced with NLP)
            insight = {
                "title": f"Market Insight {i+1}",
                "content": result.content[:500] + "..." if len(result.content) > 500 else result.content,
                "sector": sector.value,
                "impact_level": self._assess_impact_level(result.content),
                "time_relevance": self._assess_time_relevance(result.content),
                "sources": result.sources,
                "confidence_score": self._calculate_confidence_score(result),
                "generated_at": datetime.now().isoformat(),
                "tags": self._extract_tags(result.content, sector)
            }
            insights.append(insight)
        
        return insights
    
    def _assess_impact_level(self, content: str) -> str:
        """Assess impact level based on content analysis."""
        high_impact_keywords = [
            "major", "significant", "breakthrough", "revolutionary", "disruptive",
            "substantial", "critical", "massive", "game-changing", "transformative"
        ]
        medium_impact_keywords = [
            "important", "notable", "considerable", "growing", "increasing",
            "emerging", "developing", "moderate", "steady"
        ]
        
        content_lower = content.lower()
        
        high_count = sum(1 for keyword in high_impact_keywords if keyword in content_lower)
        medium_count = sum(1 for keyword in medium_impact_keywords if keyword in content_lower)
        
        if high_count >= 2:
            return "high"
        elif medium_count >= 2 or high_count >= 1:
            return "medium"
        else:
            return "low"
    
    def _assess_time_relevance(self, content: str) -> str:
        """Assess time relevance based on content analysis."""
        immediate_keywords = [
            "now", "current", "today", "this week", "this month", "immediate",
            "urgent", "short-term", "near-term"
        ]
        long_term_keywords = [
            "future", "long-term", "years", "decade", "2030", "2040", "2050",
            "strategic", "roadmap", "vision"
        ]
        
        content_lower = content.lower()
        
        immediate_count = sum(1 for keyword in immediate_keywords if keyword in content_lower)
        long_term_count = sum(1 for keyword in long_term_keywords if keyword in content_lower)
        
        if immediate_count >= long_term_count and immediate_count > 0:
            return "immediate"
        elif long_term_count > immediate_count:
            return "long_term"
        else:
            return "short_term"
    
    def _calculate_confidence_score(self, result) -> float:
        """Calculate confidence score based on sources and content quality."""
        base_score = 0.5
        
        # Add score based on number of sources
        source_score = min(len(result.sources) * 0.1, 0.3)
        
        # Add score based on content length (more detailed = higher confidence)
        content_score = min(len(result.content) / 2000, 0.2)
        
        return min(base_score + source_score + content_score, 1.0)
    
    def _extract_tags(self, content: str, sector: MarketSector) -> List[str]:
        """Extract relevant tags from content."""
        sector_tags = {
            MarketSector.ELECTRIC_VEHICLES: [
                "EV", "electric", "battery", "charging", "tesla", "BYD", "sustainability",
                "range", "infrastructure", "adoption", "sales"
            ],
            MarketSector.BATTERY_TECHNOLOGY: [
                "lithium", "solid-state", "energy density", "charging speed", "cost",
                "recycling", "materials", "manufacturing", "breakthrough"
            ],
            MarketSector.CHARGING_INFRASTRUCTURE: [
                "charging stations", "fast charging", "network", "grid", "renewable",
                "urban", "highway", "home charging", "workplace"
            ],
            MarketSector.PERFORMANCE: [
                "speed", "performance", "efficiency", "optimization", "fast",
                "acceleration", "throughput", "benchmark", "metrics", "scalability"
            ]
        }
        
        content_lower = content.lower()
        tags = []
        
        relevant_keywords = sector_tags.get(sector, [])
        for keyword in relevant_keywords:
            if keyword.lower() in content_lower:
                tags.append(keyword)
        
        return tags[:5]  # Return top 5 tags
    
    def get_ev_max_insights(
        self,
        focus_area: Optional[str] = None,
        time_frame: str = "current"
    ) -> Dict[str, Any]:
        """Get insights specifically relevant to EV MAX INC.
        
        Args:
            focus_area: Specific focus area (optional)
            time_frame: Time frame for analysis
            
        Returns:
            EV MAX specific insights
        """
        if focus_area and focus_area not in self.ev_max_focus_areas:
            raise ValueError(f"Focus area must be one of: {self.ev_max_focus_areas}")
        
        queries = [focus_area] if focus_area else self.ev_max_focus_areas[:5]
        
        # Create research project
        project_name = f"ev_max_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project = self.research.create_project(
            project_name,
            "Market insights for EV MAX INC strategic planning"
        )
        
        # Add EV MAX specific context to queries
        enhanced_queries = []
        for query in queries:
            enhanced_queries.append(f"{query} market opportunities for electric vehicle companies")
            enhanced_queries.append(f"{query} competitive analysis and strategic implications")
        
        for i, query in enumerate(enhanced_queries):
            project.add_query(
                query,
                category="ev_max_strategic",
                priority=len(enhanced_queries) - i,
                recency_filter="month" if time_frame == "current" else None
            )
        
        # Conduct research
        project = self.research.conduct_research(project_name, parallel=True)
        
        # Generate EV MAX specific insights
        insights = self._extract_market_insights(project, MarketSector.ELECTRIC_VEHICLES)
        
        return {
            "company": "EV MAX INC",
            "analysis_type": "strategic_insights",
            "focus_area": focus_area or "comprehensive",
            "time_frame": time_frame,
            "generated_at": datetime.now().isoformat(),
            "insights": insights,
            "recommendations": self._generate_ev_max_recommendations(insights),
            "project_data": project.to_dict()
        }
    
    def _generate_ev_max_recommendations(self, insights: List[Dict[str, Any]]) -> List[str]:
        """Generate strategic recommendations for EV MAX INC based on insights."""
        recommendations = []
        
        high_impact_insights = [i for i in insights if i["impact_level"] == "high"]
        immediate_insights = [i for i in insights if i["time_relevance"] == "immediate"]
        
        if high_impact_insights:
            recommendations.append(
                f"Focus on {len(high_impact_insights)} high-impact market opportunities identified"
            )
        
        if immediate_insights:
            recommendations.append(
                f"Take immediate action on {len(immediate_insights)} time-sensitive market developments"
            )
        
        # Sector-specific recommendations
        ev_insights = [i for i in insights if "electric" in i["content"].lower()]
        if ev_insights:
            recommendations.append(
                "Leverage current electric vehicle market momentum for strategic positioning"
            )
        
        battery_insights = [i for i in insights if "battery" in i["content"].lower()]
        if battery_insights:
            recommendations.append(
                "Monitor battery technology developments for supply chain and product strategy"
            )
        
        if not recommendations:
            recommendations.append("Continue monitoring market developments for strategic opportunities")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def generate_performance_queries(
        self,
        context: str = "general",
        time_frame: str = "current",
        geographic_focus: Optional[str] = None
    ) -> List[str]:
        """Generate super fast performance intelligence queries.
        
        Args:
            context: Context for performance analysis (general, ev, manufacturing, operations)
            time_frame: Time frame for analysis
            geographic_focus: Geographic focus
            
        Returns:
            List of performance-focused research queries
        """
        geo_modifier = f"in {geographic_focus}" if geographic_focus else "globally"
        
        performance_queries = {
            "general": [
                f"Latest high-performance technology innovations {geo_modifier} {time_frame}",
                f"Breakthrough performance improvements in industry {time_frame}",
                f"Super fast performance optimization techniques {time_frame}",
                f"Performance benchmarking and metrics {geo_modifier}",
                f"Speed and efficiency improvements {time_frame}"
            ],
            "ev": [
                f"Latest EV performance improvements and speed records {time_frame}",
                f"Electric vehicle acceleration and performance benchmarks {geo_modifier}",
                f"Fast charging technology and performance {time_frame}",
                f"EV battery performance optimization {time_frame}",
                f"High-performance electric vehicle developments {geo_modifier}"
            ],
            "manufacturing": [
                f"Manufacturing process performance optimization {time_frame}",
                f"Production speed and efficiency improvements {geo_modifier}",
                f"Automation performance in manufacturing {time_frame}",
                f"Quality and performance metrics in manufacturing",
                f"Fast production techniques and methodologies {time_frame}"
            ],
            "operations": [
                f"Operational performance optimization strategies {time_frame}",
                f"Business process performance improvements {geo_modifier}",
                f"Workflow efficiency and speed optimization {time_frame}",
                f"Performance analytics and monitoring tools {time_frame}",
                f"Rapid decision-making and performance {geo_modifier}"
            ]
        }
        
        return performance_queries.get(context, performance_queries["general"])
    
    def conduct_performance_intelligence(
        self,
        context: str = "general",
        analysis_name: Optional[str] = None,
        time_frame: str = "current",
        geographic_focus: Optional[str] = None,
        custom_queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Conduct super fast performance intelligence analysis.
        
        Args:
            context: Context for performance analysis
            analysis_name: Custom name for the analysis
            time_frame: Time frame for analysis
            geographic_focus: Geographic focus
            custom_queries: Optional custom queries to include
            
        Returns:
            Performance intelligence results
        """
        if not analysis_name:
            analysis_name = f"performance_intel_{context}_{datetime.now().strftime('%Y%m%d')}"
        
        # Generate performance-focused queries
        queries = self.generate_performance_queries(context, time_frame, geographic_focus)
        
        if custom_queries:
            queries.extend(custom_queries)
        
        # Create research project
        project = self.research.create_project(
            analysis_name,
            f"Super Fast Performance Intelligence - {context}"
        )
        
        # Add queries to project with high priority
        for i, query in enumerate(queries):
            project.add_query(
                query,
                category="performance_intelligence",
                priority=len(queries) - i,
                recency_filter="month" if time_frame == "current" else None
            )
        
        # Conduct research with parallel execution for speed
        project = self.research.conduct_research(analysis_name, parallel=True)
        
        # Generate performance-specific insights
        insights = self._extract_performance_insights(project)
        
        return {
            "analysis_name": analysis_name,
            "intelligence_type": "super_fast_performance",
            "context": context,
            "time_frame": time_frame,
            "geographic_focus": geographic_focus,
            "generated_at": datetime.now().isoformat(),
            "total_queries": len(queries),
            "total_results": len(project.results),
            "insights": insights,
            "performance_metrics": self._calculate_performance_metrics(insights),
            "recommendations": self._generate_performance_recommendations(insights),
            "project_data": project.to_dict()
        }
    
    def _extract_performance_insights(self, project) -> List[Dict[str, Any]]:
        """Extract performance-specific insights from research results."""
        insights = []
        
        for i, result in enumerate(project.results):
            if result.model == "error":
                continue
            
            # Extract performance-focused insight
            insight = {
                "title": f"Performance Insight {i+1}",
                "content": result.content[:500] + "..." if len(result.content) > 500 else result.content,
                "performance_level": self._assess_performance_level(result.content),
                "impact_level": self._assess_impact_level(result.content),
                "time_relevance": self._assess_time_relevance(result.content),
                "sources": result.sources,
                "confidence_score": self._calculate_confidence_score(result),
                "generated_at": datetime.now().isoformat(),
                "tags": self._extract_performance_tags(result.content)
            }
            insights.append(insight)
        
        return insights
    
    def _assess_performance_level(self, content: str) -> str:
        """Assess performance level based on content analysis."""
        super_fast_keywords = [
            "super fast", "ultra-fast", "high-speed", "rapid", "instant",
            "record-breaking", "breakthrough", "fastest", "quickest", "acceleration"
        ]
        fast_keywords = [
            "fast", "quick", "efficient", "optimized", "improved",
            "enhanced", "better performance", "increased speed"
        ]
        
        content_lower = content.lower()
        
        super_fast_count = sum(1 for keyword in super_fast_keywords if keyword in content_lower)
        fast_count = sum(1 for keyword in fast_keywords if keyword in content_lower)
        
        if super_fast_count >= 2:
            return "super_fast"
        elif super_fast_count >= 1 or fast_count >= 2:
            return "fast"
        else:
            return "standard"
    
    def _extract_performance_tags(self, content: str) -> List[str]:
        """Extract performance-related tags from content."""
        performance_keywords = [
            "speed", "performance", "efficiency", "optimization", "fast",
            "acceleration", "throughput", "latency", "response time",
            "benchmark", "metrics", "scalability", "reliability"
        ]
        
        content_lower = content.lower()
        tags = []
        
        for keyword in performance_keywords:
            if keyword in content_lower:
                tags.append(keyword)
        
        return tags[:7]  # Return top 7 tags
    
    def _calculate_performance_metrics(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate aggregate performance metrics from insights."""
        total_insights = len(insights)
        
        if total_insights == 0:
            return {
                "total_insights": 0,
                "super_fast_count": 0,
                "high_impact_count": 0,
                "average_confidence": 0.0
            }
        
        super_fast_insights = [i for i in insights if i.get("performance_level") == "super_fast"]
        high_impact_insights = [i for i in insights if i.get("impact_level") == "high"]
        
        avg_confidence = sum(i.get("confidence_score", 0) for i in insights) / total_insights
        
        return {
            "total_insights": total_insights,
            "super_fast_count": len(super_fast_insights),
            "fast_count": len([i for i in insights if i.get("performance_level") == "fast"]),
            "high_impact_count": len(high_impact_insights),
            "average_confidence": round(avg_confidence, 2),
            "super_fast_percentage": round(len(super_fast_insights) / total_insights * 100, 1)
        }
    
    def _generate_performance_recommendations(self, insights: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on performance intelligence."""
        recommendations = []
        
        super_fast_insights = [i for i in insights if i.get("performance_level") == "super_fast"]
        high_impact_insights = [i for i in insights if i.get("impact_level") == "high"]
        
        if super_fast_insights:
            recommendations.append(
                f"Leverage {len(super_fast_insights)} super fast performance opportunities identified for competitive advantage"
            )
        
        if high_impact_insights:
            recommendations.append(
                f"Prioritize {len(high_impact_insights)} high-impact performance improvements for maximum ROI"
            )
        
        # Extract common performance themes
        all_tags = []
        for insight in insights:
            all_tags.extend(insight.get("tags", []))
        
        if all_tags:
            from collections import Counter
            top_tags = Counter(all_tags).most_common(3)
            recommendations.append(
                f"Focus on key performance areas: {', '.join([tag for tag, _ in top_tags])}"
            )
        
        immediate_insights = [i for i in insights if i.get("time_relevance") == "immediate"]
        if immediate_insights:
            recommendations.append(
                f"Implement {len(immediate_insights)} immediate performance optimizations for quick wins"
            )
        
        if not recommendations:
            recommendations.append("Continue monitoring performance trends and optimization opportunities")
        
        return recommendations[:5]  # Return top 5 recommendations