# Ходаков Максим ТТП-42 
## Лабораторна робота №4 з дисципліни "Інтелектуальні системи"


### Приклад використання CSP в задачі розміщення N ферзей

```
Це рев’ю стосується коду, який реалізує задачу CSP (Constraint Satisfaction Problem) для гри N-Ферзів із використанням пошуку з поверненням. Код також містить реалізацію евристик та відстеження вартості шляху. Нижче наведено аналіз основних компонентів, ефективності алгоритму та рекомендації для покращення.

1. Загальна структура
Код добре структурований і складається з кількох ключових частин:

Клас CSP, який реалізує загальний алгоритм CSP з використанням пошуку з поверненням.
Функція обмежень, що визначає, чи атакують ферзі один одного.
Основний блок, який ініціалізує змінні, домени та виконує розв'язання задачі.
Рішення читається легко, а використання евристик додає ефективності алгоритму.

2. Оцінка основних компонентів
Алгоритм реалізує стандартний підхід до розв'язання задачі CSP із пошуком у глибину (пошук з поверненням). Код відповідає вимогам:

Використовує порожнє присвоєння як початковий стан.
На кожному кроці вибирає змінну, присвоює їй значення та перевіряє на узгодженість.
Виконує перевірку мети (чи всім змінним присвоєно значення).
Відстежує вартість шляху (кількість кроків).
Це дозволяє правильно та ефективно розв’язувати задачу.

Евристики
У коді реалізовано три евристики:

MRV (мінімальна кількість решти значень):

Вибирає змінну, домен якої має найменшу кількість можливих значень. Це зменшує кількість потенційних гілок у дереві пошуку.
Ступенева евристика:

Якщо декілька змінних мають однаковий мінімальний розмір домену, вибирається змінна з найбільшим ступенем (найбільшою кількістю обмежень із сусідніми змінними). Це сприяє зменшенню конфліктів.
Евристика найменш обмежувального значення:

Серед усіх можливих значень для змінної вибирається значення, яке спричиняє найменшу кількість конфліктів для інших змінних.
Ці евристики суттєво покращують продуктивність, зменшуючи кількість необхідних повернень.

Відстеження вартості шляху
Код відстежує вартість шляху, яка збільшується на кожному кроці при присвоєнні значення змінній. Це корисно для оцінки ефективності алгоритму, особливо при тестуванні на більших розмірах дошки.

3. Ефективність та продуктивність
Код демонструє непогану ефективність для стандартних задач (наприклад, N=8). Використання евристик суттєво зменшує кількість рекурсивних викликів і прискорює пошук рішення.

Проте для більших значень N може бути корисним впровадження додаткових оптимізацій, таких як:

Проріджування доменів (Forward Checking), щоб виключати несумісні значення одразу після кожного присвоєння.
Використання алгоритму підтримки узгодженості дуг (AC-3), щоб підтримувати узгодженість між змінними під час виконання алгоритму.

4. Рекомендації щодо покращення
Оптимізація обчислень:

Реалізувати кешування підрахунків під час використання евристики найменш обмежувального значення.
У ступеневій евристиці враховувати реальні обмеження між змінними, а не лише загальну кількість неприсвоєних змінних.
Додаткові оптимізації:

Впровадити проріджування доменів, щоб зменшити кількість конфліктів ще до рекурсивних викликів.
Додати перевірку узгодженості дуг для забезпечення узгодженості між усіма змінними.
Покращення структури коду:

Додати коментарі для складних частин коду.
Розділити функціональність на менші модулі або функції для кращої читабельності.
Тестування на більших значеннях N:

Перевірити продуктивність алгоритму для більших значень N (наприклад, N=16 чи N=20).
Визначити, які частини алгоритму потребують оптимізації.

5. Висновок
Код реалізує всі основні аспекти CSP, включаючи вибір змінних, призначення значень, перевірку узгодженості та пошук рішення. Використання евристик забезпечує ефективність, а відстеження вартості шляху дозволяє аналізувати продуктивність алгоритму.
```