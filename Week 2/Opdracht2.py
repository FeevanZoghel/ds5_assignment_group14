# Reg 1-50 Julien
def complex(x,y):
    c = x + y * 'i'

    return c













































# Reg 51 - 100 Mathijs


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





















































# Regel 101-150 Megin

















































# Regel 151-200 Fee

















































#t