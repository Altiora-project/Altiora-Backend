## Описание архитектуры сериализаторов

### 1. **Базовые сериализаторы**
- `BaseResponseSerializer` - базовый для всех успешных ответов
- `ErrorResponseSerializer` - базовый для всех ответов с ошибками

### 2. **Группа ProjectRequest (Заявки на проект)**
- `ProjectRequestSerializer` - основная модель заявки с валидацией
- `ProjectRequestResponseSerializer` - ответ с данными заявки
- `ProjectRequestErrorResponseSerializer` - ответ с ошибками заявки

### 3. **Группа Technology (Технологии)**
- `TechnologySerializer` - модель технологии
- `TechnologyResponseSerializer` - ответ с одной технологией
- `TechnologyListResponseSerializer` - ответ со списком технологий
- `TechnologyErrorResponseSerializer` - ответ с ошибками технологий

### 4. **Группа Service (Услуги) - самая сложная**
- `TagSerializer` - теги (используются в услугах и проектах)
- `ServiceListSerializer` - краткая информация об услугах
- `ServiceDetailSerializer` - полная информация об услуге
- `ServicePostscriptumSerializer` - постскриптум услуги
- `CaseStudySerializer` - реальные проекты

### 5. **Response сериализаторы для услуг**
- `ServiceResponseSerializer` - ответ с деталями услуги
- `ServiceListResponseSerializer` - ответ со списком услуг
- `ServiceListWithCaseStudiesResponseSerializer` - услуги + проекты
- `ServiceErrorResponseSerializer` - ошибки услуг

### 6. **Swagger документация**
- `ServiceDetailSwaggerSerializer` - для документации API
- `ServiceDetailSwaggerResponseSerializer` - ответ для Swagger
- `ServiceListWithCaseStudiesDataSerializer` - структура данных для Swagger

## Ключевые особенности архитектуры:

1. **Наследование**: Все response сериализаторы наследуются от базовых
2. **Композиция**: Сложные сериализаторы включают простые (например, `ServiceDetail` включает `Tag`, `ServicePostscriptum`, `CaseStudy`)
3. **Разделение ответственности**: Отдельные сериализаторы для списков и деталей
4. **Swagger поддержка**: Специальные сериализаторы для документации API
5. **Валидация**: Встроенная валидация в `ProjectRequestSerializer`