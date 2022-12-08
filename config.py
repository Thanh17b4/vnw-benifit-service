import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    port=3210,
    database="benefit_service",
    user="thanhpv",
    password="22121992"
)
