from src.core.action import Action

def run_action(action: Action) -> bool:
    return action.run()
