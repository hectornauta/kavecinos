def insertarGridV3(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        x = limiteInferiorX
        y = limiteInferiorY

        xDePrueba = x + salto/2
        yDePrueba = y + salto/2

        tabla = []

        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            fila = []
            while(x<limiteSuperiorX):
                clases = []
                clase1 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase1)
                clase2 = predecirClase(self.datos.datosCompletos,(xDePrueba-(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase2)
                clase3 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba-(salto/2)),k)
                clases.append(clase3)
                clase4 = predecirClase(self.datos.datosCompletos,(xDePrueba+(salto/2),yDePrueba+(salto/2)),k)
                clases.append(clase4)
                contadores = Counter(clases)
                clase = masFrecuente(clases)
                calidad = contadores[clase]
                if calidad==1:
                    proporcion=0.0
                else:
                    if calidad==2:
                        proporcion=0.1
                    else:
                        if calidad==3:
                            proporcion=0.5
                        else:
                            proporcion=1
                color = self.diccionario[clase]
                celda = []
                celda.append((clase,proporcion))
                fila.append(celda)
                x = x + salto
                xDePrueba = x + salto/2
            tabla.insert(0,fila)
            y = y + salto
            yDePrueba = y + salto/2      
        print(tabla) 