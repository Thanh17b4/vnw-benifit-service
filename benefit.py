from fastapi import APIRouter, Response
from slugify import slugify
from starlette import status

from config import mydb
from model.check_data import is_blank
from schemas import Benefit, BenefitResult, BenefitListResult

benefit_router = APIRouter()


@benefit_router.post('/benefit/create/', status_code=201)
def create_benefit(request: Benefit, response: Response):
    benefit = request.benefit_to_dict()
    # Validate data
    is_ok, msg = __validate(benefit)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(benefit["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO benefits (name, slug) VALUES (%s, %s)"
        val = (benefit["name"], slug)
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} benefit has been inserted successfully"


def __validate(req: dict):
    if req.get("name") is None or is_blank(req.get("name")) is True:
        return False, "name cannot be null"
    return req, ""


@benefit_router.get('/benefit/detail/{id}', status_code=200)
def detail_benefit(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM benefits WHERE id = %d" % id)
        benefit = my_cursor.fetchone()
        if benefit is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"benefits_id is not correct"
        return True, BenefitResult(benefit)


@benefit_router.get('/benefit/all/', status_code=200)
def all_benefit(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM benefits")
        total_benefits = my_cursor.fetchone()[0]
        d = total_benefits % limit
        if d == 0:
            total_page = total_benefits // limit
        else:
            total_page = total_benefits // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute("SELECT * FROM benefits ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
        benefits = my_cursor.fetchall()
        if benefits is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return BenefitListResult(benefits)


@benefit_router.put('/benefit/update/{id}', status_code=200)
async def update_benefit(id: int, req: Benefit, response: Response):
    benefit = req.benefit_to_dict()
    boolean, result = detail_benefit(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check have some changes or not
    ok, msg = __check_changes(result, benefit)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(benefit["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "UPDATE benefits SET name = %s, slug = %s   WHERE id = %s"
        val = (benefit["name"], slug, id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_changes(req: dict, new_req: dict):
    if req["name"] == new_req["name"]:
        return False, "no information have been changed"
    return new_req, ""


@benefit_router.delete('/benefit/delete/{id}', status_code=200)
async def delete_benefit(id: int, response: Response):
    boolean, result = detail_benefit(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM benefits WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
