def apply_competition_injections():
    from competition.application import competition_creator
    from competition.infrastructure.dependency_injection.container import container
    container.wire(modules=[competition_creator])
