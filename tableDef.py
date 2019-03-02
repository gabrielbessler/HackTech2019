from sqlalchemy import *

metadata = MetaData()

annotationsTable = Table(
    "annotations_table",
    metadata,
    Column("id",Integer,primary_key = True),
    Column("sentence",String),
    Column("annotation",String)
)
