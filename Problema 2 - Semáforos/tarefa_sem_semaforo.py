import threading
import time

T = 8
M = 200000  

contador = 0


def tarefa_sem_semaforo():
  global contador
  for _ in range(M):
    temp = contador
    time.sleep(0)
    contador = temp + 1


if __name__ == "__main__":
  print(f"=== INICIANDO VERSÃO SEM SEMÁFORO (T={T}, M={M}) ===")
  esperado = T * M
  print(f"Valor esperado: {esperado}")

  threads = []
  inicio = time.time()

  for _ in range(T):
    t = threading.Thread(target=tarefa_sem_semaforo)
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  fim = time.time()
  tempo_gasto = fim - inicio

  print(f"Valor obtido: {contador}")
  print(f"Diferença: {esperado - contador}")
  print(f"Tempo de execução: {tempo_gasto:.4f} segundos")