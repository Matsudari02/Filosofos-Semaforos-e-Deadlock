import sys
import threading
import time
import traceback

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


def thread_1():
    log("quero o LOCK_A...")
    LOCK_A.acquire()
    log("peguei o LOCK_A")

    log("dormindo 50ms (dá tempo da Thread 2 pegar o LOCK_B)")
    time.sleep(PAUSA)

    log("agora quero o LOCK_B, sem largar o LOCK_A...")
    LOCK_B.acquire()
    log("peguei o LOCK_B")

    log("T1 concluiu")
    LOCK_B.release()
    LOCK_A.release()


def thread_2():
    log("quero o LOCK_B...")
    LOCK_B.acquire()
    log("peguei o LOCK_B")

    log("dormindo 50ms (dá tempo da Thread 1 pegar o LOCK_A)")
    time.sleep(PAUSA)

    log("agora quero o LOCK_A, sem largar o LOCK_B...")
    LOCK_A.acquire()
    log("peguei o LOCK_A")

    log("T2 concluiu")
    LOCK_A.release()
    LOCK_B.release()


def diagnosticar():
    quadros = sys._current_frames()

    print("\n" + "=" * 62)
    print(f"DEADLOCK: nenhum progresso após {TEMPO_LIMITE:.0f}s")
    print("=" * 62)

    print("Threads vivas (threading.enumerate):")
    for t in threading.enumerate():
        if t is threading.current_thread():
            print(f"  - {t.name}: executando este diagnóstico")
            continue
        ponto = traceback.extract_stack(quadros[t.ident])[-1]
        print(f"  - {t.name}: BLOQUEADA em {ponto.name}(), "
              f"linha {ponto.lineno} -> {ponto.line}")

    print(f"\nLOCK_A retido: {LOCK_A.locked()} | LOCK_B retido: {LOCK_B.locked()}")
    print(
        "\nCiclo de espera:\n"
        "  Thread 1 segura LOCK_A e espera LOCK_B\n"
        "  Thread 2 segura LOCK_B e espera LOCK_A"
    )


def main():
    threading.current_thread().name = "Principal"

    t1 = threading.Thread(target=thread_1, name="Thread 1", daemon=True)
    t2 = threading.Thread(target=thread_2, name="Thread 2", daemon=True)
    t1.start()
    t2.start()

    # Daemon + join com limite: detecta a trava sem prender o terminal
    limite = time.perf_counter() + TEMPO_LIMITE
    for t in (t1, t2):
        t.join(max(0.0, limite - time.perf_counter()))

    if t1.is_alive() or t2.is_alive():
        diagnosticar()
        sys.exit(1)

    log("as duas threads terminaram (o deadlock não aconteceu dessa vez)")


if __name__ == "__main__":
    main()
