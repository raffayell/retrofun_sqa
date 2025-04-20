## Database URL structure
{dialect}{+driver}://{username}:{password}@{hostname}:{port}/{database}

### MySQL with pymysql
`url = 'mysql+pymysql://retrofun:my-password@localhost:3306/retrofun'`
### PostgreSQL with psycopg2
`url = 'postgresql+psycopg2://retrofun:my-password@localhost:5432/retrofun'`

### database file in the current directory
`url = 'sqlite:///retrofun.sqlite'`
### database file in /home/miguel/retrofun directory
`url = 'sqlite:////home/miguel/retrofun/retrofun.sqlite'`
### database file in C:\users\miguel\retrofun directory (Microsoft Windows)
`url = 'sqlite:///c:\\users\\miguel\\retrofun\\retrofun.sqlite'`