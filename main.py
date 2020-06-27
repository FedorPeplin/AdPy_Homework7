from pprint import pprint
import psycopg2 as pg

def create_db(): #создает таблицы
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Student(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gpa NUMERIC(10,2),
            birth TIMESTAMP WITH TIME ZONE);
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Course(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL);
    ''')
    cur.execute('''
           CREATE TABLE if not exists Student_Course(
               id SERIAL PRIMARY KEY,
               student_id INTEGER REFERENCES Student(id),
               course_id INTEGER REFERENCES Course(id));
    ''')

def get_students(course_id): #возвращает студентов определенного курса
    cur.execute('''
                SELECT S.id, S.name FROM Student_Course SC 
                JOIN student S on S.id = SC.student_id 
                WHERE SC.course_id = %s;
                ''', (course_id, ))
    student_out = cur.fetchall()
    pprint(student_out)

def add_students(course_id, Students): # создает студентов и записывает их на курс
    for id in Students:
        cur.execute('''
            INSERT INTO Student(name, gpa, birth)
            VALUES (%s, %s, %s);
        ''', Students[id])
        cur.execute('''
            insert into Student_Course(student_id, course_id)
            values (%s, %s)
        ''', (id, course_id))

def add_student(student): #просто создает студента
    for id in student:
        cur.execute('''
            INSERT INTO Student(name, gpa, birth)
            VALUES (%s, %s, %s);
        ''', student[id])

def add_courses(course): #создает курсы
    for id in course:
        cur.execute('''
            insert into Course(id, name)
            values (%s, %s);
        ''', course[id])

def get_student(student_id): #возвращает студента по его id
    cur.execute('SELECT * FROM student WHERE id= %s', (student_id, ))
    student_out = cur.fetchall()
    pprint(student_out)

#создание дополнительной функции для удаления таблиц, чтобы была возможность
# много раз создавать таблицы
def delete_db():
    cur.execute('''DROP TABLE IF EXISTS Student CASCADE;''')
    cur.execute('''DROP TABLE IF EXISTS Course CASCADE;''')
    cur.execute('''DROP TABLE IF EXISTS Student_Course CASCADE;''')

if __name__ == '__main__':

    my_students = {
        '1': ('ИВАН', 5.00, '2000-01-01'),
        '2': ('ДА', 4.99, '1999-12-12'),
        '3': ('МАРЬЯ', 4.98, '1998-06-06')
    }

    my_courses = {
        '1': (1, 'ВЫСШАЯ МАТЕМАТИКА'),
        '2': (2, 'ФИЗИКА'),
        '3': (3, 'ФИЗКУЛЬТУРА')
    }
    with pg.connect(
            database='netology4', user='netology4', password='netology4', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        delete_db()
        create_db()
        add_student(my_students)
        def show_all_students():
            id = int(input('Всего в базе три студента, информацию о каком хотите отобразить? Введите 1/2/3 '))
            return get_student(id)
        show_all_students()
        add_courses(my_courses)
        def adding_and_showing_result():
            course=int(input('Всего имеются три курса, на какой из них мы добавим студентов? Введите 1/2/3 '))
            print ('На курсе, который Вы выбрали, имеются следующие студенты:')
            get_students(course)
            print ('На этот курс мы добавим студентов из словаря my_students')
            add_students(course, my_students)
            print('После добавления студентов на курс, который Вы выбрали, теперь на него добавляются:')
            get_students(course)
        adding_and_showing_result()