from app.cli.mods.processors import Input
from app.game.models import Evaluation
from app.state import Stage, get_state


class QuestionProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()
        game = state.game

        match (input_.validated, input_.option_name):
            case (1, "PLAY_SAMPLE"):
                game.current_song.play_sample()
                game.current_player.help_usage.repeats.decrement()
            case (2, "GET_A_CLUE"):
                game.current_song.play_clue()
                game.current_player.help_usage.clues.decrement()
            case (3, "GIVE_ANSWER"):
                state.stage = Stage.GAME.value.ANSWER
            case _:
                raise ValueError("Invalid input.")


class AnswerProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        state = get_state()

        state.game.current_song.answer.give_answer(input_.validated)
        state.stage = Stage.GAME.value.EVALUATION_


class EvaluationProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        match (input_.validated, input_.option_name):
            case (1, "LISTEN_TO_EXTENDED_SAMPLE"):
                start_time = state.game.current_song.question_sample.start_time
                state.game.current_song.play(start=start_time)
            case (2, "LISTEN_TO_ENTIRE_SONG"):
                state.game.current_song.play()
            case (3, "EVALUATE_AS_CORRECT_ANSWER"):
                state.game.current_song.answer.evaluate(Evaluation.FULL_ANSWER)
            case (4, "EVALUATE_AS_HALF_CORRECT_ANSWER"):
                state.game.current_song.answer.evaluate(Evaluation.HALF_ANSWER)
            case (5, "EVALUATE_AS_WRONG_ANSWER"):
                state.game.current_song.answer.evaluate(Evaluation.WRONG_ANSWER)
            case (6, "EVALUATE_AS_NO_ANSWER"):
                state.game.current_song.answer.evaluate(Evaluation.NO_ANSWER)
            case _:
                raise ValueError("Invalid input.")

        if input_.validated in range(3, 7):
            try:
                state.game.next_iteration()
                state.stage = Stage.GAME.value.QUESTION
            except StopIteration:
                state.stage = Stage.GAME.value.ENDGAME


class EndgameProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        state = get_state()

        representation = state.game.get_endgame_stats()
        state.viewer.display(representation)

        input("Press ENTER to return to main menu.")

        state.stage = Stage.MAIN_MENU
