class File:
    def __init__(
        self,
        name: str,
        display_str: str,
        short_status: str,
        has_staged_change: bool,
        has_unstaged_change: bool,
        tracked: bool,
        deleted: bool,
        added: bool,
        has_merged_conflicts: bool,
        has_inline_merged_conflicts: bool,
    ) -> None:
        self.name = name
        self.display_str = display_str
        self.short_status = short_status
        self.has_staged_change = has_staged_change
        self.has_unstaged_change = has_unstaged_change
        self.tracked = tracked
        self.deleted = deleted
        self.added = added
        self.has_merged_conflicts = has_merged_conflicts
        self.has_inline_merged_conflicts = has_inline_merged_conflicts
