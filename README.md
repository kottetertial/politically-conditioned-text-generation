# Моделирование политических взглядов автора в автоматически генерируемом тексте

Репозиторий содержит код, необходимый для подготовки данных и оценки работы PPLM-модели, генерирующей тексты на английском языке представителей двух политических направлений: либерального и консервативного. 

* **scrapers** - сбор данных;
* **processors/unification** - приведение собранных данных к единообразному виду;
* **processors/exploratory_analysis** - анализ собранного материала;
* **evaluation/tg_evaluation** - телеграм-бот для сбора ручной разметки;
* **evaluation/metrics** - оценка текстов с помощью автоматических метрик;

Процесс и результаты обучения модели находятся в [форке оригинального репозитория](https://github.com/kottetertial/politically-conditioned-text-generation-PPLM).