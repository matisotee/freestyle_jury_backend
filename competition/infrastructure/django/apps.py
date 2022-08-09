from django.apps import AppConfig


class CompetitionConfig(AppConfig):
    name = 'competition'

    def ready(self):
        from competition.application import competition_creator
        from competition.infrastructure.django.dependency_injection import Container
        INJECTED_MODULES = [competition_creator]
        container = Container()
        container.wire(modules=INJECTED_MODULES)
