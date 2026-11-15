import threading
import time

T = 8  
M = 200000  

contador = 0
semaforo = threading.Semaphore(1)


def tarefa_com_semaforo():
  global contador
  for _ in range(M):
    semaforo.acquire()
    try:
      contador = contador + 1
    finally:
      semaforo.release()


if __name__ == "__main__":
  print(f"=== INICIANDO VERSÃO COM SEMÁFORO (T={T}, M={M}) ===")
  esperado = T * M
  print(f"Valor esperado: {esperado}")

  threads = []
  inicio = time.time()

  for _ in range(T):
    t = threading.Thread(target=tarefa_com_semaforo)
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  fim = time.time()
  tempo_gasto = fim - inicio

  print(f"Valor obtido: {contador}")
  print(f"Tempo de execução: {tempo_gasto:.4f} segundos")