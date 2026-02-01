from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class SiteAnalysis(BaseModel):
    content_selectors: List[str] = Field(
        description="CSS selectors for main content area (in order of priority)"
    )
    navigation_selectors: List[str] = Field(
        description="CSS selectors for navigation/sidebar menu"
    )
    title_selector: Optional[str] = Field(
        default=None,
        description="CSS selector for page title"
    )
    exclude_selectors: List[str] = Field(
        default_factory=list,
        description="CSS selectors for elements to exclude (headers, footers, etc.)"
    )
    url_pattern: str = Field(
        description="Regex pattern to match valid documentation URLs"
    )
    base_url: str = Field(
        description="Base URL of the documentation site"
    )
    grouping_strategy: str = Field(
        default="path_depth_2",
        description="Strategy for grouping pages: path_depth_N, single_file, or manual"
    )
    notes: str = Field(
        default="",
        description="Additional notes about the site structure"
    )


class DocumentationConfig(BaseModel):
    name: str = Field(description="Unique identifier for this documentation set")
    display_name: str = Field(description="Human-readable name")
    start_url: str = Field(description="Starting URL for scraping")
    site_analysis: SiteAnalysis
    version: str = Field(default="v1", description="Current version")
    created_at: str
    updated_at: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class ScrapedPage(BaseModel):
    url: str
    title: str
    content: str
    group: str
    markdown: str
    source_url: str
