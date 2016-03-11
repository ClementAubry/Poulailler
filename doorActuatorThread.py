import sys
from threading import Thread
import time

class openDoorActuatorThread(Thread):

    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""


# Création des threads
thread_1 = Afficheur("canard")
thread_2 = Afficheur("TORTUE")

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()
