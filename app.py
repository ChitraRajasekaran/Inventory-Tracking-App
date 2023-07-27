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

@app.route('/products/<int:id>/edit', methods = ['GET','POST'])
def edit_products(id):
    # p_name = db.session.query(Product.name).filter(Product.id == id)
    p_name = db.one_or_404(db.select(Product.name).filter(Product.id == id))
    return render_template('edit.html',name = p_name, id=id)

@app.route('/products/update', methods = ['GET','POST'])
def update_products():
    id = request.form.get('pid','')
    name = request.form.get('pname','')
    id_info = db.session.query(Product).filter(Product.id == id).one()
    id_info.name = name
    db.session.commit()
    return redirect(url_for('index'))
@app.route('/')
def index():
    headers = ['ProductName','Actions']
    return render_template('index.html', headers=headers,tableData = Product.query.all())