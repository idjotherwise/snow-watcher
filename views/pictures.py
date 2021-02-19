import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates


templates = Jinja2Templates('templates')
router = fastapi.APIRouter()


@router.get('/pictures', include_in_schema=False)
async def pictures(request: Request):
    # data = {'request': request}
    return templates.TemplateResponse('home/pictures.html', {'request': request})