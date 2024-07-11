from flask import Flask, redirect, render_template, request, url_for, jsonify

import json
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='biz0lzc2u0dmp0sq7icr-mysql.services.clever-cloud.com',          # Cambia 'localhost' si tu servidor MySQL está en otro host
        user='uwflb7vojqnyjjug',         # Tu usuario de MySQL
        password='eydlrWP9vN80ls5tEwWJ',  # Tu contraseña de MySQL
        database='biz0lzc2u0dmp0sq7icr' # La base de datos a la que deseas conectarte
    )

# Establece la conexión
connection = mysql.connector.connect(
        host='biz0lzc2u0dmp0sq7icr-mysql.services.clever-cloud.com',          # Cambia 'localhost' si tu servidor MySQL está en otro host
        user='uwflb7vojqnyjjug',         # Tu usuario de MySQL
        password='eydlrWP9vN80ls5tEwWJ',  # Tu contraseña de MySQL
        database='biz0lzc2u0dmp0sq7icr' # La base de datos a la que deseas conectarte
    )

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/dashboard", methods=["GET", "POST"])
def Dashboard():
    
    connection = get_db_connection()
    
    cursor = connection.cursor()
    query = """SELECT SUM(F.total)
                FROM Factura F
                WHERE MONTH(F.fecha) = 6 AND YEAR(F.fecha) = YEAR(CURDATE());"""
    cursor.execute(query)
    result = cursor.fetchall()
    Enero = result[0]
    print(f"Total de ventas en enero: {Enero}")

    return render_template("dashboard.html", Enero=Enero)

#-----------------------------------------------------Factura-----------------------------------------------------#
@app.route("/factura", methods=["GET", "POST"])
def Factura():
    connection = get_db_connection()
    
    cursor = connection.cursor()
    query = """SELECT F.id_factura, F.fecha, F.tipo_factura, F.id_cliente, F.id_empleado, F.total, E.nombre, C.nombre
               FROM Factura F
               JOIN Empleado E ON F.id_empleado = E.id_empleado 
               JOIN Cliente C ON F.id_cliente = C.id_cliente 
               ORDER BY fecha DESC"""
    cursor.execute(query)
    rows = cursor.fetchall()
    clientes = [{'id': row[0], 'fecha': row[1], 'tipo': row[2], 'cliente': row[3], 'empleado': row[4], 'total': row[5], 'nombreemp': row[6], 'nombrecln': row[7]} for row in rows]
    
    query1 = """
    SELECT p.id_empleado, p.nombre
    FROM Empleado p
    """
    cursor.execute(query1)
    rows = cursor.fetchall()
    empleado = [{'id': row[0], 'nombre': row[1]} for row in rows]

    query2 = """
    SELECT p.id_cliente, p.nombre
    FROM Cliente p
    """
    cursor.execute(query2)
    rows = cursor.fetchall()
    cliente = [{'id': row[0], 'nombre': row[1]} for row in rows]

    query3 = """
    SELECT p.id_producto, p.categoria, p.prenda
    FROM Producto p
    """
    cursor.execute(query3)
    rows = cursor.fetchall()
    producto = [{'id': row[0], 'categoria': row[1], 'prenda': row[2]} for row in rows]

    return render_template("factura.html", clientes=clientes,  empleado=empleado, cliente=cliente, producto=producto)

#Guardar
@app.route("/facturaguarda", methods=["POST"])
def AddFactura():
    fecha = request.form['Fecha']
    tipo = request.form['Tipo']
    cliente = request.form['Cliente']
    empleado = request.form['Empleado']


    cursor.execute("SELECT id_factura FROM Factura ORDER BY id_factura DESC LIMIT 1")
    last_id_row = cursor.fetchone()
    if last_id_row:
        last_id = last_id_row[0]
        # Eliminar el prefijo 'F' para obtener solo el número
        numero_factura = int(last_id[1:])
    else:
        # Si no hay registros en la tabla, comenzar desde 0
        numero_factura = 0

    # Incrementar el número de factura en 1
    nuevo_numero_factura = numero_factura + 1

    # Formatear el nuevo ID de factura con el prefijo 'F' y rellenar con ceros a la izquierda
    idF = f'F{nuevo_numero_factura:04d}' 


    # Obtener los datos de los productos del formulario
    productos = []
    for i in range(1, 6):  # Supongamos que como máximo tienes 5 productos
        campo_producto = f'Producto{i}'
        if campo_producto in request.form:
            producto = request.form[campo_producto]
            productos.append(producto)

    # Ahora, puedes procesar la lista de productos como desees
    for producto in productos:
        print()# Aquí puedes realizar alguna acción con cada producto, como insertarlo en la base de datos

    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("INSERT INTO Factura (id_factura, fecha, tipo, id_cliente, id_empleado) VALUES (%s, %s, %s, %s, %s)")
    data = (idF, fecha, tipo, cliente, empleado)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Factura'))

#Editar Factura
@app.route("/EditFactura/<id>", methods=['POST', 'GET'])
def EditFactura(id):
    
    idF = request.form['idF']
    precio = request.form['precio']
    telf = request.form['numero_de_telefono']
    ubi = request.form['ubicacion']
    cnt = request.form['cantidad']
    fch = request.form['fecha']
    emp = request.form['emp']
    name2 = request.form['nombre1']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("UPDATE Producto SET id_producto = ?, marca = ?, precio_original = ?, precio_promocion = ?, categoria = ? WHERE id_producto = ?")
    data = (idF, precio, telf, ubi, cnt, fch, emp, name2)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Factura'))

#Eliminar Factura ---------Restrictiva---------
@app.route("/DelFactura/<id>", methods=['POST', 'GET'])
def DelFactura(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("DELETE FROM Producto WHERE id_producto=?")
    data = (id)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Factura'))
    
    
#-----------------------------------------------------Empleados-----------------------------------------------------#
@app.route("/empleados", methods=["GET", "POST"])
def empleados():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id_empleado, nombre, contacto FROM Empleado ORDER BY nombre DESC")
    rows = cursor.fetchall()
    clientes = [{'id': row[0], 'nombre': row[1], 'num': row[2]} for row in rows]
    return render_template("empleados.html", clientes=clientes)

#Guardar
@app.route("/emp", methods=["POST"])
def add_empleados():
    idc = request.form['id_cliente']
    name = request.form['nombre']
    telf = request.form['numero_de_telefono']

    if idc and name and telf:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO Empleado (id_empleado, contacto, nombre) VALUES (%s, %s, %s)"
        data = (idc, telf, name)
        cursor.execute(sql, data)
        connection.commit()
    return redirect(url_for('empleados'))

@app.route("/deleteemp/<string:id>", methods=['POST', 'GET'])
def deleteemp(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("DELETE FROM Empleado WHERE id_empleado= %s")
    data = (id,)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('empleados'))

@app.route("/editemp/<string:id>", methods=['POST', 'GET'])
def editemp(id):
    
    idc = request.form['id_cliente']
    name = request.form['nombre']
    telf = request.form['numero_de_telefono']

    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("UPDATE Empleado SET id_empleado = %s, contacto = %s, nombre = %s WHERE id_empleado = %s")
    data = (idc, telf, name, id)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('empleados'))


#-----------------------------------------------------Clientes-----------------------------------------------------#
@app.route("/clientes", methods=["GET", "POST"])
def Clientes():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id_cliente, ubicacion, contacto, nombre FROM Cliente ORDER BY id_cliente DESC")
    rows = cursor.fetchall()
    clientes = [{'id_cliente': row[0], 'ubicacion': row[1], 'contacto': row[2], 'nombre': row[3]} for row in rows]
    return render_template("clientes.html", clientes=clientes)

#Guardar
@app.route("/AddCliente", methods=["POST"])
def AddClientes():
    
    cedula= request.form['Cedula']
    nombre = request.form['Nombre']
    contacto = request.form['Contacto']
    ubi = request.form['Ubicacion']

    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("INSERT INTO Cliente (id_cliente, nombre, contacto, ubicacion) VALUES (%s, %s, %s, %s)")
    data = (cedula, nombre, contacto, ubi)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Clientes'))

@app.route("/DelCliente/<string:id>", methods=['POST', 'GET'])
def DelCliente(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("DELETE FROM Cliente WHERE id_cliente= %s")
    data = (id,)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Clientes'))

@app.route("/EditCliente/<string:id>", methods=['POST', 'GET'])
def EditCliente(id):
    
    #idcC= request.form['idC']
    nombre = request.form['Nombre']
    contacto = request.form['Contacto']
    ubi = request.form['Ubicacion']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("UPDATE Cliente SET id_cliente = %s, nombre = %s, contacto = %s, ubicacion = %s WHERE id_cliente = %s")
    data = (id, nombre, contacto, ubi, id)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Clientes'))


#-----------------------------------------------------Productos-----------------------------------------------------#
@app.route("/productos1", methods=["GET", "POST"])
def Products():
    connection = get_db_connection()
    cursor = connection.cursor()


    # Opciones para las dropdowns
    opcionesPrenda_ropa = ["Camisa", "Chaqueta", "Pantalon", "Jogger", "Interior", "Abrigo", "Saco", "Short", "Crop Top"]
    opcionesTalla_ropa = ["XS", "S", "M", "L", "XL"]
    opcionesMarca_ropa = ["Lewis", "Calvin Klein", "Balmain", "Everlane", "Frame", "Ralph Lauren", "Hugo Boss", "Tommy Hilfiger", 
                          "Brooks Brothers", "Lacoste", "Zara", "H&M", "Uniqlo", "Gap"]

    opcionesPrenda_calzado = ["Tacones", "Deportivos", "Botas", "Zandalias", "Crocs", "Zapatillas"]
    opcionesTalla_calzado = [str(talla) for talla in range(28, 46)]
    opcionesMarca_calzado = ["Nike", "Adidas", "Yordan", "Joma", "Under Armour", "Puma", "Rebooks", "New Balance", "Lacoste", 
                             "Birkenstock", "Teva", "Chaco", "Havaianas", "Reef", "Clarks", "Cole Haan", "Steve Madden", 
                             "Keen", "Tory Burch"]

    opcionesPrenda_accesorios = ["Lentes", "Bolso", "Cartera", "Reloj", "Anillo", "Pulsera", "Cadena", "Sombrero", "Gorra", 
                                 "Corbata", "Arete"]
    opcionesTalla_accesorios = ["XS", "S", "M", "L", "XL"]
    opcionesMarca_accesorios = ["Dior", "Calvin Klein", "Tommy", "Lacoste", "Secret", "Chanel", "Hermès", "Fendi", 
                                 "Saint Laurent", "Michael Kors", "Coach", "Nike", "Adidas", "Under Armour", "Puma", 
                                 "Carhartt", "Patagonia", "The North Face", "Columbia", "Supreme", "Rolex", "Omega", 
                                 "Tag Heuer", "Patek Philippe", "Audemars Piguet", "Breitling", "Cartier", 
                                 "IWC Schaffhausen", "Seiko", "Casio"]


    query = """
    SELECT p.id_producto, p.categoria, p.marca, p.stock, p.precio, p.cantidad, 
           p.id_proveedor, p.talla, p.prenda, pr.nombre
    FROM Producto p
    JOIN Proveedor pr ON p.id_proveedor = pr.id_proveedor
    ORDER BY p.categoria DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    clientes = [{'id': row[0], 'categoria': row[1], 'marca': row[2], 'stock': row[3], 'precio': row[4], 'cantidad': row[5], 'id_proveedor': row[6], 'talla': row[7], 'prenda': row[8], 'nombre_proveedor': row[9]} for row in rows]
    
    
    query1 = """
    SELECT p.id_proveedor, p.nombre
    FROM Proveedor p
    """
    cursor.execute(query1)
    rows = cursor.fetchall()
    proveedor = [{'id': row[0], 'nombre': row[1]} for row in rows]
    
    categoria = ""
    return render_template("productos.html", categoriaPY=categoria, clientes=clientes, proveedor=proveedor, opcionesRopaPrenda=opcionesPrenda_ropa, opcionesRopaTalla=opcionesTalla_ropa, opcionesRopaMarca=opcionesMarca_ropa, opcionesAccesoriosPrenda=opcionesPrenda_accesorios, opcionesAccesoriosTalla=opcionesTalla_accesorios, opcionesAccesoriosMarca=opcionesMarca_accesorios, opcionesCalzadoPrenda=opcionesPrenda_calzado, opcionesCalzadoTalla=opcionesTalla_calzado, opcionesCalzadoMarca=opcionesMarca_calzado)

#Editar Productos
@app.route("/EditProducts/<id>", methods=['POST', 'GET'])
def EditProducts(id):
    
    idp= request.form['Idp']
    #categoria= request.form['CategoriaEdit']
    prenda = request.form['PrendaEdit']
    marca = request.form['MarcaEdit']
    talla = request.form['TallaEdit']
    proveedor = request.form['ProveedorEdit']
    stock = request.form['StockEdit']
    precio = request.form['PrecioEdit']

    # Imprimir los valores para depuración
    print(f"Id: {idp}")
    print(f"Prenda: {prenda}")
    print(f"Marca: {marca}")
    print(f"Talla: {talla}")
    print(f"Proveedor: {proveedor}")
    
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("UPDATE Producto SET prenda = %s, marca = %s, talla = %s, id_proveedor = %s, stock = %s, precio = %s WHERE id_producto = %s")
    data = (prenda, marca, talla, proveedor, stock, precio, idp)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Products'))

#Eliminar Productos ---------Restrictiva---------
@app.route("/DelProducts/<id>", methods=['POST', 'GET'])
def DelProducts(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = ("DELETE FROM Producto WHERE id_producto=?")
    data = (id)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Products'))

#Guardar
@app.route("/AddProducts", methods=["POST"])
def AddProducts():
    categoria= request.form['Categoria']
    prenda = request.form['Prenda']
    marca = request.form['Marca']
    talla = request.form['Talla']
    proveedor = request.form['Proveedor']
    stock = request.form['Stock']
    precio = request.form['Precio']

    # Imprimir los valores para depuración
    print(f"Categoria: {categoria}")
    print(f"Prenda: {prenda}")
    print(f"Marca: {marca}")
    print(f"Talla: {talla}")
    print(f"Proveedor: {proveedor}")

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Obtener el último id_producto
    cursor.execute("SELECT id_producto FROM Producto ORDER BY id_producto DESC LIMIT 1")
    last_id_row = cursor.fetchone()
    if last_id_row:
        last_id = last_id_row[0]
    else:
        last_id = "00000"  
        
    new_id = int(last_id) + 1

    # Asegurarse de que el id tenga 5 dígitos, por ejemplo, 00041
    new_id_str = str(new_id).zfill(5)

    # Insertar el nuevo producto
    sql = "INSERT INTO Producto (id_producto, categoria, prenda, marca, talla, id_proveedor, stock, precio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (new_id_str, categoria, prenda, marca, talla, proveedor, stock, precio)
    cursor.execute(sql, data)
    connection.commit()
    return redirect(url_for('Products'))








if __name__ == '__main__':
    app.run(debug=True)