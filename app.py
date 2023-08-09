from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
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
    name = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<Product {self.id} {self.name}'
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    
    def __repr__(self):
        return f'<Location {self.id} {self.name}'

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer,nullable = True)
    product_qty = db.Column(db.Integer,nullable = True)
    location_id = db.Column(db.Integer,nullable = True)

    def __repr__(self):
        return f'<Inventory {self.inventory_id}'

db.create_all()
#All inventory routes


@app.route('/inventory/create', methods=['GET'])
def create_inventory():
    headers = ['Products', 'Product_Qty','Location_Id']
    # products = db.session.query(Product.name,Product.id).join(Inventory,Inventory.product_id == Product.id)
    products = db.session.query(Product.name,Product.id).all()
    locations = db.session.query(Location.name,Location.id).all()
    return render_template('create_inventory.html',headers=headers,products=products,locations = locations)

@app.route('/inventory/save', methods=['GET','POST'])
def add_inventory():
    headers = ['Product_id','Product_Qty']
    product_id = request.form.get('product_id','')
    product_qty = request.form.get('product_qty', '')
    location_id = request.form.get('location_id','')

    if db.session.query(Inventory.query.filter(Inventory.product_id == product_id).exists()).scalar():
        inventory = db.session.query(Inventory).filter(Inventory.product_id == product_id).one()
        inventory.product_qty = product_qty
        inventory.location_id = location_id
        db.session.commit()
    else:
        inventory = Inventory(product_id=product_id,product_qty=product_qty,location_id=location_id)
        db.session.add(inventory)
        db.session.commit()
    return redirect(url_for('inventory'))
    

@app.route('/inventory/<int:id>/edit', methods = ['GET','POST'])
def edit_inventory(id):
    headers = ['Product_Name', 'Product_Qty', 'Location_Name']
    products = db.session.query(Product.id,Product.name,Inventory.product_qty).join(Inventory,Inventory.product_id==Product.id).filter(Inventory.id == id)
    locations = db.session.query(Location.name,Location.id).order_by("name").all()
    return render_template('update_inventory.html',headers=headers, products = products, id=id, locations=locations)

@app.route('/inventory/update', methods = ['GET','POST'])
def update_inventory():
    id = request.form.get('pid','')
    product_qty = request.form.get('product_qty','')
    location_id = request.form.get('location_id','')
    id_info = db.session.query(Inventory).filter(Inventory.id == id).one()
    id_info.product_qty = product_qty
    id_info.location_id = location_id
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
    headers = ['Id','Product_Name', 'Product_Qty','Location_Name']
    #products = db.session.query(Product.name,Product.id,Inventory.id,Inventory.product_qty,Inventory.location_id).join(Inventory,Inventory.product_id == Product.id).order_by(Inventory.id)
    #the below has inventory,products and locations joined
    products = db.session.query(Inventory.id.label('Inventory_id'),Inventory.product_qty,Inventory.location_id,
                                Product.name.label('Product_name'),Product.id.label('Product_id'),
                                Location.id.label('Location_id'),Location.name.label('Location_name')).join(Product,Inventory.product_id == Product.id).join(Location,Inventory.location_id == Location.id).order_by(Inventory.id).all()
    return render_template('index.html', headers=headers,tableData = products)


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
    products = db.session.query(Product.id,Product.name,Inventory.product_qty).join(Inventory,Inventory.product_id == Product.id).order_by("name").all()
    return render_template('products.html', headers=headers,tableData = products)





# THE BELOW ROUTE NEED CHANGES ALTOGETHER TO MATCH WITH THE FUNCTIONALITY CHANGES
#All location routes

@app.route('/locations/create', methods=['GET'])
def create_locationss():
    headers = ['LocationName','Actions']
    return render_template('create_locations.html',headers=headers)

@app.route('/locations/save', methods=['GET','POST'])
def add_locations():
    headers = ['LocationName','Actions']
    name = request.form.get('name', '')
    loc = Location(name=name)
    db.session.add(loc)
    db.session.commit()
    id = db.one_or_404(db.select(Location.id).filter(Location.name == name))
    inv = Inventory(location_id = id)
    db.session.add(inv)
    db.session.commit()
    return redirect(url_for('locations'))

@app.route('/locations/<int:id>/edit', methods = ['GET','POST'])
def edit_locations(id):
    p_name = db.one_or_404(db.select(Location.name).filter(Location.id == id))
    return render_template('update_location.html',name = p_name, id=id)

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
