import game


def test_play_game_wins_after_all_correct_moves(monkeypatch, capsys):
    correct_moves = [
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
    moves = iter(correct_moves)
    monkeypatch.setattr("builtins.input", lambda _: next(moves))

    game.play_game()

    output = capsys.readouterr().out
    assert "You escaped the tower with 10 perfect moves!" in output
    assert "You win!" in output
    assert "Game over." not in output


def test_play_game_ends_on_incorrect_move(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "open door")

    game.play_game()

    output = capsys.readouterr().out
    assert "Wrong move!" in output
    assert "You needed to 'search desk'." in output
    assert "Game over." in output
    assert "You win!" not in output