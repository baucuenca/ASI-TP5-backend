# Endpoint para el modelo de prestamo

from fastapi import APIRouter, HTTPException, Response
from sqlmodel import select

from ..models.loan import Loan, LoanCreate, LoanUpdate, LoanRead
from ..models.book import Book
from ..models.member import Member
from ..config.db import session_dep

# Rutas
loan = APIRouter()

# Parcear Loan a LoanRead
def parse_to_loan_read(loan: Loan, session: session_dep):
    book = session.get(Book, loan.book_id)
    member = session.get(Member, loan.member_id)
    return LoanRead(
        book_title=book.title,
        member_email=member.email,
        loan_date=loan.loan_date,
        return_date=loan.return_date,
        returned=loan.returned
    )

# Obtener todos los prestamos
@loan.get("/loans", response_model=list[LoanRead], tags=["Loans"])
def get_loans(session: session_dep):
    db_loans = session.exec(select(Loan)).all()
    if not db_loans:
        raise HTTPException(status_code=404, detail="No loans found")

    # Se devuelve una lista de instancias de LoanRead
    return [
        parse_to_loan_read(loan, session)
        for loan in db_loans
    ]

# Obtener un prestamo por ID
@loan.get("/loans/{loan_id}", response_model=LoanRead, tags=["Loans"])
def get_loan(loan_id: int, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Se devuelve una instancia de LoanRead la cual acomoda mejor los datos para el usuario
    read_loan = parse_to_loan_read(db_loan, session)
    return read_loan

# Crear un nuevo prestamo
@loan.post("/loans", response_model=LoanRead, tags=["Loans"])
def create_loan(loan: LoanCreate, session: session_dep):
    # Verificar la existencia del libro y el miembro
    db_book = session.get(Book, loan.book_id)
    db_member = session.get(Member, loan.member_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    loans_count = len(session.exec(select(Loan).where(Loan.book_id == loan.book_id)).all())
    if loans_count >= db_book.stock:
        raise HTTPException(status_code=409, detail="No more copies available for loan")
    
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db_loan = Loan.model_validate(loan)
    session.add(db_loan)
    session.commit()
    session.refresh(db_loan)
    return parse_to_loan_read(db_loan, session)

# Actualizar un prestamo existente
@loan.patch("/loans/{loan_id}", response_model=LoanRead, tags=["Loans"])
def update_loan(loan_id: int, loan: LoanUpdate, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan_data = loan.model_dump(exclude_unset=True)  # Excluir campos no enviados
    db_loan.sqlmodel_update(loan_data)  # Actualizar los campos del prestamo
    session.add(db_loan)
    session.commit()
    session.refresh(db_loan)
    return parse_to_loan_read(db_loan, session)

# Eliminar un prestamo existente
@loan.delete("/loans/{loan_id}", status_code=204, tags=["Loans"])
def delete_loan(loan_id: int, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    session.delete(db_loan)
    session.commit()
    return Response(status_code=204)  # Respuesta exitosa sin contenido