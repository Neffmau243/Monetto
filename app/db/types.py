from sqlalchemy import BigInteger
from sqlalchemy.dialects import mysql

ID_TYPE = BigInteger().with_variant(mysql.BIGINT(unsigned=True), "mysql")
