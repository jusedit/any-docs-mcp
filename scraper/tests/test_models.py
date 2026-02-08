"""Unit tests for models.py — ScopeRules, data models, serialization."""
from models import (
    EngineDecision, EngineMode, GroupPlan, GroupPlanEntry,
    LLMAnalysis, Manifest, ManifestEntry, PipelineConfig,
    ScopeRules, SelectorSpec, UrlRecord,
)


class TestScopeRules:
    def test_url_matches_no_patterns_same_domain(self):
        rules = ScopeRules(base_url="https://example.com")
        assert rules.url_matches("https://example.com/docs/intro")
        assert rules.url_matches("https://example.com/")
        assert not rules.url_matches("https://other.com/docs")

    def test_url_matches_include_patterns(self):
        rules = ScopeRules(
            base_url="https://example.com",
            include_patterns=[r"/docs/", r"/api/"],
        )
        assert rules.url_matches("https://example.com/docs/intro")
        assert rules.url_matches("https://example.com/api/v1")
        assert not rules.url_matches("https://example.com/blog/post")

    def test_url_matches_exclude_patterns(self):
        rules = ScopeRules(
            base_url="https://example.com",
            exclude_patterns=[r"/blog/", r"/pricing/"],
        )
        assert rules.url_matches("https://example.com/docs/intro")
        assert not rules.url_matches("https://example.com/blog/post")
        assert not rules.url_matches("https://example.com/pricing/plans")

    def test_exclude_takes_priority(self):
        rules = ScopeRules(
            base_url="https://example.com",
            include_patterns=[r"/docs/"],
            exclude_patterns=[r"/docs/internal/"],
        )
        assert rules.url_matches("https://example.com/docs/intro")
        assert not rules.url_matches("https://example.com/docs/internal/secret")

    def test_invalid_regex_handled_gracefully(self):
        rules = ScopeRules(
            base_url="https://example.com",
            include_patterns=[r"[invalid", r"/docs/"],
        )
        assert rules.url_matches("https://example.com/docs/intro")

    def test_different_domain_rejected(self):
        rules = ScopeRules(base_url="https://example.com")
        assert not rules.url_matches("https://evil.com/docs/intro")


class TestEngineDecision:
    def test_serialization(self):
        d = EngineDecision(
            mode=EngineMode.CURL,
            curl_md_length=5000,
            selenium_md_length=4800,
            diff_ratio=0.04,
            reason="cURL content sufficient",
        )
        data = d.model_dump()
        assert data["mode"] == "curl"
        assert data["curl_md_length"] == 5000

    def test_selenium_mode(self):
        d = EngineDecision(mode=EngineMode.SELENIUM, reason="JS-heavy site")
        assert d.mode == EngineMode.SELENIUM


class TestManifest:
    def test_manifest_with_entries(self):
        m = Manifest(
            start_url="https://example.com",
            engine_mode="curl",
            total_pages=2,
            total_files=2,
            entries=[
                ManifestEntry(url="https://example.com/a", md_raw_path="a.md", size_bytes=100, content_hash="abc"),
                ManifestEntry(url="https://example.com/b", md_raw_path="b.md", size_bytes=200, content_hash="def"),
            ],
        )
        assert len(m.entries) == 2
        json_str = m.model_dump_json()
        assert "abc" in json_str


class TestGroupPlan:
    def test_group_plan_structure(self):
        plan = GroupPlan(groups=[
            GroupPlanEntry(name="getting-started", paths=["intro.md", "setup.md"], output_path="getting-started.md"),
            GroupPlanEntry(name="api", paths=["api/v1.md"], output_path="api.md"),
        ])
        assert len(plan.groups) == 2
        assert plan.groups[0].name == "getting-started"


class TestPipelineConfig:
    def test_defaults(self):
        c = PipelineConfig(start_url="https://example.com", name="test")
        assert c.max_pages == 500
        assert c.max_workers == 10
        assert c.engine_diff_threshold == 0.3

    def test_custom_values(self):
        c = PipelineConfig(
            start_url="https://example.com",
            name="test",
            max_pages=100,
            max_workers=5,
        )
        assert c.max_pages == 100
        assert c.max_workers == 5
