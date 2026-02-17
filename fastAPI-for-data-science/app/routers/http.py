from fastapi import APIRouter, Header, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(prefix="/http", tags=["http"])


@router.get("/")
async def root(
    accept: str = Header(...),
    accept_encoding: str = Header(...),
    connection: str = Header(...),
    host: str = Header(...),
    user_agent: str = Header(...),
):
    return {
        "accept": accept,
        "accept_encoding": accept_encoding,
        "connection": connection,
        "host": host,
        "user_agent": user_agent,
    }


@router.get("/request")
async def request(request: Request):
    return {
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "query": dict(request.query_params),
        "params": dict(request.query_params),
    }


@router.get("/response")
async def response(response: Response):
    response.set_cookie("cookie-name", "cookie-value", max_age=3600)

    return {
        "headers": dict(response.headers),
    }


@router.get("/html", response_class=HTMLResponse)
async def html():
    return """
        <html> 
            <head>
                <title>Hello world!</title>
            </head>
            <body> 
                <h1>Hello world!</h1>
            </body>
        </html>
    """


@router.get("/redirect")
async def redirect():
    return RedirectResponse("/html-next")


@router.get("/html-next", response_class=HTMLResponse)
async def html_next():
    return """
        <html> 
            <head>
                <title>Hello world!</title>
            </head>
            <body> 
                <h1>You've been redirected!</h1>
            </body>
        </html>
    """