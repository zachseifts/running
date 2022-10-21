from datetime import timedelta

from django import template
from django.utils.timezone import now
from django.urls import reverse

from activities.models import Shoe

register = template.Library()

@register.inclusion_tag('tags/base_navbar.html')
def base_navbar(user):
    ''' Generates the navigation bar for users.
    '''
    year, week, _ = now().isocalendar()
    this_week = reverse('activity-weekly', kwargs={'year': year, 'week': week})

    last_week_date = now() - timedelta(weeks = 1)
    last_week = reverse('activity-weekly', kwargs={'year': year, 'week': last_week_date.isocalendar().week})

    this_year = reverse('activity-yearly', kwargs={'year': year})
    return {
        'user': user,
        'this_week': this_week,
        'last_week': last_week,
        'this_year': this_year,
    }

@register.inclusion_tag('tags/active_shoes.html')
def active_shoes(user):
    ''' Generates a list of active shoes'
    '''
    shoes = Shoe.objects.filter(creator=user).filter(is_active=True)
    return {'shoes': shoes}

@register.inclusion_tag('tags/activity_table.html')
def activity_table(activities):
    ''' Generates a table that lists activities.
    '''
    return {'activities': activities}
