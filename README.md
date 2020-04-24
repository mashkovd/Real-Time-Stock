 # Проект предоставляет данные об изменении стоимости ценных бумаг в режиме реального времени 
 
 ## Основные задачи, которые решает проект
 1. Накопление свечных данных по акциям в различных интервалах.
 1. Отображение изменения стоимости акций в режиме реального времени на графике.
 
 ## Для запуска проекта необходимо:
 1. Установить  [Docker Engine](https://docs.docker.com/get-docker/)
 и [Docker Compose](https://docs.docker.com/compose/install/).
 1. Получить token для работы с [Тинькофф Инвестиции OpenApi](https://github.com/TinkoffCreditSystems/invest-openapi)
 1. Изменить значение tinkoff_token на token полученный из предыдущего шага(достаточно Sandbox-token)
 1. запустить приложение командой docker-compose up из рабочего каталога
 
 ### Используемые библиотеки 
 
 1. Работа с OpenAPI Тинькофф Инвестиции [open-api-python-client](open-api-python-client)
 1. Построение графиков [Dash](https://dash.plotly.com/)
 1. Bootstrap components для Dash [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) 
 