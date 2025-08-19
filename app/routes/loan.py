# Endpoint para el modelo de prestamo

from fastapi import APIRouter, HTTPException, Response
from sqlmodel import select

from ..models.loan import Loan, LoanCreate, LoanUpdate
from ..config.db import session_dep

# Rutas
loan = APIRouter()

# Obtener todos los prestamos
@loan.get("/loans", response_model=list[Loan], tags=["Loans"])
def get_loans(session: session_dep):
    db_loans = session.exec(select(Loan)).all()
    if not db_loans:
        raise HTTPException(status_code=404, detail="No loans found")
    return db_loans

# Obtener un prestamo por ID
@loan.get("/loans/{loan_id}", response_model=Loan, tags=["Loans"])
def get_loan(loan_id: int, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

# Crear un nuevo prestamo
@loan.post("/loans", response_model=Loan, tags=["Loans"])
def create_loan(loan: LoanCreate, session: session_dep):
    db_loan = Loan.model_validate(loan)
    session.add(db_loan)
    session.commit()
    session.refresh(db_loan)
    return db_loan

# Actualizar un prestamo existente
@loan.patch("/loans/{loan_id}", response_model=Loan, tags=["Loans"])
def update_loan(loan_id: int, loan: LoanUpdate, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan_data = loan.model_dump(exclude_unset=True)  # Excluir campos no enviados
    db_loan.sqlmodel_update(loan_data)  # Actualizar los campos del prestamo
    session.add(db_loan)
    session.commit()
    session.refresh(db_loan)
    return db_loan

# Eliminar un prestamo existente
@loan.delete("/loans/{loan_id}", response_model=Loan, tags=["Loans"])
def delete_loan(loan_id: int, session: session_dep):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    session.delete(db_loan)
    session.commit()
    return Response(status_code=204)  # Respuesta exitosa sin contenido