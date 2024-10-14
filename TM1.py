class TuringMachine:
    def __init__(self, tape, blank_symbol=' '):
        self.tape = list(tape)  # Стрічка машини Тьюринга
        self.head_position = 0  # Початкова позиція головки
        self.state = 'q0'  # Початковий стан
        self.blank_symbol = blank_symbol  # Символ для пустої клітинки
        self.transitions = self.define_transitions()

    def define_transitions(self):
        """
        Визначення переходів машини Тьюринга.
        Переходи представлені у вигляді: { (стан, символ): (новий_стан, новий_символ, напрямок) }
        """
        return {
            ('q0', '1'): ('q0', '1', 'R'),  # Пропускати символи '1' вправо
            ('q0', '0'): ('q1', '1', 'N'),  # Зустріли '0' — переходимо в стан q1 і видаляємо розділювач
            ('q1', '1'): ('q1', '1','R'),  # Йдемо вліво, щоб знайти кінець лівого числа
            ('q1', '0'): ('q2', ' ', 'L'),  #
            ('q1', ' '): ('q2', ' ', 'L'),  #
            ('q2', '1'): ('qH', ' ', 'R'),  #
            ('q2', '0'): ('qH', ' ', 'R'),  #
            ('q2', ' '): ('qH', ' ', 'R')  #
        }

    def step(self):
        """Виконати один крок машини Тьюринга згідно з таблицею переходів."""
        current_symbol = self.tape[self.head_position]
        action = self.transitions.get((self.state, current_symbol))

        if action:
            new_state, new_symbol, direction = action
            # Змінюємо поточний символ на новий
            old_symbol = self.tape[self.head_position]
            self.tape[self.head_position] = new_symbol
            # Змінюємо стан
            self.state = new_state
            # Рухаємо головку
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1
            # Нічого не робимо, якщо напрямок 'N' (halt)
            return old_symbol, new_symbol

    def run(self):
        """Виконувати кроки машини Тьюринга, поки не досягне стану halt (qH)."""
        while self.state != 'qH':
            a,b = self.step()
            print(f"Стан: {self.state}, Стрічка: {''.join(self.tape)}, Головка на позиції: {self.head_position}, читає {a}, запис {b} ")
            input()

        print(f"Кінцевий результат: {''.join(self.tape)}")


# Створимо стрічку, яка представляє два числа в унарній системі
# Наприклад, числа 3 і 2 будуть представлені як "111011" (три одиниці, нуль як роздільник, дві одиниці)
tape = "111011 "

# Створюємо і запускаємо машину Тьюринга
tm = TuringMachine(tape)
tm.run()
