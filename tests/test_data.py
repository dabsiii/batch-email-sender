from pathlib import Path

from icecream import ic

from src.data import Data


def test_data():

    relative_path = Path("tests\\excel file.xlsx")

    data = Data(relative_path.resolve())
    columns = data.get_columns()
    dic = data.get_records()
    print(dic)

    for record in dic:
        name = record["NAME"]
        attachment = record["FILE"]
        email = record["EMAIL"]
        ic(name, attachment, email)
