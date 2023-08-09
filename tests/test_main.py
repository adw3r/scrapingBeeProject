from main import dump_json


def test_dump_result():
    data = {'test': 'data'}
    dump_json(data)
