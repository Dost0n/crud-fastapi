from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BookSchema, RequestBook, Response
import crud


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
@router.post('/create')
async def create(request:RequestBook, db:Session = Depends(get_db)):
    _book = crud.create_book(db, book=request.parameter)
    return Response(code=200, status ="Ok", message="Book created successfully", result=_book).dict(exclude_none=True)


@router.get('/')
async def get(db:Session=Depends(get_db)):
    _book = crud.get_book(db,0,100)
    return Response(code=200, status="OK", message="Success fetch all data",  result=_book).dict(exclude_none=True)


@router.get("/{id}")
async def get_book_by_id(id, db:Session=Depends(get_db)):
    _book = crud.get_book_by_id(db, id)
    return Response(code=200, status="OK", message="Success get data", result=_book).dict(exclude_none=True)


@router.post("/update/{id}")
async def update_book(id, request:RequestBook, db:Session = Depends(get_db)):
    _book = crud.update_book(db, book_id=id, title=request.parameter.title,
                             description=request.parameter.description)
    return Response(code=200, status = "OK", message="Success update data", result=_book).dict(exclude_none=True)


@router.delete("/delete/{id}")
async def delete(id:int, db:Session = Depends(get_db)):
    crud.remove_book(db, book_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)