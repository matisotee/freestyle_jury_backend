from pubsub import pub

from phase.application.update_competition import CompetitionUpdater


def update_competition(competition):
    service = CompetitionUpdater()
    service.update_competition(competition['id'], competition['status'])


def init_phase_subscribers():
    pub.subscribe(update_competition, 'competitionUpdated')
