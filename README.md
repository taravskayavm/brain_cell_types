# Brain Cell Types Classification from scRNA-seq Data

Учебный проект по классификации типов клеток мозга на основе предобработанных данных single-cell RNA-seq.

Проект демонстрирует базовый цикл работы с биоинформатическими данными и машинным обучением: загрузка данных в формате `.h5ad`, анализ разметки клеток, подготовка матрицы признаков, обучение классификатора и оценка качества модели.

## Task

Цель проекта — построить модель, которая по профилю экспрессии генов относит клетку мозга к одному из трёх классов:

- `Glutamatergic`
- `GABAergic`
- `Other`

Исходные данные включают:

- `counts.h5ad` — матрица экспрессии генов и метаданные в формате AnnData;
- `cell_labels.csv` — таблица с аннотацией клеток и целевой переменной `class_label`.

Размер набора данных в учебном задании: **280 186 клеток × 254 гена**. Данные уже нормализованы и частично предобработаны.

## Data source

Данные доступны в открытом хранилище Brain Image Library:

https://download.brainimagelibrary.org/cf/1c/cf1c1a431ef8d021/processed_data/

Для запуска ноутбука нужно скачать как минимум два файла:

- `counts.h5ad`
- `cell_labels.csv`

Файлы данных не хранятся в репозитории из-за большого размера.

## Methods

В проекте используются:

- `scanpy` — чтение и базовая работа с объектом AnnData;
- `pandas` и `numpy` — обработка таблиц и массивов;
- `scikit-learn` — обучение и оценка модели;
- `RandomForestClassifier` — базовая модель классификации;
- `classification_report` и `confusion_matrix` — оценка качества классификации;
- `joblib` — сохранение обученной модели.

Основной пайплайн:

1. Загрузка `cell_labels.csv` и `counts.h5ad`.
2. Проверка структуры данных и распределения классов.
3. Формирование признаков `X` из `adata.X`.
4. Формирование целевой переменной `y` из `cell_labels['class_label']`.
5. Разделение данных на обучающую и тестовую выборки.
6. Обучение модели Random Forest.
7. Оценка качества с помощью precision, recall, F1-score и confusion matrix.
8. Сохранение модели в файл `rf_model.pkl`.

## Current results

В текущей версии ноутбука модель Random Forest показывает высокое качество на тестовой выборке:

- accuracy: около `0.99`;
- macro F1-score: около `0.99`;
- weighted F1-score: около `0.99`.

Эти результаты показывают, что по предобработанным профилям экспрессии модель хорошо отделяет три крупных класса клеток.

## Important limitations

Этот проект следует рассматривать как **учебный supervised learning-проект на предобработанных single-cell данных**, а не как полный промышленный scRNA-seq pipeline.

Текущие ограничения:

- данные уже нормализованы и предобработаны;
- в проекте нет полного QC клеток и генов;
- не выполняются стандартные этапы scRNA-seq анализа: highly variable genes, PCA, UMAP, clustering, marker genes, differential expression;
- используется случайное разделение клеток на train/test, а не разделение по `sample_id`, поэтому возможна переоценка обобщающей способности модели;
- модель решает задачу классификации по готовым меткам, а не задачу de novo-аннотации клеточных кластеров.

## How to run

1. Склонировать репозиторий.
2. Установить зависимости:

```powershell
pip install -r requirements.txt
```

3. Скачать файлы `counts.h5ad` и `cell_labels.csv` из источника данных.
4. Положить данные в локальную папку, например `data/`.
5. В ноутбуке заменить пути к файлам на свои локальные пути.
6. Запустить `TaravskayaVM_Project.ipynb`.

## Repository structure

```text
.
├── TaravskayaVM_Project.ipynb   # основной ноутбук проекта
├── requirements.txt             # зависимости Python
├── .gitignore                   # исключения для Git
└── README.md                    # описание проекта
```

## Possible improvements

Что можно улучшить в следующих версиях:

- заменить локальные абсолютные пути на относительные пути через папку `data/`;
- добавить стратифицированное разбиение данных;
- провести разбиение по `sample_id`, чтобы проверить переносимость модели между образцами;
- сравнить Random Forest с Logistic Regression, XGBoost/LightGBM или простой нейронной сетью;
- добавить анализ важности признаков и интерпретацию наиболее информативных генов;
- добавить визуализацию распределения классов и матрицы ошибок;
- оформить отдельный скрипт для обучения модели;
- добавить короткий биологический комментарий о различиях между GABAergic, Glutamatergic и Other клетками.

## Portfolio positioning

Этот проект можно описывать как:

> Educational bioinformatics/ML project: classification of mouse brain cell types using preprocessed single-cell RNA-seq data, Scanpy and scikit-learn.

Он демонстрирует начальное владение single-cell transcriptomics data formats, Python-based data analysis and supervised machine learning for biological classification tasks.
