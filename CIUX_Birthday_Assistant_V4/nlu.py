
import calendar
import re

MONTHS = {
    m.lower(): i
    for i, m in enumerate(calendar.month_name)
    if m
}

PRONOUNS = {"his", "her", "their", "him", "them"}


def parse(message, people):
    text = message.lower().strip()
    result = {'intent': 'unknown', 'entities': {}}
    e = result['entities']

    if 'how many' in text or 'count' in text:
        result['intent'] = 'count_birthdays'
    elif any(word in text for word in ['where', 'stay', 'live']):
        result['intent'] = 'person_place'
    elif 'upcoming' in text:
        result['intent'] = 'upcoming_birthdays'
    else:
        result['intent'] = 'birthday_search'

    if re.search(r'\btomorrow\b', text):
        e['relative_date'] = 'tomorrow'

    if re.search(r'\bnext month\b', text):
        e['relative_month'] = 'next'

    for name, num in MONTHS.items():
        if re.search(r'\b' + name + r'\b', text):
            e['month'] = num
            break

    relationships = people['Relationship'].dropna().unique()

    for rel in sorted(relationships, key=len, reverse=True):
        token = str(rel).lower().strip()
        if token and re.search(r'\b' + re.escape(token) + r's?\b', text):
            e['relationship'] = rel
            break

    for _, r in people.iterrows():
        candidates = [str(r['Name']), str(r.get('Nickname', ''))]

        for candidate in candidates:
            candidate = candidate.lower().strip()

            if candidate and candidate != 'nan':
                if re.search(r'\b' + re.escape(candidate) + r'\b', text):
                    e['person_id'] = r['Person_ID']
                    e['person_name'] = r['Name']
                    break

        if 'person_id' in e:
            break

    for pronoun in PRONOUNS:
        if re.search(r'\b' + pronoun + r'\b', text):
            e['person_reference'] = pronoun
            break

    if 'person_reference' in e and 'person_id' not in e:
        e['needs_clarification'] = True

    return result
