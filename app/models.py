import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(host = 'localhost',dbname = 'amcred',user = 'postgres',password = '1234',port = 5432)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
        create table if not exists organizations (
        id int not null,
        name varchar(255) not null,
        primary key(id)
        );
        ''')
        self.cursor.execute('''
        create table if not exists users (
        id int not null,
        username varchar(255) not null,
        password varchar(255) not null,
        profile int not null,
        organization_id int not null,
        primary key(id),
        foreign key(organization_id) references organizations(id)
        );
        ''')
        self.conn.commit()

    def create_user(self,username,password,profile,organization_id):
        self.cursor.execute('select max(id) from users')
        maxid = self.cursor.fetchone()[0]
        new_id = maxid + 1 if maxid != None else 0
        self.cursor.execute(f'''
        insert into users (id,username,password,profile,organization_id) values ({new_id},'{username}','{password}',{profile},{organization_id});
        ''')
        self.conn.commit()

    def create_organization(self,name):
        self.cursor.execute('select max(id) from organizations;')
        maxid = self.cursor.fetchone()[0]
        new_id = maxid + 1 if maxid != None else 0
        self.cursor.execute(f'''
        insert into organizations (id,name) values ({new_id},'{name}');
        ''')
        self.conn.commit()

    def get_user(self,username):
        self.cursor.execute(f"select * from users where username='{username}';")
        user = self.cursor.fetchone()
        return None if user == None else {'id':user[0],'username':user[1],'password':user[2],'profile':user[3],'organization_id':user[4]}
    
    def get_org(self,name):
        self.cursor.execute(f"select * from organizations where name='{name}';")
        org = self.cursor.fetchone()
        return None if org == None else {'id':org[0],'name':org[1]}
    
db = Database()