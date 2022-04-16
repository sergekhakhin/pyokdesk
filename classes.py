import api.issues


class Service:
    def __init__(self, code: str, quantity=1.00, **kwargs):
        self.code = code
        self.quantity = quantity
        self.__dict__.update(kwargs)


class Issue:
    def __repr__(self):
        return f'issue_{self.id}'

    def __init__(self, issue_id: int):
        self.id = issue_id
        try:
            self.sync()
        except TypeError:
            print(f'[ ERROR ] Заявка {self.id} не существует')
            del self

    def sync(self):
        self.__dict__.update(api.issues.get_issue_info(self.id))

    def get_comments(self):
        return api.issues.get_issue_comments(self.id)

    def get_services(self):
        return api.issues.get_issue_services(self.id)

    def open(self):
        api.issues.change_issue_status(self.id, 'opened')
        self.sync()

    def complete(self):
        api.issues.change_issue_status(self.id, 'completed')
        self.sync()

    def change_assignee(self, assignee_id=None, group_id=None):
        api.issues.change_assignee(self.id, assignee_id, group_id)
        self.sync()

    def add_comment(self, content: str, author_id=None, public=False):
        api.issues.add_comment(self.id, content, author_id, public)
        self.sync()

    def add_service(self, service: Service, performer_id: int = None):
        service.performer_id = performer_id
        if not performer_id:
            try:
                service.performer_id = self.assignee['id']
            except TypeError:
                pass
        api.issues.add_service(self.id, **vars(service))

    def delete(self):
        api.issues.delete_issue(self.id)
        del self


class IssueTemplate:
    def __init__(self, **params) -> None:
        self.__dict__.update(params)

    def post(self) -> Issue:
        issue_id = api.issues.create_issue(**vars(self))
        return Issue(issue_id)


class IssueGroup:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def get_issue_template(self) -> IssueTemplate:
        static_params = ['assignee_id', 'priority']
        issue_template = IssueTemplate()
        for k, v in vars(self).items():
            if k in static_params:
                setattr(issue_template, k, v)
        return issue_template
