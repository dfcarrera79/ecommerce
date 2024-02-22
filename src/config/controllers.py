from sqlalchemy import text
from sqlalchemy.orm import Session

class SessionHandler:
    def __init__(self, engine):
        self.engine = engine

    def execute_sql(self, sql: str, mensaje: str):
        try:
            with Session(self.engine) as session:
                rows = session.execute(text(sql)).fetchall()
                session.commit()
                objetos = [row._asdict() for row in rows]
                return {"error": "N", "mensaje": mensaje, "objetos": objetos}
        except Exception as error:
            return {"error": "S", "mensaje": str(error), "objetos": ""}
        
