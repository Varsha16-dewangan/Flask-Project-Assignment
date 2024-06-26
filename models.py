class UserPreference:
    def __init__(self, preferences):
        self.preferences = preferences.split('.')


    def get_preferences(self):
        return [pref.strip().lower() for pref in self.preferences]
    
    