import numpy as np
import pandas as pd
import openpyxl

def cargarMatriz():
  minsumo = np.loadtxt('Matriz_IP.csv', int, delimiter=',')
  return minsumo

def formulaM(matrix1, matrix2, matrix3): #M1 = insumo , M2 = identidad , M3 = e
  resta = matrix2 - matrix1
  np.set_printoptions(precision=7, suppress=True)
  print("\nResta In - B\n")
  print(resta)
  rinv = np.linalg.inv(resta)
  np.set_printoptions(precision=3, suppress=True) 
  print("\nInversa de la resta\n")
  print(rinv)
  matx = np.dot(rinv,matrix3)
  return matx

#Programa Principal 
lipro = ["Pan de sal", "Pan de dulce", "Pan de canela","Cachos", "Pan Mixto", "Palanqueta", "Queque", "Galletas", "Donas"]
liven = []
for prod in lipro:
    prodv = int(input(f"Ingrese la cantidad en unidades (1 docena = 12 unidades) a producir de {prod.lower()}: "))
    liven.append(prodv)
tventas = np.array(liven)
mtrinp = cargarMatriz()

# Matriz Insumo-Prodcuto
print("\nMatriz Insumo-Producto")
mtrinpact = np.concatenate((mtrinp, [tventas]), axis=0)
print(mtrinpact)

vgram = np.array([46,65,62,60,65,100,70,30,65]) #Vector de gramos para cada prodcuto
vgramdc = vgram * 12
tvendcn = tventas / 12 #Vector de las docenas de cada producto
grmdmnd = vgramdc * tvendcn
grmdmnd = np.array(grmdmnd,int)
mtrinp[-1,:] = mtrinp[-1,:] * 50 #Conversión de huevos a gramos
mtrzip2 = np.concatenate((mtrinp, [grmdmnd]), axis=0)
totgrm = mtrzip2.sum(axis = 0) #Total de gramos

# Matriz Insumo-Prodcuto actualizada
print("\nMatriz Insumo-Producto actualizada")
mtrinpact2 = np.concatenate((mtrzip2, [totgrm]), axis=0)
print(mtrinpact2)

#Matriz B
matrizA = mtrinpact2[:-2,:]
matrizB = matrizA / totgrm
np.set_printoptions(precision=7, suppress=True)
print("\n\nMatriz B")
print(matrizB)

#Matriz e
mtre = np.array([5520,7020,1488,1440,1560,1200,840,360,780])
limtre = mtre.tolist()
mtre = mtre.reshape([9,1])
print("\nMatriz e")
print(mtre)

#Matriz Identidad
print("\nMatriz identidad")
mtri = np.identity(9)
print(mtri)

#Vector X
lix = ["a","b","c","d","f","g","h","i","j"]

#Vector resultado del modelo de Leontief
matx = formulaM(matrizB,mtri,mtre)
matx = np.round(matx, decimals=3)
limatx = matx.tolist()
print("\nCantidad de ingredientes diarios aplicando Leontief\n")
for i in range(len(lix)):
  print(f"{lix[i]} = {limatx[i]}")

d = {}
dia = matx.tolist()
sem = matx * 7
sem = np.round(sem, decimals=3)
sem = sem.tolist()
mes = matx * 30
mes = np.round(mes, decimals=3)
mes = mes.tolist()

d["Diarios"] = dia
d["Semanales"] = sem
d["Mensuales"] = mes

#Guardar los datos en un archivo excel
data = pd.DataFrame(d, index=lipro)
data.to_excel("Tabla-Leontief-Gramos.xlsx", sheet_name="hoja1")