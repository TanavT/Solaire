from ui.views.rushH.gameViews.EldenRing import EldenRing


# used in cogs.rush
# bot will contain list of bosses and their data
def lookup_game_view(game_name: str, game_choices: list[str], players: list[str]):
    match game_name:
        case "Elden Ring":
            return EldenRing("Elden Ring Settings...", players)
        case "Hollow Knight":
            pass
        case "Super Mario 64":
            pass
