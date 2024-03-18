from app.cli.formatters import TemplateString
from app.cli.models import MenuStep
from app.game.models import get_game


def make_question_menu() -> MenuStep:
    def get_question_menu_representation() -> TemplateString:
        game = get_game()
        score_repr = game.get_score()
        stats_repr = game.get_current_player_stats()

        return score_repr + "\n" + stats_repr

    return MenuStep(
        name="QuestionMenu",
        prompt=get_question_menu_representation(),
        options=[
            "play_sample",
            "get_a_clue",
            "give_answer",
        ],
    )


ANSWER_MENU = MenuStep(
    name="AnswerMenu",
    prompt="Please write down your guess, what song is it?",
)


def make_evaluation_menu() -> MenuStep:
    def get_evaluation_menu_representation() -> TemplateString:
        game = get_game()

        text = TemplateString(
            "Your answer is ${clr_current}${b}${answer}${r}.\n"
            "Actually it is ${clr_current}${b}${correct_answer}${r}.\n"
        ).safe_substitute(
            answer=game.current_song.answer.answer_prompt,
            correct_answer=str(game.current_song),
        )

        return text

    return MenuStep(
        name="EvaluationMenu",
        prompt=get_evaluation_menu_representation(),
        options=[
            "listen_to_extended_sample",
            "listen_to_entire_song",
            "evaluate_as_correct_answer",
            "evaluate_as_half_correct_answer",
            "evaluate_as_wrong_answer",
            "evaluate_as_no_answer",
        ],
    )


EVALUATION_MENU = MenuStep(
    name="EvaluationMenu",
    prompt=None,
    options=[
        "listen_to_extended_sample",
        "listen_to_entire_song",
        "evaluate_as_correct_answer",
        "evaluate_as_half_correct_answer",
        "evaluate_as_wrong_answer",
        "evaluate_as_no_answer",
    ],
)

ENDGAME_MENU = MenuStep(
    name="EndgameMenu",
    prompt="You've reached the end!",
)
