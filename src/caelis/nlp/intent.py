from dataclasses import dataclass, field


@dataclass
class IntentResult:
    name: str
    confidence: float
    matched_pattern: str = ""
    entities: dict = field(default_factory=dict)

    @property
    def matched(self) -> bool:
        return self.name != "unknown"