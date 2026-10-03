# API Contract

## Схема Task

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "new",
  "created_at": "2026-01-01T12:00:00+00:00"
}
```

## Endpoint 1: Task Service

#### POST /api/tasks

Принимает:
```json
{
  "title": "Сделать лабораторную",
  "description": "Дописать Часть 2"
}
```

Возвращает:
```json
{
  "id": "uuid",
  "title": "Сделать лабораторную",
  "description": "Дописать Часть 2",
  "status": "new",
  "created_at": "2026-01-01T12:00:00+00:00"
}
```

## Endpoint 1: Task Service

#### POST /api/webhooks/task_created

Принимает объект Task:
```json
{
  "id": "uuid",
  "title": "Купить хлеб",
  "description": "Зайти в магазин",
  "status": "new",
  "created_at": "2025-01-01T12:00:00+00:00"
}
```

Возвращает 200 OK:
```json
{
  "status": "received"
}
```

## Формат вебхука

Task Service после успешного создания задачи отправляет в Notification Service
полный объект Task в формате JSON.