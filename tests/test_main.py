import pytest
from pgcli.main import need_completion_refresh, obscure_process_password


@pytest.mark.parametrize('sql', [
    'DROP TABLE foo',
    'SELECT * FROM foo; DROP TABLE foo',
])
def test_need_completion_refresh(sql):
    assert need_completion_refresh(sql)

def test_obscure_process_password():
    import setproctitle
    original_title = setproctitle.getproctitle()

    setproctitle.setproctitle("pgcli user=root password=secret host=localhost")
    obscure_process_password()
    title = setproctitle.getproctitle()
    expected = "pgcli user=root password=xxxx host=localhost"
    assert title == expected

    setproctitle.setproctitle("pgcli postgres://root:secret@localhost/db")
    obscure_process_password()
    title = setproctitle.getproctitle()
    expected = "pgcli postgres://root:xxxx@localhost/db"
    assert title == expected

    setproctitle.setproctitle(original_title)
