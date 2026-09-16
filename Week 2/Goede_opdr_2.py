import numpy as np
import matplotlib.pyplot as plt


# Julien
def complex_number(x: float, y: float) -> complex:
    """
    Maakt van een x- en y-waarde een complex getal.

    Args:
        x (float): De x-waarde.
        y (float): De y-waarde.

    Returns:
        complex: Het complexe getal.

    Julien
    """
    return x + y * 1j


# Mathijs
def complex_limiet(complex_getal: complex) -> int:
    """
    Bepaalt de diverging index van een complex getal.

    Als de absolute waarde groter wordt dan 2,
    wordt het iteratienummer teruggegeven.

    Als dit binnen 100 iteraties niet gebeurt,
    wordt 0 teruggegeven.

    Args:
        complex_getal (complex): Het complexe getal dat getest wordt.

    Returns:
        int: De diverging index.

    Mathijs
    """
    an = 0

    for i in range(1, 101):
        an = an**2 + complex_getal

        if abs(an) > 2:
            return i

    return 0


# Megin
def create_mandel_data(width: int) -> np.ndarray:
    """
    Maakt een vierkante NumPy-array met diverging indices.

    Args:
        width (int): Breedte en hoogte van de afbeelding.

    Returns:
        np.ndarray: Matrix met diverging indices.

    Megin
    """
    x_values = np.linspace(-1.5, 0.5, width)
    y_values = np.linspace(-1, 1, width)

    image = np.zeros((width, width))

    for row in range(width):
        for column in range(width):

            x = x_values[column]
            y = y_values[row]

            c = complex_number(x, y)

            diverging_index = complex_limiet(c)

            image[row, column] = diverging_index

    return image


# Fee
def draw_mandel(width: int) -> None:
    """
    Tekent de Mandelbrot-afbeelding.

    Args:
        width (int): Breedte en hoogte van de afbeelding.

    Returns:
        None

    Fee
    """
    image = create_mandel_data(width)

    plt.imshow(
        image,
        extent=[-1.5, 0.5, -1, 1],
        origin="lower",
        cmap="hot"
    )

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Mandelbrot set")
    plt.colorbar(label="Diverging index")

    plt.show()


draw_mandel(200)