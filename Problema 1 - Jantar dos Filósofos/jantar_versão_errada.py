import random
import threading
import time

N = 5


class FilosofoIngenuo(threading.Thread):

  def __init__(self, id_filosofo, garfos, ciclos=3):
    super().__init__()
    self.id = id_filosofo
    self.garfos = garfos
    self.ciclos = ciclos
    self.esquerda = id_filosofo
    self.direita = (id_filosofo + 1) % N

  def pensar(self):
    print(f"Filósofo {self.id} está PENSANDO.")
    time.sleep(random.uniform(0.1, 0.2))

  def comer(self):
    print(f"Filósofo {self.id} está COMENDO.")
    time.sleep(random.uniform(0.1, 0.2))

  def run(self):
    for _ in range(self.ciclos):
      self.pensar()
      print(f"Filósofo {self.id} está COM FOME.")

      self.garfos[self.esquerda].acquire()
      print(f"Filósofo {self.id} pegou o garfo esquerdo ({self.esquerda}).")

      time.sleep(0.05)

      self.garfos[self.direita].acquire()
      print(f"Filósofo {self.id} pegou o garfo direito ({self.direita}).")

      self.comer()

      self.garfos[self.direita].release()
      self.garfos[self.esquerda].release()
      print(f"Filósofo {self.id} devolveu os garfos e voltou a pensar.")


if __name__ == "__main__":
  print("INICIANDO SIMULAÇÃO INGÊNUA")
  garfos = [threading.Lock() for _ in range(N)]
  filosofos = [FilosofoIngenuo(i, garfos, ciclos=3) for i in range(N)]

  for f in filosofos:
    f.start()

  for f in filosofos:
    f.join()

  print("Simulação finalizada.")