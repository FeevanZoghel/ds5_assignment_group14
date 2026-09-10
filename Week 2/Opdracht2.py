# Reg 1-50 Julien (complexe getallen)
def complex_number(x,y):
    """
    Julien 
    dit zorgt ervoor dat als er een input is voor x en y
    dat er een complex getal van gemaakt word
    """
    return x + y * 1j

c = complex_number(3,2)
print(c)



# 200 waarde voor X en Y
# bereik x = [-1.5 t/m 0.5]
# bereik y = [-1 t/m 1]

x_values = []
y_values = []

for i in range(200):
    x = -1.5 + i * (0.5 - (-1.5)) / 199
    x_values.append(x)
    y = -1 + i * (1 - (-1)) / 199
    y_values.append(y)


def complex_number_list(x_values, y_values):
    """
    Dit maakt een complex lijst met een input van y punten en x punten
    zip combineerd twee lijsten hun indexen met elkaar
    de output is een complexe lijst
    Julien
    """
    complex_list = [] 
    for x, y in zip(x_values,y_values):
        complex_list.append(x + y * 1j)
    return complex_list

# complex_list = complex_number_list(x_values, y_values)





































# Reg 51 - 100 Mathijs (iteratie & divergeren/convergere)


complex_getal = 1 + 0j

def complex_limiet(complex_getal)->tuple()
    '''
    Input: een complex getal, 
    Kijkt per getal of het convergeert of divergeert en voegt het daarna aan een lijst toe
    Output: 1 tuple met 2 lijsten erin, 
    - één met alle geconvergeerde getallen (tot nu toe nog 1)
    - één met alle gedivergeerde getallen

    '''
    diverges = []
    convergers = []
    A0 = 0 
    for i in range(1,100):
        if i==1:
            An = A0 + complex_getal
        else: 
            An = (An)**2 + complex_getal
        if abs(An)>2:
            diverges.append(complex_getal)
            break
    if abs(An)<=2:   
        convergers.append(complex_getal)
    return diverges, convergers






















# Regel 101-150 Megin (overdracht)
def Overdracht(complexe_getallen):
    """
    Uit de lijst met complexe getallen (def 1) wordt steeds het opeenvolgende 
    getal gehaald. Dit complex getal wordt vervolgens door het iteratieproces 
    (def 2) gehaald om te kijken als het divergeert/convergeert. 
    Megin 
    """

    for z in complexe_getallen:
        complex_limiet(z)







































# Regel 151-200 Fee (afbeelding)

















































#t