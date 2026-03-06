import pandas as pd
class ExcelUtil:
    #1.读取Excel用例
    def read_excel(file_path,sheet_name="Sheet1"):
        df=pd.read_excel(file_path,sheet_name=sheet_name)
        df=df.dropna(subset=["url","method"])
        return df.to_dict("records")
