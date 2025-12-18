from pathlib import Path

from gitlint.config import LintConfig
from gitlint.lint import GitLinter

from .base import BaseTestCase

MESSAGE_HEAD = """Create cool feature

This is the coolest feature of them all.
"""

MESSAGE_TEMPLATE = """{head}

Impact: {impact}
"""


class TestImpact(BaseTestCase):
    # Based on <https://github.com/jorisroovers/gitlint/blob/4d9119760056492eabc201bfad5de2f9e660b85f/gitlint-core/gitlint/tests/test_lint.py>

    def _get_linter(self) -> GitLinter:
        config = LintConfig()
        config.extra_path = Path(__file__).parent.parent / 'rules'
        return GitLinter(config)

    def _test_impact(self, impact: str):
        linter = self._get_linter()
        gitcontext = self.gitcontext(
            MESSAGE_TEMPLATE.format(head=MESSAGE_HEAD, impact=impact)
        )
        results = linter.lint(gitcontext.commits[-1])
        # FIXME: Should we ensure that our custom rule was loaded?
        assert len(results) == 0

    def test_impact_major(self):
        """Test that valid impact has been set"""
        self._test_impact('major')

    def test_impact_minor(self):
        """Test that valid impact has been set"""
        self._test_impact('major')

    def test_impact_patch(self):
        """Test that valid impact has been set"""
        self._test_impact('patch')

    def _test_invalid_impact(self, impact: str):
        """Test that invalid impact is not valid"""
        linter = self._get_linter()
        gitcontext = self.gitcontext(
            MESSAGE_TEMPLATE.format(head=MESSAGE_HEAD, impact=impact)
        )
        results = linter.lint(gitcontext.commits[-1])
        assert len(results) > 0
        assert 'SERAVO0001' in [x.rule_id for x in results]

    def test_invalid_impact_mainor(self):
        self._test_invalid_impact('mainor')

    def test_invalid_impact_empty(self):
        self._test_invalid_impact('')

    def test_invalid_impact_aku(self):
        self._test_invalid_impact('aku')

    def test_invalid_impact_patchx(self):
        self._test_invalid_impact('patchx')

    def test_missing_impact(self):
        """Test that missing impact is not valid"""
        linter = self._get_linter()
        gitcontext = self.gitcontext(MESSAGE_HEAD)
        results = linter.lint(gitcontext.commits[-1])
        assert len(results) > 0
        assert 'SERAVO0001' in [x.rule_id for x in results]
