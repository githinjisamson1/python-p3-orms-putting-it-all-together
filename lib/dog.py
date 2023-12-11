import sqlite3

# create connection
CONN = sqlite3.connect('lib/dogs.db')

# access cursor to execute SQL queries
CURSOR = CONN.cursor()

class Dog:
    # all to keep track of dogs
    all = []
    
    # initialize with id set to None
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
        
    # job of class to create_table
    @classmethod
    def create_table(cls):
        sql ='''CREATE TABLE IF NOT EXISTS dogs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
            )'''
        
        CURSOR.execute(sql)
        
        
    # destroy table
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        
        CURSOR.execute(sql)
    
    # update self.id after inserting
    def save(self):
        sql ='''INSERT INTO dogs (name, breed) VALUES (?, ?)'''
        val = (self.name, self.breed)
        
        CURSOR.execute(sql, val)
        
        # update self.id from None/expanded save functionality/return list/access first
        # self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        self.id = CURSOR.lastrowid
        
        # !CONN.commit() -- sqlalchemy
        
    @classmethod
    def create(cls, name, breed):
        # DRY/avoids repetition
        dog = Dog(name, breed)
        dog.save()
        
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        # create new python obj using cls constructor/pass record then create obj/instance
        dog = cls(row[1], row[2])
        dog.id = row[0]
        
        return dog     
       
        
    @classmethod
    def get_all(cls):
        sql = '''SELECT * FROM dogs'''
        
        # fetch all rows as list
        all = CURSOR.execute(sql).fetchall()   
        
        # update all class attribute with objs
        cls.all= [cls.new_from_db(row) for row in all]
        
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = '''SELECT * from dogs WHERE name = ? LIMIT 1'''
        val = (name, )
        
        # fetch row
        dog = CURSOR.execute(sql, val).fetchone()
        
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = '''SELECT * from dogs WHERE id = ? LIMIT 1'''
        val = (id, )
        
        dog = CURSOR.execute(sql, val).fetchone()
        
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = '''SELECT * FROM dogs WHERE name = ? AND breed = ?'''
        val = (name, breed)
        
    
        existing_dog = CURSOR.execute(sql, val).fetchone()
        
        if existing_dog:
            return existing_dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog
        
    def update(self):
        # TODO: check working of update again
        # use ? placeholder to prevent sql injections
        sql = "UPDATE dogs SET name = ? WHERE id = ?"
        val = (self.name, self.id)
        
        CURSOR.execute(sql, val)   
        

# dog1 = Dog("NewName", "NewBreed")
# dog1.save()