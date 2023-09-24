Base объекты
------------

* *NAME_id*(int) - последовательный id какого-то объекта

* hash(str) - как бы тоже id, но уже рандомная строка

* base
    - status(str)
    - info(str)
    - *date_planned*(datetime.datetime)
    - *date_actual*(datetime.datetime)

Наследуемые объекты проекта
---------------

* work(base)
    - *obj_id*(int)

* resource(base)
    - *obj_id*(int)

* payment(base)
    - *obj_id*(int)

Ключевые объекты
----------------

* project(base)
    - *proj_id*(int)
    - name(str)
    - creator(str)
    - viewers(list[*user_id*])
    - editors(list[*user_id*])
    - works(list[*obj_id*])
    - resources(list[*obj_id*])
    - payments(list[*obj_id*])
    - dependencies(dict[from[*obj_id*]: to[list[*obj_id*]]])

* user
    - *user_id*(int)
    - *full_name*(str)
    - email(str)
    - password(str)
    - info(str)
    - *created_projs*(list[id])
    - *other_projs*(list[id])

Дополнительные объекты
----------------------

* session(hash)
    - user(id)

* shared(hash)
    - project(id)

Описание
--------

все что написано как *field*(*base_field*)
значит что *field* как бы наследуется от *base_field*

все id - числа, но контексты у некоторых объектов разные
существуют 4 типа id
- *hash*
- *user_id*
- *proj_id*
- *obj_id*

