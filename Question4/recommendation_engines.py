class RecommendationEngine:
    def __init__(self, content):
        self.content = content
    
    def recommend(self, user_preferences):
        recommendations = []
        for item in self.content:
            for pref in user_preferences.get_preferences():
                if pref in item.lower():
                    recommendations.append(item)
                    break
        return recommendations
