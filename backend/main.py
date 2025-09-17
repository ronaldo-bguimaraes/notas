from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from extracao.extracao import Extracao
from parser.parser import Parser
from database import Base, engine, SessionLocal
from database.operations import save_nota_to_db, get_nota_by_id
from database.models.nota import NotaORM, NotaModel

app = FastAPI(title="Notas API")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criar as tabelas se não existirem
Base.metadata.create_all(bind=engine)

@app.get("/notas", response_model=List[NotaModel])
async def list_notas(db: Session = Depends(get_db)):
    """
    Lista todas as notas fiscais cadastradas no banco de dados.
    """
    notas = db.query(NotaORM).all()
    return [NotaModel(
        empresa=nota.empresa,
        chave=nota.chave,
        numero=nota.numero,
        serie=nota.serie,
        emissao=nota.emissao,
        items=[ItemModel(
            codigo=item.codigo,
            descricao=item.descricao,
            quantidade=item.quantidade,
            unidade=item.unidade,
            valor_unitario=item.valor_unitario,
            valor_total=item.valor_total
        ) for item in nota.items]
    ) for nota in notas]


def test_database_connection():
    print("Testing database connection...")
    try:
        # Create tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Test connection by creating a session
        print("Testing session...")
        db = SessionLocal()
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        result.fetchone()  # Actually fetch the result
        print("✅ Database connection successful!")
        print("✅ Tables created successfully!")
        db.close()
        return True
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


class Main:
    def __init__(self, target_url):
        self.target_url = target_url

    def run(self):
        # Extrair dados da nota
        extracao = Extracao(self.target_url)
        html_bytes = extracao.run()

        # Fazer o parse dos dados
        parser = Parser(html_bytes)
        nota = parser.run()

        print("\n📝 Nota fiscal extraída:")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
        print(f"Empresa: {nota.empresa}")
        print(f"Número: {nota.numero}")
        print(f"Quantidade de itens: {len(nota.items)}")

        # Salvar no banco de dados
        try:
            nota_salva = save_nota_to_db(nota)
            print("\n✅ Nota fiscal salva com sucesso!")
            # Nota já está no formato do modelo de domínio
            print(f"Nota fiscal salva com ID gerado")
            print(f"Número de itens salvos: {len(nota_salva.items)}")

            # Recuperar a nota do banco para testar
            print("\n🔍 Recuperando nota do banco...")
            nota_recuperada = get_nota_by_id(1)  # Usando ID 1 pois é a primeira nota
            if nota_recuperada:
                print("✅ Nota recuperada com sucesso!")
                print(f"Empresa: {nota_recuperada.empresa}")
                print(f"Número: {nota_recuperada.numero}")
                print(f"Quantidade de itens: {len(nota_recuperada.items)}")
                
                # Verificar se os dados são iguais
                assert nota.empresa == nota_recuperada.empresa, "Empresa diferente!"
                assert nota.numero == nota_recuperada.numero, "Número diferente!"
                assert len(nota.items) == len(nota_recuperada.items), "Quantidade de itens diferente!"
                print("✅ Dados verificados - Tudo ok!")
            else:
                print("❌ Nota não encontrada no banco!")
        except Exception as e:
            print("\n❌ Erro durante o teste!")
            print(f"Error: {str(e)}")
            raise

qr_code_url = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51250809477652008413651160001087671228558149|2|1|1|278155C022E96800A4ACABF2614AA8773B4551F6"

if __name__ == "__main__":
    # First test database connection
    if test_database_connection():
        main = Main(qr_code_url)
        main.run()
