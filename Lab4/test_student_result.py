import pytest

from student_result import get_result


@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        (-1, 80, "Некорректный балл"),
        (0, 80, "Незачёт"),
        (49, 80, "Незачёт"),
        (50, 60, "Зачёт"),
        (69, 60, "Зачёт"),
        (70, 70, "Хорошо"),
        (89, 70, "Хорошо"),
        (90, 80, "Отлично"),
        (100, 100, "Отлично"),
        (101, 80, "Некорректный балл"),
        (80, -1, "Некорректная посещаемость"),
        (80, 0, "Незачёт"),
        (80, 59, "Незачёт"),
        (80, 60, "Зачёт"),
        (80, 69, "Зачёт"),
        (80, 70, "Хорошо"),
        (90, 79, "Хорошо"),
        (90, 80, "Отлично"),
        (80, 100, "Хорошо"),
        (80, 101, "Некорректная посещаемость"),
    ],
)
def test_get_result_equivalence_classes_and_boundaries(
    score, attendance, expected
):
    assert get_result(score, attendance) == expected


@pytest.mark.parametrize("score", [0, 49, 50, 69, 70, 89, 90, 100])
def test_score_boundary_values(score):
    assert get_result(score, 80) in {"Незачёт", "Зачёт", "Хорошо", "Отлично"}


@pytest.mark.parametrize("attendance", [0, 59, 60, 69, 70, 79, 80, 100])
def test_attendance_boundary_values(attendance):
    assert get_result(90, attendance) in {"Незачёт", "Зачёт", "Хорошо", "Отлично"}


@pytest.mark.parametrize("score", ["90", None, [], object()])
def test_invalid_score_type(score):
    with pytest.raises(TypeError, match="Баллы должны быть числом"):
        get_result(score, 80)


@pytest.mark.parametrize("attendance", ["80", None, [], object()])
def test_invalid_attendance_type(attendance):
    with pytest.raises(TypeError, match="Посещаемость должна быть числом"):
        get_result(90, attendance)
