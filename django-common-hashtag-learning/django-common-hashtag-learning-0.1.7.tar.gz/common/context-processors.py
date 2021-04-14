from datetime import datetime

def get_current_year(request):

    current_year = datetime.today().year

    return {
        'current_year': current_year,
    }
