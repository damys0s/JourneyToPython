# tests/test_smoke.py
from journey_to_python.app import main

# Ce test vérifie que :
# L’application peut être lancée sans shell
# La CLI accepte des arguments
# Le repository CSV est correctement initialisé
# Le cas “liste vide” est géré proprement
# L’utilisateur reçoit un message clair
# Aucun effet de bord (grâce à tmp_path)


def test_smoke_list(tmp_path, capsys):
    csv_path = tmp_path / "people.csv"
    code = main(["list", "--csv", str(csv_path)])
    assert code == 0
    out = capsys.readouterr()
    assert "No people found" in out.out
