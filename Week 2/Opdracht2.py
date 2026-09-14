def complex_number(x,y):
    """
    Julien 
    dit zorgt ervoor dat als er een input is voor x en y
    dat er een complex getal van gemaakt word
    """
    return x + y * 1j

# c = complex_number(3,2)
# print(c)

# 200 waarde voor X en Y
# bereik x = [-1.5 t/m 0.5]
# bereik y = [-1 t/m 1]

x_values = []
y_values = []
n = 200
for i in range(n):
    x = -1.5 + i * (0.5 - (-1.5)) / (n-1)
    x_values.append(x)
    y = -1 + i * (1 - (-1)) / (n-1)
    y_values.append(y)




def complex_number_list(x_values, y_values):
    """
    Dit maakt een complex lijst met een input van y punten en x punten
    zip combineerd twee lijsten hun indexen met elkaar
    de output is een complexe lijst
    Julien
    """
    complex_list = []
    for x in x_values:
        for y in y_values:
            complex_list.append(x + y * 1j)
    return complex_list

complex_list = complex_number_list(x_values, y_values)

#complex_getal = 1 + 0j

def complex_limiet(complex_list) -> list():
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
    for complex_getal in complex_list:
        for i in range(1,100):
            if i==1:
                An = A0 + complex_getal
            else: 
                An = (An)**2 + complex_getal
            if abs(An)>2:
                diverges.append(complex_getal)
                break
        else: 
            convergers.append(complex_getal)
    return diverges, convergers


def Overdracht(complexe_getallen):
    """
        Uit de lijst met complexe getallen (def 1) wordt steeds het opeenvolgende 

        getal gehaald. Dit complex getal wordt vervolgens door het iteratieproces 
        (def 2) gehaald om te kijken als het divergeert/convergeert. 
        Megin 
        """
    return complex_limiet(complexe_getallen)

diverges, convergers = Overdracht(complex_list)
import matplotlib.pyplot as plt

complex_list = complex_number_list(x_values, y_values)

x_plot_div = [z.real for z in diverges]
y_plot_div = [z.imag for z in diverges]

x_plot_conv = [z.real for z in convergers]
y_plot_conv = [z.imag for z in convergers]

# for c in complex_list:
#     x_plot.append(c.real)
#     y_plot.append(c.imag)

plt.scatter(x_plot_div, y_plot_div, color = 'blue', s = 3)
plt.scatter(x_plot_conv, y_plot_conv, color = 'black', s = 3)
plt.xlabel("reel")
plt.ylabel("imag")
plt.title("Mandelbrott set")
plt.xlim(-1.5, 0.5)
plt.ylim(-1, 1)
plt.show()




































# Regel 151-200 Fee (afbeelding)

# import matplotlib.pyplot as plt

# complex_list = complex_number_list(x_values, y_values)

# x_plot = []
# y_plot = []

# for c in complex_list:
#     x_plot.append(c.real)
#     y_plot.append(c.imag)

# plt.scatter(x_plot, y_plot)
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Complexe getallen uit onze huidige code")
# plt.xlim(-1.5, 0.5)
# plt.ylim(-1, 1)
# plt.show()














































#t