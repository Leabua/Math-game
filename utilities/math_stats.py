import json
from pathlib import Path

stats_file = Path("math_stats.json")


def existing_stats():
    """Loads stats from an existing json"""
    if stats_file.exists():
        try:
            with open(stats_file, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return create_stats()

    return create_stats()


def create_stats():
    """Create new stats dictionary for new player"""
    return {
        "games_played": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "best_score_percent": 0.0,
        "current_streak": 0,
        "best_streak": 0,
    }


def save_stats(stats):
    """Save stats to json"""
    try:
        with open(stats_file, "w") as file:
            json.dump(stats, file, indent=2)
    except IOError as e:
        print(f"Warning: Could not save stats - {e}")


def update_stats(stats, score, total):
    """update_stats with current game results"""
    stats["games_played"] += 1
    stats["total_questions"] += total
    stats["correct_answers"] += score

    if total <= 0:
        return stats

    percentage = (score / total) * 100

    if percentage > stats["best_score_percent"]:
        stats["best_score_percent"] = percentage

    if percentage == 100:
        stats["current_streak"] += 1
        if stats["current_streak"] > stats["best_streak"]:
            stats["best_streak"] = stats["current_streak"]
    else:
        stats["current_streak"] = 0

    return stats


def display_stats(stats):
    """Display overall stats"""
    if stats["games_played"] == 0:
        return

    if stats["total_questions"] == 0:
        return

    overall_accuracy = (stats["correct_answers"] / stats["total_questions"]) * 100

    print("\n--- Overall Stats ---")
    print(f"Games played: {stats['games_played']}")
    print(f"Overall accuracy: {overall_accuracy:.2f}%")
    print(f"Best score: {stats['best_score_percent']:.2f}%")
    print(f"Current streak: {stats['current_streak']} perfect games")
    print(f"Best streak: {stats['best_streak']} perfect games")
