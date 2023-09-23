Base объекты
------------

* id(int) - последовательный id какого-то объекта

* hash(str) - как бы тоже id, но уже рандомная строка

* base
    - status(str)
    - dates(dates)
    - info(str)

Объекты проекта
---------------

* dependence(id)
    - this(id)
    - after(id)

* dates(id)
    - planned(str)
    - actual(str)

* work(base, id)

* resource(base, id)

* payment(base, id)

Ключевые объекты
----------------

* project(base, id)
    - viewers(list[id])
    - editors(list[id])
    - works(list[id])
    - resources(list[id])
    - payments(list[id])
    - dependencies(list[id])

* user(id)
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

