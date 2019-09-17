import random
import numpy as np
class neurona():
    def __init__ (self,tam):#Recibe el numero de entradas que tendra la neurona
        self.tam=tam#Numero de entradas de la neurona
        self.entradas=[]#Datos de entrada de la neurona
        self.pesos=np.random.rand(tam)#pesos para cada entrada de la neurona
        self.salida=0.0#Valor de salida de la neurona
        self.error=0.0#Error de la neurona
	#comentario

    def calcular_salida(self):#Metodo de salida
        e=2.718281828459
        self.salida=1/(1+(e**-(self.entradas*self.pesos).sum()))
        return self.salida

    def recalcular_pesos(self):#Calcular los nuevos pesos
        self.pesos=self.pesos+self.error*self.salida

class capa():
    def __init__(self,n,e):#Recibe el numero de neuronas de la capa y el numero de entradas
        self.num=n
        self.entradas=[]
        self.salidas=np.empty(n)
        self.neuronas=[]
        self.errores=np.empty(n)
        self.p=np.empty([n,e])
        for i in range(n):
            self.neuronas.append(neurona(e))#Agrega una neurona a la capa con e numero de entradas
            
        
    def procesar_entradas(self,entradas):#Recibe las entradas de la capa y retorna un array con las salidas de las neuronas de la capa
        self.entradas=entradas
        for i in range(self.num):
            self.neuronas[i].entradas=entradas
            self.salidas[i]=self.neuronas[i].calcular_salida()
        print self.salidas
        return self.salidas

    def error_salida(self,esperados):#Recibe un array con los datos de salida esperados
        for i in range(self.num):
            self.neuronas[i].error=self.neuronas[i].salida*(1-self.neuronas[i].salida)*(esperados[i]-self.neuronas[i].salida)
            self.errores[i]=self.neuronas[i].error
        return self.errores

    def error_oculta(self,errores,pesos_capa):#Recibe un array de los errores y otro de los pesos de cada neurona
        s=0.0
        for i in range(self.num):
            self.neuronas[i].error=self.neuronas[i].salida*(1-self.neuronas[i].salida)*(pesos_capa[:,i]*errores).sum()
            self.errores[i]=self.neuronas[i].error
        return self.errores

    def pesos(self):#Devuelve los pesos de todas las neuronas de la capa
        for i in range(self.num):
            self.p[i]=self.neuronas[i].pesos
        return self.p

    def recalcular_capa(self):#Recalcula los pesos de las neuronas de la capa
        for neurona in self.neuronas:
            neurona.recalcular_pesos()

class red():
    def __init__(self, capas,entradas):#Recibe un vector de enteros, siendo cada elemento del vector, el numero de neuronas que tendra la capa y el numero de entradas
        self.capas=[]
        self.salidas=np.empty(capas[-1])
        e=entradas
        for neuronas in capas:
            self.capas.append(capa(neuronas,e))
            e=neuronas

    def activar_red(self,entradas):#Activa la red con las entradas y retorna su salida
        e=entradas
        for capa in self.capas:
            e=capa.procesar_entradas(e)
        self.salidas=e
        return e

    def recalcular_red(self):#Calcular los nuevos pesos en base a los errores
        for capa in self.capas:
            capa.recalcular_capa()

    def backpropagation(self,entradas,meta):
        for i in range(83):#iteraciones
            self.activar_red(entradas)#obtener los resultados de la red
            error=self.capas[-1].error_salida(meta)#Calcular el error de la capa de salida
            for j in range(len(self.capas)-2,-1,-1):#Calcular los errores de las capas ocultas
                error=self.capas[j].error_oculta(error,self.capas[j+1].pesos())
            self.recalcular_red()

    def guardar_pesos(self,archivo):#Metodo para guardar los pesos en un archivo de texto
        #una linea separa capas,un guion separa neuronas y un asterisco los pesos
        f=open(archivo,"w")
        linea=""
        for capa in self.capas:
            for neurona in capa.neuronas:
                for peso in neurona.pesos:
                    linea+=str(peso)
                    linea+="*"
                linea+="-"
            f.write(linea+"\n")
            linea=""
        f.close()

def main():
    prueba=red([2,1],2)
    prueba.capas[0].neuronas[0].pesos=np.array([0.1,0.8])
    prueba.capas[0].neuronas[1].pesos=np.array([0.4,0.6])
    prueba.capas[1].neuronas[0].pesos=np.array([0.3,0.9])
    prueba.backpropagation(np.array([0.35,0.9]),[.5])
    prueba.guardar_pesos("pesos.txt")

def main2():
    prueba=red([2,4,1],3)
    prueba.backpropagation(np.array([0,0.35,0.9]),[1])
    prueba.guardar_pesos("pesos2.txt")
    
main()
