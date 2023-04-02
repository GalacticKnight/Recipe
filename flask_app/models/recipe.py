from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Recipe:
    database="recipetest"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']#!!!!!!!!!!!!very important
        self.creator = None

    @staticmethod
    def validate_recipe(data):#done
        is_valid = True 
        if len(data['name']) < 3:
            flash("At least 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("At least 3 characters.")
            is_data = False
        if len(data['instructions']) < 1:
            flash("instructions")
            is_data = False
        return is_valid

    
    @classmethod
    def save(cls,data):#you need user_id!!!!!!
        query = '''INSERT INTO recipes 
        (name, description, instructions, date_made, under_30, users_id) 
        VALUES 
        (%(name)s, %(description)s, %(instructions)s,%(date_made)s, %(under_30)s, %(users_id)s);'''
        #you cannot assume, you HAVE TO HAVE AN ID TO LOCATIE WHERE YOU WANT TO PUT IN THE TABLE
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def update(cls,data):#you need user_id!!!!!!
        query = '''UPDATE recipes SET 
        id =(%(id)s),
        name = (%(name)s),
        description = (%(description)s),
        instructions = (%(instructions)s),
        date_made = (%(date_made)s),
        under_30 = (%(under_30)s) 
        where id= %(id)s;'''
        return connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = '''DELETE FROM recipes WHERE ID = %(id)s;'''#??????????????????????
        results = connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def find_by_id(cls, data):
        query='''SELECT * FROM recipes LEFT JOIN users on users.id = recipes.users_id WHERE recipes.id= %(id)s'''#!!!!!!!!!!!
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        r = cls(results[0])
        u = {
            "id": results[0]["users.id"],
            "first_name":results[0]["first_name"],
            "last_name":results[0]["last_name"],
            "email":results[0]["email"],
            "password":results[0]["password"],
            "created_at":results[0]["users.created_at"],
            "updated_at":results[0]["users.updated_at"]
        }
        print(results)
        r.creator=User(u)#
        return r

    @classmethod
    def get_all(cls):#the goal of this
        query = '''SELECT * FROM recipes LEFT JOIN users on users.id = recipes.users_id;'''
        results = connectToMySQL(cls.database).query_db(query)
        print(results)
        lst =[]
        for i in results:
            r = cls(i)
            u = {
                "id": i["users.id"],
                "first_name":i["first_name"],
                "last_name":i["last_name"],
                "email":i["email"],
                "password":i["password"],
                "created_at":i["users.created_at"],
                "updated_at":i["users.updated_at"]
            }
            r.creator=User(u)#
            lst.append(r)
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",lst)
        return lst
