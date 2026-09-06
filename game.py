def play_game():
    """A short text adventure with exactly 10 moves to win."""
    print("=== Escape the Midnight Tower ===")
    print("You wake up inside a locked tower. To escape, you must make the right 10 moves.")
    print("Type the exact action shown in each prompt.\n")

    sequence = [
        "search desk",
        "take key",
        "open chest",
        "read note",
        "unlock door",
        "climb ladder",
        "light lantern",
        "cross bridge",
        "open gate",
        "escape",
    ]

    for move_number, correct_action in enumerate(sequence, start=1):
        print(f"Move {move_number}/10")
        player_choice = input(f"What do you do? > ").strip().lower()

        if player_choice != correct_action:
            print(f"Wrong move! The tower seals shut. You needed to '{correct_action}'.")
            print("Game over.")
            return

        print(f"Good choice. You {correct_action}.")

    print("\nYou escaped the tower with 10 perfect moves!")
    print("You win!")


if __name__ == "__main__":
    play_game()
