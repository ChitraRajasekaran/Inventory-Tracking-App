from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chitrarajasekaran@localhost:5432/inventoryapp'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

app.app_context().push()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Product {self.id} {self.name}'
# Deleting the db.createall because inculding db migrate
# db.create_all()

@app.route('/products/create', methods=["POST"])
def add_products():
    name = request.form.get('name', '')
    products = Product(name=name)
    db.session.add(products)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    headers = ['ProductName','Actions']
    return render_template('index.html', headers=headers,tableData = Product.query.all())