import textwrap

import pytest


from src.agents.general_purpose.renderers import render_task_lists
from src.domain import Todolist


@pytest.mark.parametrize("inputs, expected", [
    pytest.param([], "", id="empty list"),
    pytest.param(
[
            Todolist(id_="aaa", name="Groceries", archived=False),
            Todolist(id_="bbb", name="Old things", archived=True),
        ],
"""
- Id: aaa; Name: Groceries; Is active: yes
- Id: bbb; Name: Old things; Is active: no
""".strip(),
        id="simple list"),
    pytest.param(
        [
            Todolist(id_="aaa", name="Groceries", archived=False, sub_todolists=[
                Todolist(id_="aba", name="Fruits and Vegetables", archived=False, sub_todolists=[
                    Todolist(id_="abb", name="Fresh fruits", archived=False),
                    Todolist(id_="abc", name="Fresh vegetables", archived=False),
                    Todolist(id_="abd", name="Canned vegetables", archived=True),
                ]),
                Todolist(id_="aca", name="Meat and fish", archived=False),
            ]),
            Todolist(id_="bbb", name="Old things", archived=True),
        ],
"""
- Id: aaa; Name: Groceries; Is active: yes; Sub-lists:
    - Id: aba; Name: Fruits and Vegetables; Is active: yes; Sub-lists:
        - Id: abb; Name: Fresh fruits; Is active: yes
        - Id: abc; Name: Fresh vegetables; Is active: yes
        - Id: abd; Name: Canned vegetables; Is active: no
    - Id: aca; Name: Meat and fish; Is active: yes
- Id: bbb; Name: Old things; Is active: no
""".strip(),
        id="nested lists"),
])
def test_render_task_lists(inputs: list[Todolist], expected: str) -> None:
    # When
    res = render_task_lists(inputs)

    # Then
    assert res == expected





