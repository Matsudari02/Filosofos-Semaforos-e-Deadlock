import sys
import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

PAUSA = 0.05
TEMPO_LIMITE = 3.0
INICIO = time.perf_counter()


def log(msg):
    agora = time.perf_counter() - INICIO
    nome = threading.current_thread().name
    # Escrita única por linha, para os logs das threads não se misturarem
    sys.stdout.write(f"[{agora:6.3f}s] [{nome}] {msg}\n")
    sys.stdout.flush()


def tarefa(rotulo):
    # Regra global: LOCK_A sempre antes do LOCK_B, em todas as threads
    log("quero o LOCK_A...")
    LOCK_A.acquire()
    log("peguei o LOCK_A")

    # Mesma pausa da versão que trava: só a ordem de aquisição mudou
    time.sleep(PAUSA)

    log("agora quero o LOCK_B...")
    LOCK_B.acquire()
    log("peguei o LOCK_B")

    log("dentro da seção crítica")
    time.sleep(PAUSA)

    log(f"{rotulo} concluiu")
    LOCK_B.release()
    LOCK_A.release()
    log("larguei os dois locks")


def main():
    threading.current_thread().name = "Principal"

    t1 = threading.Thread(target=tarefa, args=("T1",), name="Thread 1", daemon=True)
    t2 = threading.Thread(target=tarefa, args=("T2",), name="Thread 2", daemon=True)
    t1.start()
    t2.start()

    limite = time.perf_counter() + TEMPO_LIMITE
    for t in (t1, t2):
        t.join(max(0.0, limite - time.perf_counter()))

    if t1.is_alive() or t2.is_alive():
        log("alguma thread ficou presa (não era para acontecer)")
        sys.exit(1)

    log("as duas threads terminaram sem deadlock")


if __name__ == "__main__":
    main()
