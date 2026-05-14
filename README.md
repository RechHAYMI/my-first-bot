# 📊 MoneyFlow Bot | Day 40+ Progress

### 🐍 О проекте
Приветсвую всех, это мой первый "масштабный" проект на python, сейчас это мой основной проект.

Бот помогает вести учет финансов, но главная его цель для меня — **научиться писать профессиональный код**.

---

### 🚀 Что под капотом (Stack)
Я выбрал современные инструменты, которые используют в реальном продакшене:

* **Framework:** [aiogram 3.x](https://github.com/aiogram/aiogram) 
* **Database:** SQLite3 (переезжаем на PostgreSQL)
* **Architecture:** Middleware, FSM (Finite State Machine), Router-based logic
* **OS:** Разработка ведется полностью на **Arch Linux** 🖥️

---

### 🔥 Ключевые фичи
- ✅ **Admin ShadowMiddleware:** Умная проверка прав доступа.
- 📬 **Smart Broadcast:** Система рассылки через `copy_to` для сохранения оригинального контента.
- 📝 **FSM Logic:** Четкие сценарии взаимодействия, чтобы пользователь не запутался.
- 📈 **Future:** В планах графики статистики через Matplotlib.
- ⌨️ **Inline Keyboard** Инлайн кнопочки

---

### 📂 Структура проекта
Я стараюсь следовать принципам чистого кода, поэтому проект разбит на модули:
- `handlers/` — обработка команд и сообщений.
- `middlewares/` — фильтры и проверка прав.
- `database/` — вся логика работы с БД.
- `states/` — состояния для FSM.
- `Keyboard/` — Кнопки.

---

### 🛠 Как запустить (для тех, кто хочет потыкать)
1. Склонируйте репозиторий:
   ```bash
   git clone [https://github.com/твой_ник/твой_репозиторий.git](https://github.com/твой_ник/твой_репозиторий.git)
2. Установите зависимости:
   pip install -r requirements.txt
3. Создайте .env файл и добавьте туда свой BOT_TOKEN.
4. Запускайте python main.py







# 📊 MoneyFlow Bot | Day 40+ Progress

### 🐍 About the Project
Hello everyone, this is my first "large-scale" project in Python, and it's currently my main project.

The bot helps me keep track of my finances, but its main goal for me is to learn how to write professional code.

---

### 🚀 What's Under the Hood (Stack)
I chose modern tools that are used in real production:

* **Framework:** [aiogram 3.x](https://github.com/aiogram/aiogram)
* **Database:** SQLite3 (we're moving to PostgreSQL)
* **Architecture:** Middleware, FSM (Finite State Machine), Router-based logic
* **OS:** Development is conducted entirely on **Arch Linux** 🖥️

---

### 🔥 Key Features
- ✅ **Admin ShadowMiddleware:** Smart access rights checking.
- 📬 **Smart Broadcast:** Copy-to broadcasting system to preserve original content.
- 📝 **FSM Logic:** Clear interaction scenarios to avoid user confusion.
- 📈 **Future:** Plans include statistics graphics via Matplotlib.
- ⌨️ **Inline Keyboard** Inline buttons

---

### 📂 Project Structure
I try to follow clean code principles, so the project is divided into modules:
- `handlers/` — command and message processing.
- `middlewares/` — filters and permissions checking.
- `database/` — all database logic.
- `states/` — states for FSM.
- `Keyboard/` — Buttons.

---

### 🛠 How to run (for those who want to tinker)
1. Clone the repository:
```bash
    git clone [https://github.com/твой_ник/твой_реписорий.git](https://github.com/твой_ник/твой_реписорий.git)
2. Install dependencies:
pip install -r requirements.txt
3. Create a .env file and add your BOT_TOKEN there.
4. Run python main.py
