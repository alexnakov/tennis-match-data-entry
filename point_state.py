from dataclasses import dataclass

@dataclass
class PointState:
  first_dir: str = "Wide"
  first_result: str = ""
  second_dir: str = ""
  second_result: str = ""
  return_type: str = ""
  return_shot: str = ""
  return_outcome: str = ""
  end_type: str = ""
  end_shot: str = ""
  end_outcome: str = ""
  strategy_position: str = ""
  strategy_play_style: str = ""
  winner: str = ""

  def reset(self):
    self.__dict__.update(PointState().__dict__)

  def to_summary(self) -> str:
    parts = []
    if self.first_dir.strip() or self.first_result.strip():
        parts.append(f"1st: {self.first_dir} {self.first_result}".strip())
    if self.second_dir.strip() or self.second_result.strip():
        parts.append(f"2nd: {self.second_dir} {self.second_result}".strip())
    if self.return_type.strip() or self.return_shot.strip() or self.return_outcome.strip():
        parts.append(f"Return: {self.return_type} {self.return_shot} {self.return_outcome}".strip())
    if self.winner.strip():
        parts.append(f"Winner: {self.winner}")
    if self.end_type.strip() or self.end_shot.strip() or self.end_outcome.strip():
        parts.append(f"End: {self.end_type} {self.end_shot} {self.end_outcome}".strip())
    if self.strategy_position.strip() or self.strategy_play_style.strip():
        sp = self.strategy_position.strip()
        ps = self.strategy_play_style.strip()
        if sp and ps:
          strategy = f"{sp} + {ps}"
        else:
          strategy = sp or ps  
        parts.append(f"Strategy: {strategy}")
    return ";  ".join(p for p in parts if p and not p.endswith(":"))
