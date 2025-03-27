import pandas as pd

data = {
    'student_id': [101,101,101,101,101,102,102,102,102,103,103,103,103,103,104,104,104,104,104,],
    'attendance_date': pd.to_datetime(['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05', '2024-03-02',
                                        '2024-03-03','2024-03-04', '2024-03-05', '2024-03-05', '2024-03-06' , '2024-03-07' , '2024-03-08', '2024-03-09', '2024-03-01','2024-03-02','2024-03-03','2024-03-04','2024-03-05']),
    'status': ['Absent', 'Absent', 'Absent', 'Absent', 'Present', 'Absent',
               'Absent', 'Absent', 'Absent', 'Absent', 'Absent','Absent','Absent','Absent','Present','Present','Absent','Present','Present',]
}

attendance = pd.DataFrame(data)

attendance['absence_streak'] = (attendance['status'] == 'Absent').astype(int).groupby(attendance['student_id']).cumsum()
attendance['absence_group'] = (attendance['status'] != 'Absent').astype(int).groupby([attendance['student_id'], attendance['absence_streak']]).cumsum()

absent_streaks = attendance[attendance['status'] == 'Absent'].groupby(['student_id', 'absence_group']).agg(
    absence_start_date=('attendance_date', 'min'),
    absence_end_date=('attendance_date', 'max'),
    total_absent_days=('attendance_date', 'count')
).reset_index(drop=True)

latest_absent_streaks = absent_streaks[absent_streaks['total_absent_days'] > 3].sort_values(by=['student_id', 'absence_start_date'], ascending=False).drop_duplicates(subset=['student_id'])

result = latest_absent_streaks[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days']]
print(result)
import pandas as pd

data = {
    'student_id': [101, 102, 103, 104, 105,],
    'student_name': ([' alice jhonson', 'bob smith', 'charile brown', 'david lee', 'eva white', '2023-10-06',
                                        ]),
    'parets mail id': ['alice_parents@gmail.com', 'bob_parents@gmail,com', 'invalid_email.com', 'invalid_email.com', 'eva white@example.com', ]
}

attendance = pd.DataFrame(data)

attendance['absence_streak'] = (attendance['status'] == 'Absent').astype(int).groupby(attendance['student_id']).cumsum()
attendance['absence_group'] = (attendance['status'] != 'Absent').astype(int).groupby([attendance['student_id'], attendance['absence_streak']]).cumsum()

absent_streaks = attendance[attendance['status'] == 'Absent'].groupby(['student_id', 'absence_group']).agg(
    absence_start_date=('attendance_date', 'min'),
    absence_end_date=('attendance_date', 'max'),
    total_absent_days=('attendance_date', 'count')
).reset_index(drop=True)

latest_absent_streaks = absent_streaks[absent_streaks['total_absent_days'] > 3].sort_values(by=['student_id', 'absence_start_date'], ascending=False).drop_duplicates(subset=['student_id'])

students_data = {
    'student_id': [1, 2],
    'student_name': ['Alice', 'Bob'],
    'parent_email': ['alice@example.com', 'bob@invalidemail']
}

students = pd.DataFrame(students_data)

final_output = latest_absent_streaks.merge(students, on='student_id', how='left')

def is_valid_email(email):
    if '@' in email:
        local_part, domain = email.split('@', 1)
        if domain == 'domain.com' and local_part and local_part[0].isalpha() and all(c.isalnum() or c == '_' for c in local_part):
            return True
    return False

final_output['email'] = final_output['parent_email'].apply(lambda x: x if is_valid_email(x) else None)
final_output['msg'] = final_output.apply(lambda x: f"Dear Parent, your child {x['student_name']} was absent from {x['absence_start_date'].date()} to {x['absence_end_date'].date()} for {x['total_absent_days']} days. Please ensure their attendance improves." if x['email'] else None, axis=1)

result = final_output[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]
print(result)