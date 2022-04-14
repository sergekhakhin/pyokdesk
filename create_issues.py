from classes import Service, IssueTemplate

titles = list(['title1', 'title2'])
company_ids = list(['1', '2'])
assignee_id = str('6')
priority = str('low')
complete = bool(True)
services = list([Service('5118'), Service('5200')])
prefixes = list(['prefix1', 'prefix2'])
quantity = int()

params = {
    'assignee': assignee_id,
    'priority': priority
}


def add_prefixes_to_titles(prefixes: list, titles: list) -> list:
    titles_with_prefixes = []
    for prefix in prefixes:
        for title in titles:
            titles_with_prefixes.append(f'{prefix} | {title}')
    return titles_with_prefixes


def multiply_titles(titles: list, quantity: int) -> list:
    multiplied_titles = []
    for title in titles:
        for i in range(1, quantity + 1):
            multiplied_titles.append(f'{title} ({i}/{quantity})')
    return multiplied_titles


def make_issue_templates(titles: list, company_ids: list, **params) -> list:
    issue_templates = []
    if company_ids:
        for company_id in company_ids:
            params['company_id'] = company_id
            for title in titles:
                params['title'] = title
                issue_templates.append(IssueTemplate(**params))
    else:
        for title in titles:
            params['title'] = title
            issue_templates.append(IssueTemplate(**params))
    return issue_templates


def post_issue_templates(issue_templates: list) -> list:
    issues = []
    for issue_template in issue_templates:
        issues.append(issue_template.post())
    return issues


def add_services_to_issues(services: list, issues: list, performer_id: int = None) -> None:
    for issue in issues:
        for service in services:
            service.performer_id = performer_id
            issue.add_service(service)


def complete_issues(issues: list) -> None:
    for issue in issues:
        issue.complete()


def main():
    global titles
    if prefixes:
        titles = add_prefixes_to_titles(prefixes, titles)
    if quantity > 1:
        titles = multiply_titles(titles, quantity)
    issue_templates = make_issue_templates(titles, company_ids, **params)
    issues = post_issue_templates(issue_templates)
    if services:
        add_services_to_issues(services, issues)
    if complete:
        complete_issues(issues)


if __name__ == '__main__':
    main()
