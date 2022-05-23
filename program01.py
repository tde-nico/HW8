'''
Un pixel artist di fama mondiale di nome Fred Zuppa ha recentemente
prodotto diversi capolavori sottoforma di immagini quadrate raster
codificate su pixels in scala di grigi. Le immagini che ha disegnato
possono prendere valori da 0 a 255 compresi. Sfortunatamente le famose
opere sono andate perdute in quanto il suo disco rigido (ahilui!) ha
smesso di funzionare e ovviamente il buon Fred e' disperato. I
programmi per recuperarle dal filesystem non funzionano purtroppo e
cosi' Fred si affida al suo amico informatico di fiducia, il quale gli
dice:

   "Fratello, in verita' ti dico, se ti ricordi la dimensione delle
   immagini e i valori dei pixel di cui erano formate e delle
   proprieta' particolari delle tue opere, allora possiamo provare a
   scrivere un generatore ricorsivo che le produca tutte in base ai
   tuoi input, cosi' facendo possiamo provare a recuperarle!"

Il mattino seguente Fred riesce a dare le informazioni necessarie
sottoforma di:
   1. `D` parametro intero che descrive la dimensione dell'immagine
       quadrata.
   2. `colors` una lista di interi che descrive i colori delle
      immagini di Fred.  I colori di Fred sono compresi fra 0, 255.
      colors puo' essere quindi [128, 0, 255] mentre NON puo' essere
      [-100, 999]
   3. Un testo `img_properties` che descrive le proprieta' delle sue
      immagini: Il testo puo' descrivere nessuna proprita' (stringa
      vuota) oppure puo' descrivere una proprieta' che riguarda i
      pattern che le immagini devono contenere.

       Ad esempio:

       Se `img_properties` e' vuota allora le immagini non devono soddisfare
       nessuna proprieta'. Viceversa se `img_properties` e' uguale a
       'pattern_{type}_' allora signifca che le immagini devono
       mostrare il pattern di tipo `type` specificato nella stringa.
       Il pattern puo' essere di un solo tipo.

       I tipi di pattern possibili sono i quattro seguenti:
          a) 'pattern_diff_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine
          di dimensione uguale a 2x2, questa sottoimmagine deve avere i
          pixel di colore tutti diversi.

                 valid        not valid
            |  96 | 255 |   |   0 | 255 |
            | 128 |   0 |   | 255 |  96 |


          b) 'pattern_cross_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine
          di dimensione uguale a 2x2, questa sottoimmagine deve
          avere i pixel sulla diagonale uguali fra loro e i pixel
          sulla antidiagonale uguale fra loro ma pixel delle due
          diagonali devono essere diverse.

               valid          not valid     not valid
            |  96 | 255 |   |  0 | 255 |   | 61 | 61 |
            | 255 |  96 |   | 96 |   0 |   | 61 | 61 |

          c) 'pattern_hrect_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine di
          dimensione 2x2, questa sottoimmagine deve avere i pixel
          sulle righe tutti uguali ma righe adiacenti di colore
          diverso.

                 valid       not valid        not valid
            |   0 |   0 |   | 255 | 255 |    | 43 | 43 |
            | 128 | 128 |   | 0   | 255 |    | 43 | 43 |

          d) 'pattern_vrect_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine di
          dimensione 2x2, questa sottoimmagine deve avere i pixel
          sulle colonne tutti uguali ma colonne adiacenti di colore
          diverso.

                valid         not  valid    not valid
             | 0 | 255 |     | 0  | 0  |    | 22 | 22 |
             | 0 | 255 |     | 0  | 255|    | 22 | 22 |

Implementare la funzione ricorsiva o che usa metodi ricorsivi:
  
      images = ex(colors, D, img_properties)

che prende in ingresso la lista di colori `colors`, la dimensione
delle immagini `D` e una stringa `img_properties` che ne descrive le
proprieta' e generi ricorsivamente tutte le immagini seguendo le
proprieta' suddette.  La funzione deve restituire l'elenco di tutte le
immagini come una lista di immagini.  Ciascuna immagine e' una tupla di
tuple dove ogni intensita' di grigio e' un intero.
L'ordine in cui si generano le immagini non conta.

     Esempio: immagine 2x2 di zeri (tutto nero) e':
        img = ( (0, 0), (0, 0), )


Il timeout per ciascun test è di 1 secondo.

***
E' fortemente consigliato di modellare il problema come un albero di
gioco, cercando di propagare le solo le "mosse" necessarie nella
ricorsione e quindi nella costruzione della soluzione in maniera
efficiente; oppure, in maniera alternativa, cercate di "potare" l'albero di
gioco il prima possibile.
***

Potete visualizzare tutte le immagini da generare invocando

     python test_01.py data/images_data_15.json

questo salva su disco tutte le immagini attese del test 15 e crea
un file HTML di nome `images_data_15.html` nella directory radice
del HW con cui e' possibile vedere le immagini aprendo il file html
con browser web.
'''

class Img:
    images = []
    def __init__(self, conf):
        self._sons = []
        self._conf = conf

    def pattern(self, color, y, x):
        return 1

    def apply(self, y, x):
        for color in self.colors:
            if self.pattern(color, y, x):
                self._conf[y][x] = color
                self._sons.append(self.P(list(map(list, self._conf))))

    def generate(self, y, x):
        if x >= self.D:
            x = 0
            y += 1
        if y >= self.D:
            self.images.append(tuple([tuple(row) for row in self._conf]))
            return
        self.apply(y, x)
        for son in self._sons:
            son.generate(y, x+1)



class diff(Img):
    def pattern(self, color, y, x):
        return not ((x and (color == self._conf[y-1][x-1] or color == self._conf[y][x-1]))
            or ((x != self.D-1) and (color == self._conf[y-1][x+1]))
            or color == self._conf[y-1][x])


class cross(Img):
    def pattern(self, color, y, x):
        return not (x and color == self._conf[y][x-1])

    def apply(self, y, x):
        if y:
            if x:
                self._conf[y][x] = self._conf[y-1][x-1]
            else:
                self._conf[y][x] = self._conf[y-1][x+1]
        elif x > 1:
            self._conf[y][x] = self._conf[y][x-2]
        else:
            for color in self.colors:
                if self.pattern(color, y, x):
                    self._conf[y][x] = color
                    self._sons.append(self.P(list(map(list, self._conf))))
            return
        self._sons.append(self.P(list(map(list, self._conf))))


class hrect(Img):
    def pattern(self, color, y, x):
        return color != self._conf[y-1][x]

    def generate(self, y, x):
        if y >= self.D:
            self.images.append(tuple([tuple([self._conf[row][0]]*self.D) for row in range(self.D)]))
            return
        self.apply(y, x)
        for son in self._sons:
            son.generate(y+1, x)


class vrect(Img):
    def pattern(self, color, y, x):
        return not (x and color == self._conf[y][x-1])

    def generate(self, y, x):
        if x >= self.D:
            self.images.append(tuple([tuple(self._conf[0]) for row in range(self.D)]))
            return
        self.apply(y, x)
        for son in self._sons:
            son.generate(y, x+1)





def get_pattern(pattern):
    if pattern == 'pattern_diff_':
        return diff
    if pattern == 'pattern_cross_':
        return cross
    if pattern == 'pattern_hrect_':
        return hrect
    if pattern == 'pattern_vrect_':
        return vrect
    return Img

def ex(colors, D, img_properties):
    conf = [[-1]*D for i in range(D)]
    pattern = get_pattern(img_properties)
    pattern.P = pattern
    pattern.D = D
    pattern.colors = colors
    first = pattern(conf)
    first.generate(0,0)
    return pattern.images
    
    

if __name__ == '__main__':
    #'''
    import json
    inp = 'data/images_data_09.json'
    with open(inp) as f:
        js = json.load(f)
    data = js['input']
    print(data)
    print('')
    #'''
    res = ex(data['colors'], data['D'], data['img_properties'])
    for img in res:
        for row in img:
            print(row)
        print('')
    #print(res)
    print(len(res))
    #'''
    










