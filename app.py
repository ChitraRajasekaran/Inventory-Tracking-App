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
    product_id = db.Column(db.Integer,nullable = False)
    product_qty = db.Column(db.Integer,nullable = True)
    location_id = db.Column(db.Integer,nullable = True)

    def __repr__(self):
        return f'<Inventory {self.inventory_id}'
    
    #86792192

db.create_all()
#All inventory routes


@app.route('/inventory/create', methods=['GET'])
def create_inventory():
    headers = ['Product_Id', 'Product_Qty','Location_Id']
    return render_template('create_inventory.html',headers=headers)

@app.route('/inventory/save', methods=['GET','POST'])
def add_inventory():
    headers = ['Product_Qty','Location_Id']
    product_qty = request.form.get('product_qty', '')
    location_id = request.form.get('location_id', '')
    inv = Inventory(product_qty=product_qty,location_id=location_id )
    db.session.add(inv)
    db.session.commit()
    # id = db.one_or_404(db.select(Inventory.product_id).filter(Inventory.product_id == product_id))
    # prod = Product(id = id)
    # db.session.add(prod)
    # db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/inventory/<int:id>/edit', methods = ['GET','POST'])
def edit_inventory(id):
    p_qty = db.one_or_404(db.select(Inventory.product_qty).filter(Inventory.id == id))
    return render_template('update_inventory.html',name = p_qty, id=id)

@app.route('/inventory/update', methods = ['GET','POST'])
def update_inventory():
    id = request.form.get('pid','')
    product_qty = request.form.get('product_qty','')
    id_info = db.session.query(Inventory).filter(Inventory.id == id).one()
    id_info.product_qty = product_qty
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/inventory/<int:id>/delete', methods = ['POST'])
def delete_inventory(id):
    i_delete_id = Inventory.query.get_or_404(id)
    db.session.delete(i_delete_id)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/')
def inventory():
    headers = ['Id','Product_Id', 'Product_Qty','Location_Id']
    return render_template('index.html', headers=headers,tableData = Inventory.query.order_by("id").all())


#All product routes

@app.route('/products/create', methods=['GET'])
def create_products():
    headers = ['ProductName','Actions']
    return render_template('create_products.html',headers=headers)

@app.route('/products/save', methods=['GET','POST'])
def add_products():
    headers = ['ProductName','Product_Qty','Actions']
    name = request.form.get('name', '')
    prod = Product(name=name)
    db.session.add(prod)
    db.session.commit()
    id = db.one_or_404(db.select(Product.id).filter(Product.name == name))
    inv = Inventory(product_id = id)
    db.session.add(inv)
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/products/<int:id>/edit', methods = ['GET','POST'])
def edit_products(id):
    p_name = db.one_or_404(db.select(Product.name).filter(Product.id == id))
    return render_template('update_product.html',name = p_name, id=id)

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
    headers = ['ProductName','Product_Qty','Actions']
    return render_template('products.html', headers=headers,tableData = Product.query.order_by("name").all())






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
