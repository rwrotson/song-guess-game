from dataclasses import dataclass

from app.cli.formatters import Style, TemplateString


# class with classmethod .from_game(game) and .from_player(player)
# endgame presenter
# library stats
# history
# rewrite as functions, not dataclasses?.. maybe no


@dataclass
class ScoreItem:
    player_id: int
    player_name: str
    score: float

    def representation(self, spaces_number: int = 1) -> TemplateString:
        return TemplateString(
            "${player_name}:${spaces}${clr_n}${b}${score}${r}\n",
        ).safe_substitute(
            player_name=self.player_name,
            spaces=" " * spaces_number,
            clr_n=f"$clr_{self.player_id + 1}",
            score=f"{self.score:.2f}",
        )


@dataclass(frozen=True, slots=True)
class Score:
    items: list[ScoreItem]
    current_round: int
    current_player_id: int  # counting from 0

    def _compute_max_length_of_line(self):
        min_lengths_of_lines = [
            len(i.player_name) + len(f"{i.score:.2f}") for i in self.items
        ]
        default_minimal_length = 15
        extra_spaces = 4

        return max([max(min_lengths_of_lines), default_minimal_length]) + extra_spaces

    @property
    def representation(self) -> TemplateString:
        score_repr = TemplateString(
            "${clr_n}${b}ROUND ${round_n}${r}\n",
        ).safe_substitute(
            clr_n=f"$clr_{self.current_player_id + 1}",
            round_n=self.current_round + 1,
        )

        max_length = self._compute_max_length_of_line()
        for i, item in enumerate(self.items):
            extra_spaces_number = (
                max_length - len(item.player_name) - len(f"{item.score:.2f}")
            )

            if i == self.current_player_id:
                item_repr = item.representation(spaces_number=extra_spaces_number)
                score_repr += "${b}" + item_repr + "${r}"
                continue

            score_repr += item.representation(spaces_number=extra_spaces_number)

        return score_repr

    def __str__(self):
        return self.representation
