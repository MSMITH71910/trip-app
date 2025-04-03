from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get value from a dictionary by key"""
    return dictionary.get(key, 0)

@register.filter
def filter_by_reaction(reactions, reaction_type):
    """Filter reactions by reaction type"""
    return reactions.filter(reaction_type=reaction_type).count()