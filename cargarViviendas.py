from tkinter import filedialog
import tkinter as tk
import dbf
import re


tabla = []

root = tk.Tk()
root.withdraw()

fichero = filedialog.askopenfilename(title="Abrir", initialdir='D:', filetypes=(('Todos los ficheros', '*.*'),
                                                                                ('Ficheros de Excel', '*.xlsx'),
                                                                                ('Ficheros de texto', '*.txt')))

table_OG = dbf.Table(fichero, codepage=0xf0)
table_OG.open()

print("Generando nueva tabla...")

shutil.copyfile(fichero, 'c1_modificada.dbf')

table_NEW = dbf.Table('c1_modificada.dbf', codepage=0xf0)
table_NEW.open(mode=dbf.READ_WRITE)

table_OG.close()

print("Generando índice de datos...")
index = table_NEW.create_index(lambda rec: (rec.frac, rec.radio, rec.mza, rec.lado))

fraccion = ''
radio = ''
manzana = ''
viviendas = ''
flag = True
frac_aceptada = True
rad_aceptado = True
manz_aceptada = True
viv_aceptada = True
codigo_calle = []
nombre_calle = []
lados_keys = []

while flag:
    while frac_aceptada:
        fraccion = input("Ingrese la fracción (2 dígitos): ")
        if re.search(r"^[0-9]{2}$", fraccion):
            frac_aceptada = False
        else:
            print("Ingrese un valor válido")
    while rad_aceptado:
        radio = input("Ingrese el radio (2 dígitos): ")
        if re.search(r"^[0-9]{2}$", radio):
            rad_aceptado = False
        else:
            print("Ingrese un valor válido")
    while manz_aceptada:
        manzana = input("Ingrese la manzana (4 dígitos): ")
        if re.search(r"^[0-9]{4}$", manzana):
            manz_aceptada = False
        else:
            print("Ingrese un valor válido")

    for rec in index.search(match=(fraccion, radio, manzana,), partial=True):
        lados_keys.append(rec.lado.strip())
        codigo_calle.append(rec.ccalle.strip())
        nombre_calle.append(rec.ncalle.strip())
    print(lados_keys)

    for i in range(len(lados_keys)):
        while viv_aceptada:
            viviendas = input("¿Cuántas viviendas hay en el lado " + lados_keys[i] + " (" + str(codigo_calle[i]) + ", " + str(nombre_calle[i]) + ")?")
            if re.search(r"^[0-9]+$", viviendas):
                viv_aceptada = False
            else:
                print("Ingrese un valor válido")

        for reg in index.search(match=(fraccion, radio, manzana,lados_keys[i]), partial=True):
            if int(viviendas) == 0:
                dbf.write(reg, orden_reco='', cod_tipo_v='', cod_tipo_2='LSV')
            else:
                dbf.delete(reg)
                for l in range(int(viviendas)):
                    table_NEW.append(tuple(reg))
                    dbf.write(table_NEW[len(table_NEW)-1], orden_reco=str(l+1), cod_tipo_v='A', cod_tipo_2='A')

        viv_aceptada = True

    seguir = input("¿Desea agregar más viviendas? s/n ").upper()
    if seguir == "N":
        flag = False
    lados = []
    lados_keys = []
    codigo_calle = []
    nombre_calle = []
    frac_aceptada = True
    rad_aceptado = True
    manz_aceptada = True
