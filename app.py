from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import numpy as np
import json



app = Flask(__name__)


def cargar_archivo_excel(ruta):
    try:
        datos = pd.read_excel(ruta, header=None)
        return datos
    except Exception as e:
        print("Error al cargar el archivo:", e)
        return None

global num_entradas
global num_salidas
global num_patrones

def contar_elementos(matriz):
    global num_entradas, num_salidas, num_patrones
    matriz_lista = matriz.tolist()  
    num_entradas = sum(row.count('x') for row in matriz_lista)
    num_salidas = sum(row.count('s') for row in matriz_lista)
    num_patrones = sum(row.count('p') for row in matriz_lista)
    return num_entradas, num_salidas, num_patrones


def mostrar_matriz(matriz):
    matriz_str = ""
    for row in matriz[1:]:
        matriz_str += ' '.join(str(cell) for cell in row[1:]) + "\n"
    return matriz_str



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        archivo = request.files["archivo"]
        if archivo.filename != "":
            try:
                datos = pd.read_excel(archivo, header=None)
                num_entradas, num_salidas, num_patrones = contar_elementos(datos.values)
                matriz_str = mostrar_matriz(datos.values)
                return render_template("resultado.html", num_entradas=num_entradas, num_salidas=num_salidas, num_patrones=num_patrones, matriz=matriz_str)
            except Exception as e:
                error = "Error al procesar el archivo: " + str(e)
                return render_template("index.html", error=error)
    return render_template("index.html", num_entradas=0)

@app.route("/graficas", methods=["GET", "POST"])
def exito():
    if request.method == "POST":

        pass

    # Obtén los datos pasados desde la redirección
    num_entradas = request.args.get("num_entradas")
    num_salidas = request.args.get("num_salidas")
    num_patrones = request.args.get("num_patrones")
    matriz = request.args.get("matriz")
    # Renderiza el nuevo HTML exito.html con los datos
    return render_template("graficas.html", num_entradas=num_entradas, num_salidas=num_salidas, num_patrones=num_patrones, matriz=matriz)

@app.route("/guardar_datos", methods=["POST"])
def guardar_datos():
    if request.method == "POST":
        # Obtener los datos del formulario
        
        num_capas_ocultas = int(request.form["capas"])
        neuronas_capa1 = int(request.form["neuronas1"])
        activacion_capa1 = request.form["activacion1"]
        neuronas_capa2 = int(request.form["neuronas2"]) if "neuronas2" in request.form else None
        activacion_capa2 = request.form["activacion2"] if "activacion2" in request.form else None
        neuronas_capa3 = int(request.form["neuronas3"]) if "neuronas3" in request.form else None
        activacion_capa3 = request.form["activacion3"] if "activacion3" in request.form else None
        activacion_salida = request.form["activacionSalida"] if "activacionSalida" in request.form else None
        neuronas_salida = int(request.form["nSalida"]) if "nSalida" in request.form else None

        # Generar las matrices según las condiciones especificadas
        matrices = []

        if num_capas_ocultas == 1:
            WEC1 = np.random.uniform(-1, 1, (num_entradas, neuronas_capa1)).round(1).tolist()
            WC1CS = np.random.uniform(-1, 1, (neuronas_capa1, num_salidas)).round(1).tolist()
            matrices.extend([WEC1, WC1CS])
        elif num_capas_ocultas == 2:
            WEC1 = np.random.uniform(-1, 1, (num_entradas, neuronas_capa1)).round(1).tolist()
            WC1C2 = np.random.uniform(-1, 1, (neuronas_capa1, neuronas_capa2)).round(1).tolist()
            WC2CS = np.random.uniform(-1, 1, (neuronas_capa2, num_salidas)).round(1).tolist()
            matrices.extend([WEC1, WC1C2, WC2CS])
        elif num_capas_ocultas == 3:
            WEC1 = np.random.uniform(-1, 1, (num_entradas, neuronas_capa1)).round(1).tolist()
            WC1C2 = np.random.uniform(-1, 1, (neuronas_capa1, neuronas_capa2)).round(1).tolist()
            WC2C3 = np.random.uniform(-1, 1, (neuronas_capa2, neuronas_capa3)).round(1).tolist()
            WC3CS = np.random.uniform(-1, 1, (neuronas_capa3, num_salidas)).round(1).tolist()
            matrices.extend([WEC1, WC1C2, WC2C3, WC3CS])


        # Guardar los datos en un archivo de texto
        with open("datos.txt", "w") as file:
            file.write(f"Número de capas ocultas: {num_capas_ocultas}\n")
            file.write(f"Número de neuronas para la capa 1: {neuronas_capa1}, Activación: {activacion_capa1}\n")
            if neuronas_capa2 is not None:
                file.write(f"Número de neuronas para la capa 2: {neuronas_capa2}, Activación: {activacion_capa2}\n")
            if neuronas_capa3 is not None:
                file.write(f"Número de neuronas para la capa 3: {neuronas_capa3}, Activación: {activacion_capa3}\n")
            file.write(f"Número de salidas para la capa salida: {neuronas_salida}, Activación: {activacion_salida}\n")
            file.write(f"MATRIZ {matrices}\n")



        # Retorna los datos guardados
        return jsonify({
            "num_capas_ocultas": num_capas_ocultas,
            "neuronas_capa1": neuronas_capa1,
            "activacion_capa1": activacion_capa1,
            "neuronas_capa2": neuronas_capa2,
            "activacion_capa2": activacion_capa2,
            "neuronas_capa3": neuronas_capa3,
            "activacion_capa3": activacion_capa3,
            "activacion_salida": activacion_salida,
            "neuronas_salida": neuronas_salida,
            "matrices": matrices
            
        })
    

if __name__ == "__main__":
    app.run(debug=True)