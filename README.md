# BE CAREFUL TASKS in tasks AND PACKAGES IN DONapi/js_ast_builder/malware_samples ARE MALICIOUS

## Как сбилдить и запустить всю эту махину
#### git clone
```
git clone git@github.com:zizzs3228/INT-24.git && cd INT-24
```
#### docker compose
```
docker compose up --build -d
```
Он поднимет сразу 2 сервиса. Первый - микросервис для построения AST на JS, а второй - это AST движок на питоне. Микросервис слушает только локалхост, а gradio слушает 0.0.0.0, поэтому держите в голове. 
#### train model
Не обязательное действие, но красивый вывод я там реализовал, чтобы удобно было прочитать, как модель научилась

в директории
```
cd DONapi
```
поставить зависимости
```
pip install -r requirements.txt
```
и запустить
```
python3 train.py
```
#### запуск самого DONapi
в той же директории
```
python3 main.py -p <package_name>
```
Есть некоторый процент пакетов, который плохо парсится и выкидывает ошибку, но это ~5% пакетов. Я протестировал zip, tar, react, less, mongoose и mongodb - на них точно не падает

## Немного скриншотов выполнения программы
![image](https://github.com/zizzs3228/INT-24/assets/73750173/6a626d22-6acc-4cfb-b0b1-4280eb5757b6)

Только development tools поместился в скриншот)
Закомментировал класс, который отвечает за раскрытие compile, потому что если раскрыть compile, то eval я раскрываю, как просто код, а принт так же, как просто код, поэтому будет выведена 1. В общем, если интересно посмотреть, то закомменченный класс по этому пути: generic_ast/modules/optimizations/builtins/execution.py

![image](https://github.com/zizzs3228/INT-24/assets/73750173/f3c705fc-058f-4cd0-99c9-a81a9f309935)

train.py

![image](https://github.com/zizzs3228/INT-24/assets/73750173/6fc285b0-e820-4662-8ec1-2f8042d729ff)

DONapi на less, mongoose и mongodb (пакетах, которые не участвовали в обучении модели)
