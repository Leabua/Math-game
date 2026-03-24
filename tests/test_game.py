import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os


from utilities.game_logic import generate_integer
from utilities.math_stats import (
    create_stats,
    update_stats,
)

sys.path.insert(0, str(Path(__file__).parent.parent))

os.chdir(Path(__file__).parent.parent)


class TestGenerateInteger:
    def test_level_1_range(self):
        for _ in range(100):
            num = generate_integer(1)
            assert 0 <= num <= 99

    def test_level_2_range(self):
        for _ in range(100):
            num = generate_integer(2)
            assert 10 <= num <= 99

    def test_level_3_range(self):
        for _ in range(100):
            num = generate_integer(3)
            assert 100 <= num <= 999


class TestMathStats:
    def setup_method(self):
        self.test_stats_file = Path("test_math_stats.json")
        if self.test_stats_file.exists():
            self.test_stats_file.unlink()
        import utilities.math_stats as ms

        ms.stats_file = self.test_stats_file

    def teardown_method(self):
        if self.test_stats_file.exists():
            self.test_stats_file.unlink()
        import utilities.math_stats as ms

        ms.stats_file = Path("math_stats.json")

    def test_create_stats(self):
        stats = create_stats()
        assert stats["games_played"] == 0
        assert stats["total_questions"] == 0
        assert stats["correct_answers"] == 0
        assert stats["best_score_percent"] == 0.0
        assert stats["current_streak"] == 0
        assert stats["best_streak"] == 0

    def test_update_stats_perfect_score(self):
        stats = create_stats()
        updated = update_stats(stats, 10, 10)

        assert updated["games_played"] == 1
        assert updated["total_questions"] == 10
        assert updated["correct_answers"] == 10
        assert updated["best_score_percent"] == 100.0
        assert updated["current_streak"] == 1
        assert updated["best_streak"] == 1

    # 7/10 test
    def test_update_stats_imperfect_score(self):
        stats = create_stats()
        updated = update_stats(stats, 7, 10)

        assert updated["games_played"] == 1
        assert updated["total_questions"] == 10
        assert updated["correct_answers"] == 7
        assert updated["best_score_percent"] == 70.0
        assert updated["current_streak"] == 0
        assert updated["best_streak"] == 0

    def test_update_stats_streak_continues(self):
        stats = create_stats()
        stats["current_streak"] = 2
        stats["best_streak"] = 2

        updated = update_stats(stats, 10, 10)

        assert updated["current_streak"] == 3
        assert updated["best_streak"] == 3

    def test_update_stats_streak_broken(self):
        stats = create_stats()
        stats["current_streak"] = 5
        stats["best_streak"] = 5

        updated = update_stats(stats, 8, 10)

        assert updated["current_streak"] == 0
        assert updated["best_streak"] == 5

    def test_update_stats_best_score_improves(self):
        stats = create_stats()
        stats["best_score_percent"] = 80.0

        updated = update_stats(stats, 9, 10)

        assert updated["best_score_percent"] == 90.0

    def test_update_stats_best_score_stays(self):
        stats = create_stats()
        stats["best_score_percent"] = 95.0

        updated = update_stats(stats, 8, 10)

        assert updated["best_score_percent"] == 95.0


class TestAddition:
    def test_add_solve_mode_wrong_answer(self, monkeypatch):
        from main_modes.add import add

        call_count = [0]

        def mock_input(prompt):
            call_count[0] += 1
            return "999"

        monkeypatch.setattr("builtins.input", mock_input)

        score = add("solve_mode", 1, 1)
        assert score == 0

    def test_add_x_mode_wrong_answer(self, monkeypatch):
        from main_modes.add import add

        def mock_input(prompt):
            return "999"

        monkeypatch.setattr("builtins.input", mock_input)

        score = add("x_mode", 1, 1)
        assert score == 0


class TestSubtraction:
    def test_minus_solve_mode_wrong_answer(self, monkeypatch):
        from main_modes.minus import minus

        def mock_input(prompt):
            return "999"

        monkeypatch.setattr("builtins.input", mock_input)

        score = minus("solve_mode", 1, 1)
        assert score == 0


class TestMultiplication:
    def test_multiply_solve_mode_wrong_answer(self, monkeypatch):
        from main_modes.multiplication import multiply

        def mock_input(prompt):
            return "999"

        monkeypatch.setattr("builtins.input", mock_input)

        score = multiply("solve_mode", 1, 1)
        assert score == 0


class TestDivision:
    def test_division_solve_mode_wrong_answer(self, monkeypatch):
        from main_modes.divison import division

        def mock_input(prompt):
            return "999"

        monkeypatch.setattr("builtins.input", mock_input)

        score = division("solve_mode", 1, 1)
        assert score == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
