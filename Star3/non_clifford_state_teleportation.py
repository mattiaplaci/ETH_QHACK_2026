from tsim import Circuit
def generatore_STAR(Stato,Phi):  
    c=Circuit("""
        QUBIT_COORDS(0.5, 0.5) 0
        QUBIT_COORDS(1.5, 0.5) 1
        QUBIT_COORDS(2.5, 0.5) 2
        QUBIT_COORDS(0.5, 1.5) 3
        QUBIT_COORDS(1.5, 1.5) 4
        QUBIT_COORDS(2.5, 1.5) 5
        QUBIT_COORDS(0.5, 2.5) 6
        QUBIT_COORDS(1.5, 2.5) 7
        QUBIT_COORDS(2.5, 2.5) 8
        QUBIT_COORDS(1, 0) 9
        QUBIT_COORDS(2, 1) 10
        QUBIT_COORDS(1, 2) 11
        QUBIT_COORDS(2, 3) 12
        QUBIT_COORDS(1, 1) 13
        QUBIT_COORDS(3, 1) 14
        QUBIT_COORDS(0, 2) 15
        QUBIT_COORDS(2, 2) 16      
        R 0
        X 1       
    """
    )


def main():
    Stato=0
    Phi=0
    c=generatore_STAR(Stato,Phi)
    c.draw()