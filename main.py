from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////recipes.db'
db = SQLAlchemy(app)

# Initialize the database
# db.create_all()


class RecipeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    serving = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Recipe(name = {self.name}, description = {self.description}, serving = {self.serving}, " \
               f"prep_time = {self.prep_time}, cooking_time = {self.cooking_time})"


recipe_put_args = reqparse.RequestParser()
recipe_put_args.add_argument("name", type=str, help="Please provide the name of the recipe", required=True)
recipe_put_args.add_argument("description", type=str, help="Please provide a description for the recipe", required=True)
recipe_put_args.add_argument("serving", type=int, help="Please provide the serving for the recipe", required=True)
recipe_put_args.add_argument("prep_time", type=int, help="Please provide the time to prepare the recipe in minutes",
                             required=True)
recipe_put_args.add_argument("cooking_time", type=int, help="Please provide the cooking time for the recipe in minutes",
                             required=True)

recipe_update_args = reqparse.RequestParser()
recipe_update_args.add_argument("name", type=str, help="Please provide the name of the recipe")
recipe_update_args.add_argument("description", type=str, help="Please provide a description for the recipe")
recipe_update_args.add_argument("serving", type=int, help="Please provide the serving for the recipe")
recipe_update_args.add_argument("prep_time", type=int, help="Please provide the time to prepare the recipe in minutes")
recipe_update_args.add_argument("cooking_time", type=int,
                                help="Please provide the cooking time for the recipe in minutes")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'serving': fields.Integer,
    'prep_time': fields.Integer,
    'cooking_time': fields.Integer
}


class Recipe(Resource):
    @marshal_with(resource_fields)
    def get(self, recipe_id):
        result = RecipeModel.query.filter_by(id=recipe_id).first()
        if not result:
            abort(404, message="Recipe ID is not valid.")
        return result

    @marshal_with(resource_fields)
    def put(self, recipe_id):
        args = recipe_put_args.parse_args()
        result = RecipeModel.query.filter_by(id=recipe_id).first()
        if result:
            abort(409, message="A recipe is already defined with that ID.")

        recipe = RecipeModel(id=recipe_id, name=args['name'], description=args['description'], serving=args['serving'],
                             prep_time=args['prep_time'], cooking_time=args['cooking_time'])
        db.session.add(recipe)
        db.session.commit()
        return recipe, 201

    @marshal_with(resource_fields)
    def patch(self, recipe_id):
        args = recipe_update_args.parse_args()
        result = RecipeModel.query.filter_by(id=recipe_id).first()
        if not result:
            abort(409, message="Cannot update a recipe that isn't defined.")

        if args['name']:
            result.name = args['name']
        if args['description']:
            result.description = args['description']
        if args['serving']:
            result.serving = args['serving']
        if args['prep_time']:
            result.prep_time = args['prep_time']
        if args['cooking_time']:
            result.cooking_time = args['cooking_time']

        db.session.commit()
        return result

    def delete(self, recipe_id):
        result = RecipeModel.query.filter_by(id=recipe_id).first()
        if not result:
            abort(404, message="Recipe ID is not valid.")

        db.session.delete(result)
        db.session.commit()
        return "Recipe deleted.", 202


api.add_resource(Recipe, "/recipe/<int:recipe_id>")

if __name__ == "__main__":
    app.run(debug=True)
