from {{ package }} import example


def test_add():
    assert example.add(2, 3) == 5
