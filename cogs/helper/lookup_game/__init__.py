from ui.views.rushH.gameViews.EldenRing import EldenRing


# used in cogs.rush
# bot will contain list of bosses and their data
def lookup_game_view(game_name: str, game_choices: list[str], players: list[str]):
    match game_name:
        case "Elden Ring":
            return EldenRing("| Elden Ring Settings... (Only bosses currently implemented)", players)
        case "Hollow Knight":
            pass
        case "Super Mario Odyssey":
            pass
