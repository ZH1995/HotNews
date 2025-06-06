from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """获取字典中的项目"""
    return dictionary.get(key)