from lib.companies import find_company_id, get_company_info_by_id
from lib.employees import get_employee_id_by_ref
from lib.issues import create_issue, add_comment, add_service, change_issue_status

while True:
    template_title = str(input("[ INPUT ] Название заявки: "))
    if not template_title:
        print("[ ERROR ] Название заявки не может быть пустым!")
        continue
    else:
        break

while True:
    company_id = find_company_id(input("[ INPUT ] Организация: "))
    if not company_id:
        continue
    else:
        break

while True:
    employee_ref = input("[ INPUT ] Сотрудник: ")
    employee_id = get_employee_id_by_ref(employee_ref)
    if not employee_id:
        continue
    else:
        break

comment = input("[ INPUT ] Комментарий: ")
if not comment:
    print('[ INFO ] Комментарий не будет добавлен')

services = []
while True:
    try:
        service_id = input("[ INPUT ] ID спецификации (q для выхода): ")
        if service_id == 'q':
            break
        service_id = int(service_id)
        service_quantity = int(input("[ INPUT ] Количество (спецификация): "))
        service_tuple = (service_id, service_quantity)
        services.append(service_tuple)
    except ValueError:
        print("[ ERROR ] Некорректный ввод!")
        continue
if not services:
    print("[ INFO ] Спецификация не будет добавлена")

start_number = 0
end_number = 0
quantity = 0
while True:
    try:
        start_number = int(input("[ INPUT ] Начало нумерации: "))
        end_number = int(input("[ INPUT ] Конец нумерации: "))
        quantity = int(input("[ INPUT ] Количество создаваемых заявок: "))
        break
    except ValueError:
        print("[ ERROR ] Некорректный ввод!")
        continue

should_complete_issues = True
while True:
    user_input = str(input("[ INPUT ] Сменить статус на «Решено»? (Y/n): "))
    if not user_input:
        break
    else:
        user_input = user_input.lower().strip()[0]
    if user_input == 'y':
        break
    elif user_input == 'n':
        should_complete_issues = False
        break
    else:
        continue

input_params = f'''
[ INFO ] Название: {template_title}
[ INFO ] Организация: {get_company_info_by_id(company_id)['name']}
[ INFO ] Сотрудник: {employee_ref}
[ INFO ] Комментарий: {comment}
[ INFO ] Спецификации: {services}
[ INFO ] Начало нумерации: {start_number} 
[ INFO ] Конец нумерации: {end_number} 
[ INFO ] Количество создавааемых заявок: {quantity}
'''

print(input_params)
while True:
    user_input = str(input("Продолжить? (Y/n): "))
    if not user_input:
        break
    else:
        user_input = user_input.lower().strip()[0]
    if user_input == 'y':
        break
    elif user_input == 'n':
        exit()
    else:
        continue

created_issues = []
for i in range(start_number, quantity + start_number):
    title = f'{template_title} ({i}/{end_number})'
    payload = {
        'company_id': str(company_id),
        'assignee_id': str(employee_id),
        'author': {
            'id': str(employee_id),
            'type': 'employee'
        }
    }
    issue_id = create_issue(title, **payload)
    created_issues.append(issue_id)

if comment:
    for issue_id in created_issues:
        add_comment(issue_id, comment, employee_id, public=True)

if services:
    for issue_id in created_issues:
        for service in services:
            add_service(issue_id, service[0], service[1], employee_id)

if should_complete_issues:
    for issue_id in created_issues:
        change_issue_status(issue_id, 'completed')
