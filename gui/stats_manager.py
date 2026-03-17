import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

stats_file = Path("math_stats.json")


def get_stats_path() -> Path:
    return Path(__file__).parent.parent / "math_stats.json"


def existing_stats() -> Dict[str, Any]:
    stats_path = get_stats_path()
    if stats_path.exists():
        try:
            with open(stats_path, "r") as file:
                stats = json.load(file)
                if "theme" not in stats:
                    stats["theme"] = "gruvbox_light"
                return stats
        except (json.JSONDecodeError, IOError):
            return create_stats()
    return create_stats()


def create_stats() -> Dict[str, Any]:
    return {
        "games_played": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "best_score_percent": 0.0,
        "current_streak": 0,
        "best_streak": 0,
        "history": [],
        "theme": "gruvbox_light",
    }


def save_stats(stats: Dict[str, Any]):
    stats_path = get_stats_path()
    try:
        with open(stats_path, "w") as file:
            json.dump(stats, file, indent=2)
    except IOError as e:
        print(f"Warning: Could not save stats - {e}")


def update_stats(
    stats: Dict[str, Any],
    score: int,
    total: int,
    mode: str = "solve_mode",
    operation: str = "addition",
    level: int = 1,
) -> Dict[str, Any]:
    stats["games_played"] += 1
    stats["total_questions"] += total
    stats["correct_answers"] += score

    percentage = (score / total) * 100 if total > 0 else 0

    if percentage > stats["best_score_percent"]:
        stats["best_score_percent"] = percentage

    if percentage == 100:
        stats["current_streak"] += 1
        if stats["current_streak"] > stats["best_streak"]:
            stats["best_streak"] = stats["current_streak"]
    else:
        stats["current_streak"] = 0

    if "history" not in stats:
        stats["history"] = []

    stats["history"].append({
        "date": datetime.now().isoformat(),
        "mode": mode,
        "operation": operation,
        "level": level,
        "total": total,
        "correct": score,
        "percentage": percentage,
    })

    if len(stats["history"]) > 100:
        stats["history"] = stats["history"][-100:]

    return stats


def get_stats_summary(stats: Dict[str, Any]) -> Dict[str, Any]:
    if stats["games_played"] == 0:
        return {
            "games_played": 0,
            "total_questions": 0,
            "overall_accuracy": 0.0,
            "best_score_percent": 0.0,
            "current_streak": 0,
            "best_streak": 0,
        }

    overall_accuracy = (stats["correct_answers"] / stats["total_questions"]) * 100

    return {
        "games_played": stats["games_played"],
        "total_questions": stats["total_questions"],
        "overall_accuracy": overall_accuracy,
        "best_score_percent": stats["best_score_percent"],
        "current_streak": stats["current_streak"],
        "best_streak": stats["best_streak"],
    }


def get_history_for_period(
    stats: Dict[str, Any],
    period: str = "all",
) -> List[Dict[str, Any]]:
    if "history" not in stats or not stats["history"]:
        return []

    history = stats["history"]

    if period == "today":
        today = datetime.now().date()
        history = [
            h for h in history
            if datetime.fromisoformat(h["date"]).date() == today
        ]
    elif period == "week":
        from datetime import timedelta
        week_ago = datetime.now() - timedelta(days=7)
        history = [
            h for h in history
            if datetime.fromisoformat(h["date"]) >= week_ago
        ]

    return history


def get_chart_data(
    stats: Dict[str, Any],
    period: str = "all",
) -> Dict[str, List]:
    history = get_history_for_period(stats, period)

    if not history:
        return {
            "sessions": [],
            "questions": [],
            "correct": [],
            "accuracy": [],
        }

    sessions = list(range(1, len(history) + 1))
    questions = [h["total"] for h in history]
    correct = [h["correct"] for h in history]
    accuracy = [h["percentage"] for h in history]

    return {
        "sessions": sessions,
        "questions": questions,
        "correct": correct,
        "accuracy": accuracy,
    }
