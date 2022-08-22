def apply_phase_injections():
    from phase.application import update_competition
    from phase.infra.dependency_injection.container import container
    container.wire(modules=[update_competition])
