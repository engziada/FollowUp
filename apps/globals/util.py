
from datetime import datetime
from os import path
from icecream import ic
from werkzeug.utils import secure_filename

from apps.profiles.models import Influencer
from apps.reports.models import ScanResults, ScanLog
from apps.social.models import Platform, SocialAccount
from apps.authentication.models import Users
from apps.home.models import Log

import xlsxwriter
import pandas as pd




def download_excel(model_name) -> str:
    model = globals().get(model_name)
    if not model:
        return ""

    items = model.query.all()
    if not items:
        return ""

    data = {}
    for column in model.__table__.columns:
        column_name: str = column.name
        if column_name.endswith("_id"):
            column_name_2 = column_name.replace("_id", "")
            data[column_name_2] = [getattr(item, column_name_2) for item in items]
        data[column.name] = [getattr(item, column_name) for item in items]

    df = pd.DataFrame(data)

    excel_file_path = (
        f"{model_name}-{datetime.now().date()}-{datetime.now().time()}.xlsx"
    )
    excel_file_path = secure_filename(excel_file_path)

    # Create an ExcelWriter object

    # excel_writer = pd.ExcelWriter(os.path.join('/home/ziada/YourSpace/app', excel_file_path), engine='xlsxwriter')
    excel_writer = pd.ExcelWriter(excel_file_path, engine="xlsxwriter")
    # Write the DataFrame to Excel
    df.to_excel(excel_writer, sheet_name=f"YourSpace-{model_name}", index=False)
    # Close the ExcelWriter object using close() method
    excel_writer.close()

    # Get the full path of the excel file
    full_path = path.abspath(excel_file_path)
    ic(full_path)
    return full_path