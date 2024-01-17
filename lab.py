from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL
import random
import string
from datetime import datetime, timedelta



app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lab2023'
mysql=MySQL(app)

app.secret_key='llavesecreta'
# Configuración de la base de datos



##################### INDEX ###########################



@app.route('/')
def index():
   
    return render_template('home.html')





#################### RUTAS DE PRODUCTOS#################



@app.route('/index_producto')
def index_producto():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_producto, r.nombre, cod_scanner, p.nombre, iv.tasa, precio_costo, precio_venta1, precio_venta2, precio_venta3, stock_minimo, stock_actual  FROM producto p JOIN rubro r on p.id_rubro=r.id_rubro JOIN iva iv on p.id_iva= iv.id_iva")
    productos = cursor.fetchall()

    cursor.execute('SELECT * FROM rubro')
    rubro = cursor.fetchall()
    
    cursor.execute('SELECT * FROM iva')
    iva=cursor.fetchall()

    return render_template('index_producto.html', productos=productos, rubro=rubro, iva=iva)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        rubro = request.form['rubro']
        cod_scanner = request.form['cod_scanner']
        nombre = request.form['nombre']
        iva = request.form['iva']
        precio_c = request.form['precio_costo']
        p_v1 = request.form['precio_venta1']
        p_v2 = request.form['precio_venta2']
        p_v3 = request.form['precio_venta3']
        stock_minimo = request.form['stock_minimo']
        stock_actual = request.form['stock_actual']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO producto (id_rubro,cod_scanner, nombre, id_iva, precio_costo, precio_venta1, precio_venta2, precio_venta3, stock_minimo, stock_actual) VALUES ( %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (rubro,cod_scanner, nombre, iva, precio_c, p_v1, p_v2, p_v3, stock_minimo, stock_actual))
        mysql.connection.commit()
        flash('Producto agregado satisfactoriamente')

        return redirect(url_for('index_producto'))

@app.route('/editar_producto/<id_producto>', methods=['POST'])
def editar_producto(id_producto):
    if request.method == 'POST':
        rubro = request.form['rubro']
        cod_scanner = request.form['cod_scanner']
        nombre = request.form['nombre']
        iva = request.form['iva']
        precio_c = request.form['precio_c']
        p_v1 = request.form['p_v1']
        p_v2 = request.form['p_v2']
        p_v3 = request.form['p_v3']
        stock_minimo = request.form['stock_minimo']
        stock_actual = request.form['stock_actual']

    cursor = mysql.connection.cursor()
   
    sql = "UPDATE producto SET id_rubro=%s, cod_scanner=%s, nombre=%s, id_iva=%s, precio_costo=%s, precio_venta1=%s, precio_venta2=%s, precio_venta3=%s, stock_minimo=%s, stock_actual=%s WHERE id_producto=%s"
   
    data = (rubro, cod_scanner, nombre, iva, precio_c, p_v1, p_v2, p_v3, stock_minimo, stock_actual, id_producto)

    cursor.execute(sql, data)
    mysql.connection.commit()

    flash('Producto editado satisfactoriamente')
    return redirect(url_for('index_producto'))

@app.route('/eliminar_producto/<id_producto>')
def eliminar_producto(id_producto):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM producto WHERE id_producto={id_producto}")
    mysql.connection.commit()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('index_producto'))




#################### RUTAS DE CLIENTES##################




@app.route('/index_cliente')
def index_cliente():
    # Mostrar la lista de clientes
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    return render_template('index_cliente.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    # Agregar un nuevo cliente
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        cta_cte = request.form['cta_cte']
        saldo_inicial = request.form['saldo_inicial']
        saldo_actual = request.form['saldo_actual']
        limite_cred = request.form['limite_cred']
        plazo_cred = request.form['plazo_cred']
        cuit = request.form['cuit']

        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cliente (nombre, cuit, direccion, telefono, cta_cte, saldo_inicial, saldo_actual, limite_cred, plazo_cred ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre, cuit, direccion, telefono, cta_cte, saldo_inicial, saldo_actual, limite_cred, plazo_cred))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')

        return redirect(url_for('index_cliente'))
    
 

@app.route('/editar_cliente/<id_cliente>', methods=['POST'])
def editar_cliente(id_cliente):
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            cta_cte = request.form['cta_cte']
            saldo_inicial = request.form['saldo_inicial']
            saldo_actual = request.form['saldo_actual']
            limite_cred = request.form['limite_cred']
            plazo_cred = request.form['plazo_cred']

            cursor = mysql.connection.cursor()    
            sql = "UPDATE cliente SET nombre=%s, direccion=%s, telefono=%s, cta_cte=%s, saldo_inicial=%s, saldo_actual=%s, limite_cred=%s, plazo_cred=%s WHERE id_cliente=%s"
            data = (nombre, direccion, telefono, cta_cte, saldo_inicial, saldo_actual, limite_cred, plazo_cred, id_cliente)
            
            cursor.execute(sql, data)
            mysql.connection.commit()
            
            flash('Contacto editado satisfactoriamente')
            return redirect(url_for('index_cliente'))
    except Exception as e:
        flash(f'Error al editar el cliente: {str(e)}', 'error')
        return redirect(url_for('index_cliente'))

            

    
   
    

@app.route('/eliminar_cliente/<id_cliente>')
def eliminar_cliente(id_cliente):
    # Eliminar un cliente
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM cliente WHERE id_cliente={id_cliente}")
    mysql.connection.commit()
    flash('Contacto eliminado satisfactoriamente')
    return redirect(url_for('index_cliente'))




############## RUTAS DE CUOTAS##################




@app.route('/index_cuotas')
def index_cuotas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_cuota, c.nombre, valor, fecha_venc, valor_venc, fecha_pago, valor_pago FROM venta_cuota vc join venta v on vc.id_venta= v.id_venta join cliente c on v.id_cliente = c.id_cliente ")
    cuotas = cursor.fetchall()
    return render_template('index_cuotas.html', cuotas=cuotas)

@app.route('/editar_cuota/<id_cuota>', methods=['POST'])
def editar_cuota(id_cuota):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM venta_cuota WHERE id_cuota = %s", (id_cuota,))
    cuota = cursor.fetchone()

    if request.method == 'POST':
        fecha_pago = request.form['fecha_pago']
        valor_pago = request.form['valor_pago']
        # Otros campos necesarios para la cuota
        try:
            cursor.execute("UPDATE venta_cuota SET fecha_pago=%s, valor_pago=%s WHERE id_cuota=%s",
                        (fecha_pago, valor_pago, id_cuota))
            mysql.connection.commit()
        except Exception as e:
            print(f"Error durante la actualización: {e}")
        flash('Cuota editada satisfactoriamente')
        return redirect(url_for('index_cuotas'))

    return render_template('editar_cuota.html', cuota=cuota)

@app.route('/eliminar_cuota/<id_cuota>')
def eliminar_cuota(id_cuota):
    # Eliminar un cliente
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM venta_cuota WHERE id_cuota={id_cuota}")
    mysql.connection.commit()
    flash('Cuota eliminado satisfactoriamente')
    return redirect(url_for('index_cuotas'))





###################### RUTA DE VENTAS #######################






def generar_numero_comprobante(cursor):
    # Obtiene el último número de comprobante utilizado desde la base de datos
    cursor.execute("SELECT MAX(SUBSTRING_INDEX(nro_comprobante, '-', -1)) FROM venta")
    ultimo_numero = cursor.fetchone()[0]

    # Verifica si ya hay algún comprobante en la base de datos
    if ultimo_numero is not None:
        # Si hay comprobantes, incrementa el número
        nuevo_numero = int(ultimo_numero) + 1
    else:
        # Si no hay comprobantes, empieza desde 0
        nuevo_numero = 0

    # Formatea el nuevo número de comprobante
    nro_comprobante = f"{nuevo_numero:04d}-{nuevo_numero:08d}"

    return nro_comprobante


@app.route('/index_venta', methods=['GET','POST'])
def agregar_venta():
    cursor = mysql.connection.cursor()
 

# Obtén los datos de las ventas con información de productos desde la base de datos
    cursor.execute("""
    SELECT v.id_venta, c.nombre as cliente_nombre, v.tipo_comprobante, v.nro_comprobante,
           v.fecha, v.neto, v.iva, v.montototal, p.nombre as producto_nombre, vi.cantidad, vi.precio
    FROM venta v
    JOIN venta_item vi ON v.id_venta = vi.id_venta
    JOIN cliente c ON v.id_cliente = c.id_cliente
    JOIN producto p ON vi.id_producto = p.id_producto
    """)
    ventas = cursor.fetchall()
    
    # Obtén el ID del producto por defecto (puedes ajustarlo según tu lógica)
    producto_id_default = 1

    # Obtén el porcentaje de IVA correspondiente al id_iva
    cursor.execute("SELECT tasa FROM iva WHERE id_iva = (SELECT id_iva FROM producto WHERE id_producto = %s)", (producto_id_default,))
    porcentaje_iva_default = cursor.fetchone()[0]

    # Inicializa porcentaje_iva con un valor por defecto
    porcentaje_iva = porcentaje_iva_default

    if request.method == 'POST':
        print("Datos del formulario:", request.form)
        id_cliente = request.form['cliente']
        id_producto = request.form.getlist('productos')

        cantidades_str = request.form['cantidades']
        
        # Reemplaza las comas por puntos y luego convierte a lista de flotantes
        cantidades_list = [float(cantidad.replace(',', '.')) for cantidad in cantidades_str.split(',')]

        # Puedes usar esta lista como sea necesario en tu lógica
        print(cantidades_list)
        # Verificar si la cadena de precio_producto no está vacía antes de convertirla a float
        precio_producto_str = request.form['precio_final']
        if precio_producto_str:
            precio_producto = float(precio_producto_str)
        else:
            precio_producto = 0.0  # O ajusta esto según sea necesario

        id_medio_pago = request.form['medio_pago']
        cuotas = int(request.form['cuotas'])

        # Realiza el cálculo del monto total
        monto_total =  precio_producto
        
        cursor.execute("SELECT tasa FROM iva WHERE id_iva = (SELECT id_iva FROM producto WHERE id_producto = %s)", (id_producto[0],))
        porcentaje_iva = cursor.fetchone()[0]
        
        # Calcula el IVA y el precio neto utilizando el porcentaje obtenido
        iva_total = (monto_total * float(porcentaje_iva)) / 100

        precio_neto = monto_total - iva_total

        # Genera letras aleatorias para el tipo de comprobante
        tipo_comprobante = ''.join(random.choices(string.ascii_uppercase, k=2))
        nro_comprobante = generar_numero_comprobante(cursor)
        
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()

        cursor.execute("INSERT INTO venta (id_cliente, tipo_comprobante, nro_comprobante, fecha, neto, iva, montototal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (id_cliente, tipo_comprobante, nro_comprobante, fecha_actual, precio_neto, iva_total, monto_total))
        venta_id = cursor.lastrowid
    
        # Inserta en la tabla venta_item
        cursor.execute("INSERT INTO venta_item (id_venta, id_producto, cantidad, precio, neto, iva) VALUES (%s,%s, %s, %s, %s, %s)", (venta_id, id_producto, cantidades_list, precio_producto, precio_neto, iva_total))

        # Inserta en la tabla venta_medio_pago
        cursor.execute("INSERT INTO venta_medio_pago (id_venta, id_medio, monto) VALUES (%s, %s, %s)", (venta_id, id_medio_pago, monto_total))

        # Inserta en la tabla venta_cuota
        if cuotas > 1:

            # Calcula el monto de cada cuota
            tasa_base = 0.05  # Tasa base de interés
            tasa_interes_adicional = tasa_base + cuotas * 0.20  # Ajusta dinámicamente la tasa de interés adicional

            monto_cuota = monto_total / cuotas * (1 + tasa_interes_adicional)
            
            
            # Bucle para insertar las cuotas
            for cuota_numero in range(1, cuotas + 1):
                # Calcula la fecha de vencimiento y el valor de vencimiento
                fecha_vencimiento = fecha_actual + timedelta(days=31* cuota_numero)
                valor_vencimiento = monto_cuota * 1.5

                # Inserta la información en la tabla venta_cuota
                cursor.execute(
                    "INSERT INTO venta_cuota (id_venta, valor, fecha_venc, valor_venc) VALUES (%s,%s, %s, %s)",
                    (venta_id, monto_cuota, fecha_vencimiento, valor_vencimiento)
                )
        for i, id_prod in enumerate(id_producto):
            cantidad_vendida = cantidades_list[i]
            print(f"ID Producto: {id_prod}, Cantidad Vendida: {cantidad_vendida}")
            cursor.execute("UPDATE producto SET stock_actual = stock_actual - %s WHERE id_producto = %s", (cantidad_vendida, id_prod))
               
            mysql.connection.commit()
        flash('Venta registrada satisfactoriamente')

        return redirect(url_for('agregar_venta'))

    # Si el método es GET, renderiza el formulario con la información necesaria
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()

    cursor.execute("SELECT * FROM medio_pago")
    medios_pago = cursor.fetchall()
    
    cursor.execute("SELECT * FROM iva")
    iva = cursor.fetchall()
    
    return render_template('index_venta.html',ventas=ventas, clientes=clientes, productos=productos, medios_pago=medios_pago, iva=iva)

@app.route('/eliminar_venta/<int:id_venta>')
def eliminar_venta(id_venta):
    # Eliminar un cliente
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM venta WHERE id_venta={id_venta}")
    mysql.connection.commit()
    flash('venta eliminada satisfactoriamente')
    return redirect(url_for('agregar_venta'))

@app.route('/editar_venta/<id_venta>', methods=['POST'])
def editar_venta(id_venta):
    if request.method == 'POST':
        # Obtén los datos del formulario de edición
        # (Ajusta esto según los campos que necesites editar)
        tipo_comprobante = request.form['tipo_comprobante']
        nro_comprobante = request.form['nro_comprobante']
        fecha = request.form['fecha']
        neto = request.form['neto']
        iva = request.form['iva']
        monto_total = request.form['monto_total']
       
        # ... otros campos ...


    cursor = mysql.connection.cursor()
    # Realiza la actualización en la base de datos
    sql=("UPDATE venta SET tipo_comprobante=%s, nro_comprobante=%s, fecha=%s, neto=%s, iva=%s, montototal=%s WHERE id_venta=%s")
    data=(tipo_comprobante, nro_comprobante, fecha, neto, iva, monto_total, id_venta)
    cursor.execute(sql,data)
    mysql.connection.commit()
    flash('Venta editada satisfactoriamente')

    # Redirige a la página de index_venta (o a donde desees)
    return redirect(url_for('agregar_venta'))     

if __name__ == '__main__':
    app.run(debug=True)
