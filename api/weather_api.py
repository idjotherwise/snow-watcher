from typing import Optional, List

import fastapi
from fastapi import Depends
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from models.location import Location
from models.reports import Report, ReportSubmittal
from models.validation_error import ValidationError
from services import openweather_service, report_service

import country_converter as coco

templates = Jinja2Templates('templates')
router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(request: Request, location: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        data = await openweather_service.get_report_async(city=location.city, state=location.state, country=location.country,
                                                   units=units)
        if location.country.lower() == 'uk':
            country = 'gb'
        else:
            country = location.country.lower()

        loc = {'city': location.city.capitalize(), 'country': coco.convert(country, to='name_short')}
        return templates.TemplateResponse('home/report.html', {'request': request, 'data' : data, 'location': loc})
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        print(f"Server crashed while processing request: {x}")
        return fastapi.Response(content='Error processing your request.', status_code=500)


@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def reports_get() -> List[Report]:
    # await report_service.add_report("A", Location(city="London"))
    # await report_service.add_report("B", Location(city='Feldkirch'))
    return await report_service.get_reports()

@router.post('/api/reports', name='all_reports', status_code=201, response_model=Report)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location
    # await report_service.add_report("A", Location(city="London"))
    # await report_service.add_report("B", Location(city='Feldkirch'))
    return await report_service.add_report(d, loc)