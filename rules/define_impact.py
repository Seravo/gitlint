import re

from gitlint.git import GitCommit
from gitlint.rules import CommitRule, RuleViolation


class ImpactDefined(CommitRule):
    """Enforce that `Impact: <major|minor|patch>` has been defined for every
    commit"""

    name = "body-requires-impact"

    id = "SERAVO0001"

    regexp = r'^Impact: (major|minor|patch)$'

    def validate(self, commit: GitCommit) -> list[RuleViolation] | None:
        self.log.debug("Check that proper Impact: has been defined")

        for line in commit.message.body:
            if re.match(self.regexp, line):
                return None
        msg = "Body does not contain a valid 'Impact' line"
        return [RuleViolation(self.id, msg, line_nr=1)]
