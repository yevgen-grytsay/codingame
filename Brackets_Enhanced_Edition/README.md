You must determine whether a given expression's bracketing can be made valid by flipping
them in-place. An expression has a valid bracketing when all the parentheses `()`,
square brackets `[]`, curly braces `{}` and angle brackets `<>` are correctly paired and nested.

You can flip a bracketing element in-place by replacing it with its counterpart, e.g.
replace a `(` with a `)`, or a `>` with a `<`. For example, converting the second parenthesis
in the expression below would make it valid:

`<{[(abc(]}> → <{[(abc)]}>`


(This is a harder version of community puzzle “Brackets, Extended Edition”. You may want to complete that one first.)

**Input**

Line 1: the number N of expressions

Next N lines: an expression

**Output**
N lines: true if the expression can be made valid by flipping elements in-place; false otherwise.

**Constraints**
N ≤ 100
number of bracketing elements ≤ 500
expression length ≤ 10000
The expression contains no whitespace.

**Example**

| Input | Output |
|-------|--------|
| 2 | |
| `<{[(abc(]}>` | true |
| `<{[(abc>}])` | false |




## I. Поиск с отсечением 1
* Если после открывающей идет такая же, то она может быть как открывающей,
так и закрывающей. Нужен поиск с возвратом.
* Если нашли закрывающую, когда ожидалась открывающая, можно разу переворачивать.
Далее ждем закрывающую такого же типа.
* Поиск с возвратом
* Можно идти сначала до конца, можно с обеих концов (особый случай `<(abc)(def)>`)
* После букв может быть только закрывающая, перед -- только открывающая

## Поиск с отсечением 2
* Сразу убирать буквы
* Если у открывающей скобки индекс парный, то у закрывающей будет непарный
и наоборот.
* Исключить комбинаторный взрыв
* Кешировать результат search