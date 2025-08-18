# Endpoint para el modelo Miembros

from fastapi import APIRouter, HTTPException, Response
from sqlmodel import select

from ..models.member import Member, MemberCreate, MemberUpdate
from ..config.db import session_dep

# Rutas
member = APIRouter()

# Obtener todos los miembros
@member.get("/members", response_model=list[Member], tags=["Members"])
def get_members(session: session_dep):
    db_members = session.exec(select(Member)).all()
    if not db_members:
        raise HTTPException(status_code=404, detail="No members found")
    return db_members

# Obtener un miembro por ID
@member.get("/members/{member_id}", response_model=Member, tags=["Members"])
def get_member(member_id: int, session: session_dep):
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

# Crear un nuevo miembro
@member.post("/members", response_model=Member, tags=["Members"])
def create_member(member: MemberCreate, session: session_dep):
    db_member = Member.model_validate(member)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member

# Actualizar un miembro existente
@member.patch("/members/{member_id}", response_model=Member, tags=["Members"])
def update_member(member_id: int, member: MemberUpdate, session: session_dep):
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    member_data = member.model_dump(exclude_unset=True)  # Excluir campos no enviados
    db_member.sqlmodel_update(member_data)  # Actualizar los campos del miembro
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member

# Eliminar un miembro existente
@member.delete("/members/{member_id}", response_model=Member, tags=["Members"])
def delete_member(member_id: int, session: session_dep):
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    session.delete(db_member)
    session.commit()
    return Response(status_code=204)  # Respuesta exitosa sin contenido