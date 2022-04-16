from copy import deepcopy
from classes import Service, IssueGroup, IssueTemplate, Issue


def create_issue_templates_with_titles(issue_templates: list[IssueTemplate], titles: list[str]) -> list[IssueTemplate]:
    issue_templates_with_titles = []
    for issue_template in issue_templates:
        for title in titles:
            new_issue_template = deepcopy(issue_template)
            new_issue_template.title = title
            issue_templates_with_titles.append(new_issue_template)
    return issue_templates_with_titles


def create_issue_templates_with_company_ids(issue_templates: list[IssueTemplate], companies_ids: list[int]) -> list[IssueTemplate]:
    issue_templates_with_company_ids = []
    for company_id in companies_ids:
        for issue_template in issue_templates:
            new_issue_template = deepcopy(issue_template)
            new_issue_template.company_id = company_id
            issue_templates_with_company_ids.append(new_issue_template)
    return issue_templates_with_company_ids


def create_issue_templates_with_prefixes(issue_templates: list[IssueTemplate], prefixes: list[IssueTemplate]) -> list[IssueTemplate]:
    issue_templates_with_prefixes = []
    for prefix in prefixes:
        for issue_template in issue_templates:
            new_issue_template = deepcopy(issue_template)
            new_title = f'{prefix} | {new_issue_template.title}'
            new_issue_template.title = new_title
            issue_templates_with_prefixes.append(new_issue_template)
    return issue_templates_with_prefixes


def create_issue_templates_with_sequential_numbers(issue_templates: list[IssueTemplate], quantity: int) -> list[IssueTemplate]:
    issue_templates_with_sequential_numbers = []
    for issue_template in issue_templates:
        for i in range(1, quantity + 1):
            new_issue_template = deepcopy(issue_template)
            new_title = f'{new_issue_template.title} ({i}/{quantity})'
            new_issue_template.title = new_title
            issue_templates_with_sequential_numbers.append(new_issue_template)
    return issue_templates_with_sequential_numbers


def post_issue_templates(issue_templates: list[IssueTemplate]) -> list[Issue]:
    issues = []
    for issue_template in issue_templates:
        issues.append(issue_template.post())
    return issues


def add_services_to_issues(issues: list[Issue], services: list[Service], performer_id: int = None) -> None:
    for issue in issues:
        for service in services:
            service.performer_id = performer_id
            issue.add_service(service)


def complete_issues(issues: list[Issue]) -> None:
    for issue in issues:
        issue.complete()


def create_issue_group(issue_group: IssueGroup):
    issue_templates = [issue_group.get_issue_template()]
    issue_templates = create_issue_templates_with_titles(
        issue_templates, issue_group.titles)
    if issue_group.prefixes:
        issue_templates = create_issue_templates_with_prefixes(
            issue_templates, issue_group.prefixes)
    if issue_group.quantity > 1:
        issue_templates = create_issue_templates_with_sequential_numbers(
            issue_templates, issue_group.quantity)
    if issue_group.company_ids:
        issue_templates = create_issue_templates_with_company_ids(
            issue_templates, issue_group.company_ids)

    issues = post_issue_templates(issue_templates)
    if issue_group.services:
        add_services_to_issues(issues, issue_group.services)
    if issue_group.complete:
        complete_issues(issues)
