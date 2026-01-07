waiting_matches: dict[str, dict] = {} 
matches: dict[str, dict] = {} 
ia_matches: dict[str, dict] = {} 
# id -> json do match

users = {}      # username -> { password }
sessions = {}   # token -> { user, exp }