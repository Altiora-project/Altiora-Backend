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
- `TagSerializer` - Сериализатор для отображения тегов
- `ServicePostscriptumSerializer` - Сериализатор для отображения постскриптума услуги.
- `CaseStudySerializer` - Сериализатор для отображения реальных проектов

- `ServiceListSimpleSerializer` - Сериализатор для отображения услуг в простом формате в списке.
- `ServiceListSerializer` - Сериализатор для отображения услуг в полном формате в списке
- `ServicesRunningLineSerializer` - Сериализатор для отображения бегущей строки с услугами
- `ServiceListResponseSerializer` - Сериализатор для ответа с данными о списке услуг и проектов. Используется в т.ч. для Swagger.

- `ServiceDetailSerializer` - Сериализатор для детального отображения услуги.
- `ServiceDetailResponseSerializer` - Сериализатор для получения услуги
- `ServiceDetailDocSerializer` - Сериализатор для документации Swagger детального просмотра услуги.
- `ServiceDetailDocResponseSerializer` - Сериализатор ответа для документации Swagger детального просмотра услуги
- `ServiceErrorResponseSerializer` - Сериализатор для ответа с ошибками при получении услуг

## Ключевые особенности архитектуры:

1. **Наследование**: Все response сериализаторы наследуются от базовых
2. **Композиция**: Сложные сериализаторы включают простые (например, `ServiceDetail` включает `Tag`, `ServicePostscriptum`, `CaseStudy`)
3. **Разделение ответственности**: Отдельные сериализаторы для списков и деталей
4. **Swagger поддержка**: Специальные сериализаторы для документации API
5. **Валидация**: Встроенная валидация в `ProjectRequestSerializer`