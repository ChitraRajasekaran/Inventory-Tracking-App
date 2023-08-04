from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy as sa
# from sqlalchemy import orm 
# from sqlalchemy import ForeignKey
from flask_migrate import Migrate

# BASE = orm.declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chitrarajasekaran@localhost:5432/inventoryapp'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

app.app_context().push()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Product {self.id} {self.name}'
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Location {self.id} {self.name}'

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer,nullable=False)
    product_qty = db.Column(db.Integer)
    location_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'<Inventory {self.inventory_id}'

db.create_all()
#All inventory routes
@app.route('/')
def display_inventory():
    headers = ['Id','Product_Id', 'Product_Qty','Location_Id']
    return render_template('index.html', headers=headers,tableData = Inventory.query.order_by("id").all())
#All location routes

@app.route('/locations/create', methods=["POST"])
def add_locations():
    name = request.form.get('name', '')
    locations = Location(name=name)
    db.session.add(locations)
    db.session.commit()
    return redirect(url_for('locations'))

@app.route('/locations/<int:id>/edit', methods = ['GET','POST'])
def edit_locations(id):
    p_name = db.one_or_404(db.select(Location.name).filter(Location.id == id))
    return render_template('edit_location.html',name = p_name, id=id)

@app.route('/locations/update', methods = ['GET','POST'])
def update_locations():
    id = request.form.get('pid','')
    name = request.form.get('pname','')
    id_info = db.session.query(Location).filter(Location.id == id).one()
    id_info.name = name
    db.session.commit()
    return redirect(url_for('locations'))

@app.route('/locations/<int:id>/delete', methods = ['POST'])
def delete_locations(id):
    p_delete_id = Location.query.get_or_404(id)
    db.session.delete(p_delete_id)
    db.session.commit()
    return redirect(url_for('locations'))

@app.route('/locations')
def locations():
    headers = ['LocationName','Actions']
    return render_template('locations.html', headers=headers,tableData = Location.query.order_by("name").all())


#All product routes
@app.route('/products/create', methods=["POST"])
def add_products():
    name = request.form.get('name', '')
    products = Product(name=name)
    db.session.add(products)
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/products/<int:id>/edit', methods = ['GET','POST'])
def edit_products(id):
    p_name = db.one_or_404(db.select(Product.name).filter(Product.id == id))
    return render_template('edit_product.html',name = p_name, id=id)

@app.route('/products/update', methods = ['GET','POST'])
def update_products():
    id = request.form.get('pid','')
    name = request.form.get('pname','')
    id_info = db.session.query(Product).filter(Product.id == id).one()
    id_info.name = name
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/products/<int:id>/delete', methods = ['POST'])
def delete_products(id):
    p_delete_id = Product.query.get_or_404(id)
    db.session.delete(p_delete_id)
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/products')
def products():
    headers = ['ProductName','Actions']
    return render_template('products.html', headers=headers,tableData = Product.query.order_by("name").all())
