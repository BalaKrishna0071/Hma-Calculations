import uvicorn
from fastapi import FastAPI, UploadFile,Request
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse
import loggers
import datetime
from datetime import timedelta
from data_fetch import fetching
from db_manager import insert_data
from excel_calculation import *
import io
from hma_calculation import Calc


# Fast API
app = FastAPI()
templates  = Jinja2Templates(directory="templates")

# First end Point for Rendering
@app.get("/")
def read_item(request: Request):
    loggers.logger.info("started running")
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# Second end Point for File Upload
@app.post("/api/upload")
def upload_file(file : UploadFile):
    try:
        # Reading Excel File
        df = pd.read_excel(file.file, sheet_name=0)

        # Calling Calculation
        c1 = Calc(df['close'].to_numpy())
        df_res = c1.calculatehma()

        # Using BytesIo for In Memory Storing
        excel_buf = io.BytesIO()
        writer =pd.ExcelWriter(excel_buf, engine="xlsxwriter")
        df_res.to_excel(writer, index=False)
        writer.close()
        excel_buf.seek(0)

        header = {
            'Content-Disposition':f'attachment; filename = {file.filename}'
        }
        return StreamingResponse(excel_buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",headers=header)
    except Exception as e:
            return {" message ": e.args}

# Third end Point
@app.get("/api/fetch/")
def fetch(symbol):

    # Date Conversion into Timestamp
    end_date = datetime.datetime.now()
    end_timestamp = end_date.timestamp()

    end_date_timestamp = int(end_timestamp)
    start_date = end_date - timedelta(days=30)

    start_date_timestamp = start_date.timestamp()
    start_date_timestamp = int(start_date_timestamp)

    # Calling fetching method
    response = fetching(start_date_timestamp=start_date_timestamp, end_date_timestamp=end_date_timestamp, sym=symbol)

    # Accessing Close Column
    price_column = response.get('c')
    time_stamp = response.get('t')

    # Creating a List for Conversion
    conv_timedate = []

    # Converting Timestamp into a Format
    for value in time_stamp:
        val = datetime.datetime.fromtimestamp(value)
        val = val.strftime("%Y-%m-%d %H:%M:%S")
        conv_timedate.append(val)

    # Creating obj
    c1 = Calc(price_column)
    res_df =c1.calculatehma()

    # Inserting dataframe into sql Db
    insert_data(res_df.to_dict('records'))

    # using BytesIo for In Memory Storing
    excel_buf = io.BytesIO()
    writer = pd.ExcelWriter(excel_buf, engine="xlsxwriter")
    res_df.to_excel(writer, index=False)
    writer.close()
    excel_buf.seek(0)

    file_name = f"{symbol}.xlsx"
    header = {
        'Content-Disposition': f'attachment; filename = {file_name}'
    }

    return StreamingResponse(excel_buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         headers=header)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
