rss2idec
========

Простой в использовании скрипт для автоматической ретрансляции RSS-лент в ii/idec сети.

Скрипт может работать не только на стороне ноды, но и на стороне простого поинта, отправляя сообщения удалённо. Для его работы необходимо создать конфиграционный файл (по одному файлу на каждую ленту).

Формат конфигурационного файла
------------------------------

Конфигурационный файл должен содержать следующие параметры:

  * node — адрес узла, на который будут отправляться сообщения;
  * auth — authkey поинта, от чьего имени будут отправляться сообщения;
  * echo — эхоконференция, в которую будет ретранслироваться RSS-лента;
  * base — имя файла для хранения идентификаторов уже отправленных сообщений;
  * url — адрес RSS-ленты.

Пример конфигурационного файла:

```
node http://idec.spline-online.tk/
auth authkey
echo ibash.org.ru
base ibash.org.ru.db
url http://ibash.org.ru/rss.xml
```