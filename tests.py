"""Module imports"""

import editdatabase
dbmanager = editdatabase.Databasemanager()

def test_plyhistoryaddrem():
    """Test playerhistory db"""
    dbmanager.plyhistoryadd("testserver")
    data = dbmanager.plyhistoryall()
    assert "testserver" in data

    dbmanager.plyhistoryremove("testserver")
    data = dbmanager.plyhistoryall()
    assert "testserver" not in data
   