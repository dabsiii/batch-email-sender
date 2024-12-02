from typing import Dict, List

import pandas


class Data:
    def __init__(self, filepath: str):
        self._dataframe = pandas.read_excel(filepath, header=0)

    def get_columns(self) -> List[str]:
        return self._dataframe.columns.to_list()

    def get_records(self) -> List[Dict]:
        return self._dataframe.to_dict(orient="records")

    def get_number_of_records(self) -> int:
        return self._dataframe.shape[0]
