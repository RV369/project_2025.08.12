import io
from ftplib import FTP
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from config import settings

login = settings.LOGIN
password = settings.PASSWORD

app = FastAPI()


async def ftp_connect(
    hostname: str,
    username: str,
    password: str,
    file_content: bytes,
    name: str,
    port: int = 2122,
) -> str:
    try:
        ftp = FTP()
        ftp.connect(host=hostname, port=port)
        ftp.login(username, password)
        with io.BytesIO(file_content) as image:
            ftp.storbinary(f'STOR {name}', image)
        ftp.quit()
    except Exception as e:
        print(f'{e} Ошибка загрузки файла')
        return '<h2>«Неуспешно»</h2>'
    return '<h2>«Успешно»</h2>'


@app.post('/file')
async def upload(
    file: Annotated[UploadFile, File()],
    ip_address: Annotated[str, Form()],
):
    if file.content_type != 'application/octet-stream':
        print(f'{file.content_type} -неверный тип файла')
        return HTMLResponse(content='<h2>«Неуспешно»</h2>')
    file_content = await file.read()
    html_content = await ftp_connect(
        ip_address,
        login,
        password,
        file_content,
        file.filename,
    )
    return HTMLResponse(content=html_content)


@app.get('/')
async def root():
    return FileResponse('public/index.html')
