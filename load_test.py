import threading
import time
import random

# Глобальные счетчики и метрики
successful_requests = 0
failed_requests = 0
latencies = []
latencies_lock = threading.Lock()

def simulate_network_request():
    """
    Эмуляция системы:
    Имитируем обращение к БД или вызов внешнего API
    """
    # рандим делей от 10 до 50 мс
    delay_ms = random.uniform(10, 50)
    # т.к фун-ция time.sleep принимает секунды, поэтому делим на 1000
    time.sleep(delay_ms / 1000.0)
    
    # Имитируем 5% вероятность ошибки (HTTP 500)
    is_error = random.random() < 0.05
    return not is_error

def load_worker(requests_per_thread):
    """
    Логика воркеров
    """
    global successful_requests, failed_requests
    local_success = 0
    local_fail = 0
    local_latencies = []

    for _ in range(requests_per_thread):
        start_time = time.perf_counter()
        success = simulate_network_request()
        end_time = time.perf_counter()
        
        # Время в миллисекундах
        elapsed_ms = (end_time - start_time) * 1000.0
        local_latencies.append(elapsed_ms)
        
        if success:
            local_success += 1
        else:
            local_fail += 1

    # добавляем локальные метрики в глобные 
    with latencies_lock:
        successful_requests += local_success
        failed_requests += local_fail
        latencies.extend(local_latencies)

def main():
    global successful_requests, failed_requests, latencies
    
    # Сброс глобальных переменных перед запуском
    successful_requests = 0
    failed_requests = 0
    latencies = []

    # Конфигурация нагрузки
    num_threads = 500
    requests_per_thread = 20
    total_requests = num_threads * requests_per_thread

    print("Запуск нагрузочного тестирования...")
    print(f"Виртуальные пользователи (потоки): {num_threads}")
    print(f"Запросов на пользователя: {requests_per_thread}")
    print(f"Всего запланировано запросов: {total_requests}\n")

    threads = []
    test_start = time.perf_counter()

    # Запуск потоков Ramp-up 
    for i in range(num_threads):
        thread = threading.Thread(target=load_worker, args=(requests_per_thread,))
        threads.append(thread)
        thread.start()
        # задержка 100 мс между запусками потоков
        time.sleep(0.1)

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    test_end = time.perf_counter()
    test_duration = test_end - test_start

     # вывод результатов
    if len(latencies) > 0:
        avg_latency = sum(latencies) / len(latencies)
        
        # Сортировка для расчета перцентилей
        latencies.sort()
        
        # Индексы для перцентилей P 95 и P 99
        idx_95 = int(len(latencies) * 0.95)
        idx_99 = int(len(latencies) * 0.99)
        
        # Защита от выхода за границы массива
        idx_95 = min(idx_95, len(latencies) - 1)
        idx_99 = min(idx_99, len(latencies) - 1)
        
        p95 = latencies[idx_95]
        p99 = latencies[idx_99]
        
        tps = successful_requests / test_duration if test_duration > 0 else 0
    else:
        avg_latency = p95 = p99 = tps = 0

    print("\nРЕЗУЛЬТАТЫ НАГРУЗОЧНОГО ТЕСТИРОВАНИЯ \n")
    print(f"Время выполнения: {test_duration:.2f} сек.")
    print(f"Успешные запросы: {successful_requests}")
    print(f"Неудачные запросы: {failed_requests}")
    print(f"Пропускная способность (TPS): {tps:.2f} запросов/сек.")
    print(f"Среднее время отклика: {avg_latency:.2f} мс")
    print(f"95-й перцентиль (P95): {p95:.2f} мс")
    print(f"99-й перцентиль (P99): {p99:.2f} мс")

if __name__ == "__main__":
    main()
