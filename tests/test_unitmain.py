from src import unitmain
from collections import OrderedDict
import pytest
import os

@pytest.fixture
def txt() -> str:
    with open('dummy1.txt', 'w') as f:
        for n in ['create_timestamp,player_id,score', '2019/09/13 10:53:40,player886,89', '2012/10/23 13:32:05,player622,86', '2012/10/23 13:32:05,player162,86']:
            f.write('{}\n'.format(n))

    yield 'dummy1.txt'

    os.remove('dummy1.txt')

def test_csv_read(txt):
    assert unitmain.csv_read(txt) == {'player886': {'cnt': 1, 'total': 89}, 'player622': {'cnt': 1, 'total': 86}, 'player162': {'cnt': 1, 'total': 86}}

def test_get_avgscore():
    result = unitmain.get_avgscore({'player685': {'cnt': 1, 'total': 82}, 'player662': {'cnt': 2, 'total': 172}})

    assert result == OrderedDict([(86, ['player662']), (82, ['player685'])])

def test_output_ranking():
    result = unitmain.output_ranking(OrderedDict([(89, ['player886']), (86, ['player622'])]))

    assert result == ['1 player886 89', '2 player622 86']


