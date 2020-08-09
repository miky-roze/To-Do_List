from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

# Creation of a database todo.db
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Creation of an instance of a class DeclarativeMeta
Base = declarative_base()


class Table(Base):

    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Creation of a table in a database
Base.metadata.create_all(engine)

# Connecting to a database
Session = sessionmaker(bind=engine)
session = Session()

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
    """)

    decision = input()
    print()

    if decision == "0":
        print("Bye!")
        break

    elif decision == "1":
        try:
            today = datetime.today()
            # Getting all tasks that have a deadline equaling today's date
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
        except Exception:
            print("Error during reading form a database has occurred")
        else:
            print(f'Today {today.day} {today.strftime("%b")}:')
            if len(rows) == 0:
                print("Nothing to do!\n")
            else:
                for i, task in enumerate(rows):
                    print(str(i + 1) + ".", task)
                print()

    elif decision == "2":
        try:
            today = datetime.today()
            # Getting all tasks that have a deadline from a week time span
            rows = session.query(Table).filter(Table.deadline <= today + timedelta(days=6)).order_by(Table.deadline).all()
        except Exception:
            print("Error during reading form a database has occurred")
        else:
            for i in range(7):
                given_day = today + timedelta(days=i)
                print(weekdays[given_day.weekday()], given_day.day, given_day.strftime("%b") + ":")
                is_task = False
                index = 1
                for element in rows:
                    if element.deadline == given_day.date():
                        print(str(index) + ".", element)
                        is_task = True
                        index += 1
                else:
                    if not is_task:
                        print("Nothing to do!")
                    print()

    elif decision == "3":
        try:
            # Getting all tasks sorted by deadline
            rows = session.query(Table).order_by(Table.deadline).all()
        except Exception:
            print("Error during reading form a database has occurred")
        else:
            print("All tasks:")
            if len(rows) == 0:
                print("There are no tasks\n")
            else:
                for i, task in enumerate(rows):
                    print(str(i + 1) + ".", task.task + ".", task.deadline.day, task.deadline.strftime("%b"))
                print()

    elif decision == "4":
        try:
            today = datetime.today()
            # Getting all tasks that have a deadline earlier than today and sorted by deadline
            rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        except Exception:
            print("Error during reading from a database has occurred")
        else:
            print("Missed tasks:")
            if len(rows) == 0:
                print("Nothing is missed!\n")
            else:
                for i, task in enumerate(rows):
                    print(str(i + 1) + ".", task.task + ".", task.deadline.day, task.deadline.strftime("%b"))
                print()

    elif decision == "5":
        new_task = input("Enter task\n")
        new_deadline = datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d')
        try:
            new_row = Table(task=new_task, deadline=new_deadline)
            session.add(new_row)
            session.commit()
        except Exception:
            print("Error during writing into a database has occurred")
        else:
            print("The task has been added!\n")

    elif decision == "6":
        try:
            today = datetime.today()
            # Getting all tasks sorted by deadline
            rows = session.query(Table).order_by(Table.deadline).all()
        except Exception:
            print("Error during reading from a database has occurred")
        else:
            print("Choose the number of the task you want to delete:")
            if len(rows) == 0:
                print("Nothing to delete!\n")
            else:
                for i, task in enumerate(rows):
                    print(str(i + 1) + ".", task.task + ".", task.deadline.day, task.deadline.strftime("%b"))

                row_to_delete = rows[int(input()) - 1]
                try:
                    session.delete(row_to_delete)
                    session.commit()
                except Exception:
                    print("Error during a deletion has occurred")
                else:
                    print("The task has been deleted!\n")

    else:
        print("We don't have that kind of option. Try again")
