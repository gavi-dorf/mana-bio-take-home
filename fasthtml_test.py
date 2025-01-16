from fasthtml.common import *
import os
import os.path
import results_parsers
import uuid
from datetime import datetime
import database_helpers

hdrs = (HighlightJS(langs=['python', 'javascript', 'html', 'css']), )

app, rt = fast_app(hdrs=hdrs)

upload_dir = "file_uploads/"

@rt('/')
def get():
    (_, cursor) = database_helpers.connect_to_database()
    results = cursor.execute("SELECT * FROM results;").fetchall()
    return Div(A("Upload new results", href="/upload-new-results"), Table(Tbody(
        map(lambda t: Tr(map(lambda i: Td(i), t)), results)
    )))


@rt('/upload-new-results')
def get():
    return Titled(
        "Upload a new results file",
        Article(
            Form(hx_post=upload, hx_target="#result-one")(
                Input(type="file", name="file"),
                Button("Upload", type="submit", cls='secondary'),
            ), Div(id="result-one")))


@rt
async def upload(file: UploadFile):
    # card = FileMetaDataCard(file)
    result_to_display = ""
    upload_timestamp = datetime.now()

    (root, ext) = os.path.splitext(file.filename)
    filepath = os.path.join(upload_dir, root + str(uuid.uuid4()) + ext)
    os.makedirs(upload_dir, exist_ok=True)

    try:
        filebuffer = await file.read()
        with open(filepath, "wb") as f:
            f.write(filebuffer)
        result_to_display = results_parsers.parse_file(filepath, upload_timestamp)
    except Exception as e:
        result_to_display = e

    os.remove(filepath)

    return Pre(Code(result_to_display))


serve()
