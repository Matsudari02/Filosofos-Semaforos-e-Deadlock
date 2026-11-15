import random
import threading
import time

N = 5


class FilosofoHierarquia(threading.Thread):

  def __init__(self, id_filosofo, garfos, ciclos=3):
    super().__init__()
    self.id = id_filosofo
    self.garfos = garfos
    self.ciclos = ciclos

    g1 = id_filosofo
    g2 = (id_filosofo + 1) % N
    self.primeiro = min(g1, g2)
    self.segundo = max(g1, g2)

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

      self.garfos[self.primeiro].acquire()
      print(
          f"Filósofo {self.id} pegou o primeiro garfo (índice {self.primeiro})."
      )

      self.garfos[self.segundo].acquire()
      print(
          f"Filósofo {self.id} pegou o segundo garfo (índice {self.segundo})."
      )

      self.comer()

      self.garfos[self.segundo].release()
      self.garfos[self.primeiro].release()
      print(f"Filósofo {self.id} devolveu os garfos e voltou a pensar.")


if __name__ == "__main__":
  print("INICIANDO SIMULAÇÃO CERTA")
  garfos = [threading.Lock() for _ in range(N)]
  filosofos = [FilosofoHierarquia(i, garfos, ciclos=3) for i in range(N)]

  for f in filosofos:
    f.start()

  for f in filosofos:
    f.join()

  print("\nTodos os filósofos concluíram seus ciclos sem deadlock!")