
class LevelSystem:
    LEVELS = [
        (0, "Aprendiz Poupador", 500),         # 0 to 500
        (1, "Organizador Consciente", 2000),   # 501 to 2000
        (2, "Guardião das Finanças", 5000),    # 2001 to 5000
        (3, "Mestre da Economia", 10000),      # 5001 to 10000
        (4, "Magnata", 1000000)                # 10000+
    ]
    
    @staticmethod
    def calculate_stats(balance):
        # Default if negative or 0
        current_xp = max(0, balance)
        
        # Find Level
        # Logic: Find the first level where balance < goal
        
        selected_lvl_idx = 0
        goal = 500
        title = "Aprendiz Poupador"
        prev_goal = 0
        
        for i, (idx, name, limit) in enumerate(LevelSystem.LEVELS):
            if current_xp < limit:
                selected_lvl_idx = idx + 1 # Display as Level 1, 2, 3...
                title = name
                goal = limit
                prev_goal = LevelSystem.LEVELS[i-1][2] if i > 0 else 0
                break
            else:
                # If we passed the last one, we are at max level
                if i == len(LevelSystem.LEVELS) - 1:
                    selected_lvl_idx = idx + 1
                    title = name
                    goal = limit * 10 # Infinite scaling visually
                    prev_goal = limit
        
        # Calculate Progress (0.0 to 1.0) for the current bar
        # Progress within the CURRENT level range, not total
        range_span = goal - prev_goal
        current_progress = current_xp - prev_goal
        
        percent = 0.0
        if range_span > 0:
            percent = current_progress / range_span
            
        percent = max(0.0, min(1.0, percent))
        
        return {
            "level": selected_lvl_idx,
            "title": title,
            "goal": goal,
            "percent": percent,
            "current": current_xp
        }
