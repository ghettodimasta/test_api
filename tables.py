from post import Postgres

sql = Postgres()

sql.create_table('products', """
    id bigint,
    name varchar,
    description varchar,
    params varchar
""")



