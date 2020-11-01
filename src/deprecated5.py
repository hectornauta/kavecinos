    def insertarGrid(self,grafico,ejes,limiteInferiorX,limiteSuperiorX,limiteInferiorY,limiteSuperiorY,k,salto):
        #¶coordenadas = list()
        cuadrados = []
        x = limiteInferiorX
        y = limiteInferiorY

        xDePrueba = x + salto/2
        yDePrueba = y + salto/2
        while(y<limiteSuperiorY):
            x = limiteInferiorX
            xDePrueba = x + salto/2
            while(x<limiteSuperiorX):
                clase = predecirClase(self.datos.datosCompletos,(xDePrueba,yDePrueba),k)
                color = self.diccionario[clase]
                cuadrado = mpatches.Rectangle((x,y),salto,salto,angle = 0.0,color=color, alpha=0.4,linewidth=0)
                #grafico.patches.extend([pyplot.Rectangle((x,y),saltoDelCuadrado,saltoDelCuadrado,
                                  #fill=True, color=color, alpha=0.5, zorder=1000,
                                  #transform=grafico.transFigure, figure=grafico)])
                cuadrados.append(cuadrado)
                ejes.add_patch(cuadrado)
                x = x + salto
                xDePrueba = x + salto/2
            y = y + salto
            yDePrueba = y + salto/2
        #for c in cuadrados:
            #print(str(c) + "/n")