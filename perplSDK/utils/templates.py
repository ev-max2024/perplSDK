"""Research query templates and generators."""

from typing import List, Dict, Optional


class ResearchTemplate:
    """Templates for generating research queries."""
    
    def __init__(self):
        self.templates = {
            "comprehensive": {
                "base_queries": [
                    "What are the latest developments in {topic}?",
                    "Who are the key players and market leaders in {topic}?",
                    "What are the current trends and growth projections for {topic}?",
                    "What challenges and opportunities exist in {topic}?",
                    "How is {topic} evolving and what are future predictions?"
                ],
                "industry_modifiers": {
                    "automotive": [
                        "automotive industry impact of {topic}",
                        "vehicle manufacturers and {topic}",
                        "automotive supply chain implications of {topic}"
                    ],
                    "technology": [
                        "technological innovations in {topic}",
                        "R&D investments in {topic}",
                        "patent landscape for {topic}"
                    ],
                    "energy": [
                        "energy sector applications of {topic}",
                        "renewable energy and {topic}",
                        "grid infrastructure impact of {topic}"
                    ]
                }
            },
            "competitive": {
                "base_queries": [
                    "Who are the top competitors in {topic} market?",
                    "What are the competitive advantages in {topic}?",
                    "Market share analysis for {topic} industry",
                    "New entrants and disruptors in {topic} space",
                    "Pricing strategies and competition in {topic}"
                ]
            },
            "market": {
                "base_queries": [
                    "Market size and growth projections for {topic}",
                    "Consumer demand trends in {topic}",
                    "Regional market analysis for {topic}",
                    "Investment and funding trends in {topic}",
                    "Regulatory impact on {topic} market"
                ]
            },
            "technical": {
                "base_queries": [
                    "Technical specifications and standards for {topic}",
                    "Manufacturing processes and capabilities in {topic}",
                    "Quality and performance metrics for {topic}",
                    "Testing and certification requirements for {topic}",
                    "Technical challenges and solutions in {topic}"
                ]
            }
        }
    
    def generate_queries(
        self,
        topic: str,
        research_type: str = "comprehensive",
        industry: Optional[str] = None,
        time_horizon: str = "current",
        custom_focus: Optional[List[str]] = None
    ) -> List[str]:
        """Generate research queries based on template.
        
        Args:
            topic: Main research topic
            research_type: Type of research template to use
            industry: Industry context for additional queries
            time_horizon: Time focus for queries
            custom_focus: Additional focus areas
            
        Returns:
            List of formatted research queries
        """
        queries = []
        
        # Get base template
        template = self.templates.get(research_type, self.templates["comprehensive"])
        
        # Generate base queries
        for query_template in template["base_queries"]:
            query = query_template.format(topic=topic)
            queries.append(self._add_time_context(query, time_horizon))
        
        # Add industry-specific queries
        if industry and research_type == "comprehensive":
            industry_templates = template.get("industry_modifiers", {}).get(industry, [])
            for query_template in industry_templates:
                query = query_template.format(topic=topic)
                queries.append(self._add_time_context(query, time_horizon))
        
        # Add custom focus queries
        if custom_focus:
            for focus in custom_focus:
                query = f"How does {focus} relate to {topic}?"
                queries.append(self._add_time_context(query, time_horizon))
        
        return queries
    
    def _add_time_context(self, query: str, time_horizon: str) -> str:
        """Add time context to queries."""
        time_modifiers = {
            "current": "current and recent",
            "historical": "historical perspective on",
            "future": "future outlook and predictions for",
            "trends": "emerging trends in"
        }
        
        modifier = time_modifiers.get(time_horizon, "")
        if modifier:
            return f"{modifier} {query}"
        return query
    
    def get_ev_industry_queries(self, topic: str) -> List[str]:
        """Get EV industry specific queries."""
        ev_templates = [
            "How does {topic} impact electric vehicle adoption?",
            "What role does {topic} play in EV market growth?",
            "How are EV manufacturers addressing {topic}?",
            "What are the implications of {topic} for EV charging infrastructure?",
            "How does {topic} affect EV battery technology and performance?",
            "What regulatory considerations exist for {topic} in the EV industry?",
            "How does {topic} influence consumer perception of electric vehicles?",
            "What partnerships and collaborations exist around {topic} in EV space?"
        ]
        
        return [template.format(topic=topic) for template in ev_templates]
    
    def create_custom_template(
        self,
        name: str,
        base_queries: List[str],
        industry_modifiers: Optional[Dict[str, List[str]]] = None
    ) -> None:
        """Create a custom research template.
        
        Args:
            name: Template name
            base_queries: List of base query templates with {topic} placeholder
            industry_modifiers: Optional industry-specific modifiers
        """
        self.templates[name] = {
            "base_queries": base_queries,
            "industry_modifiers": industry_modifiers or {}
        }