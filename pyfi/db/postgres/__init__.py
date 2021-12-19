"""
Patch for drop_all function in SQLAlchemy for postgres
"""
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"
