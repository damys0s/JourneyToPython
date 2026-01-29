from journey_to_python.app import main


def test_smoke(capsys):
    main()
    out = capsys.readouterr().out
    assert "Person(" in out
