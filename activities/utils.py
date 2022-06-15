from datetime import timedelta

def generate_stats(prefix, queryset):
    ''' Generates statistics based on queryset.
    '''
    stats = {}
    stats['{}_mileage'.format(prefix)] = sum([activity.get_total_distance() for activity in queryset])
    stats['{}_time'.format(prefix)] = sum([activity.duration() for activity in queryset], timedelta())

    return stats
