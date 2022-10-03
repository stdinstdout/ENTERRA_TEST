# Тестовое задание для Enterra

## Установка и развертывание
1. В файле config.py поменять API_KEY для openapiweather
2. В файле docker-compose.yml поменять переменные и установить необходимые порты (или оставить все как есть)
3. Клонироть репозиторий

```
git clone ...
cd ...
```

4. Работа с докером
```
docker compose build
docker compose up -d
```
5. Запустить unit-тест
```
python3 unit_test.py url
```