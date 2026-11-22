
from datetime import date, timedelta


def format_rows(rows):
    if rows.empty:
        return "No matching people found."

    return "\n".join(
        f"{r.Name} - {r.DOB.strftime('%d %B')} ({r.Relationship})"
        for _, r in rows.iterrows()
    )


def execute(parsed, df):
    intent = parsed['intent']
    e = parsed['entities']
    today = date.today()

    if e.get('needs_clarification'):
        return "I am not sure which person you mean. Could you please specify their name?"

    if e.get('person_reference') and 'person_id' not in e:
        return "Whose birthday are you asking about? Please specify the person's name."

    if 'person_id' in e:
        matches = df[df.Person_ID == e['person_id']]

        if matches.empty:
            return "I couldn't find that person in the dataset."

        r = matches.iloc[0]

        if intent == 'person_place':
            return f"{r.Name} stays in {r.Place_of_Stay}."

        return f"{r.Name}'s birthday is {r.DOB.strftime('%d %B %Y')}."

    work = df.copy()

    if 'relationship' in e:
        work = work[
            work.Relationship.str.lower() == e['relationship'].lower()
        ]

    if e.get('relative_date') == 'tomorrow':
        t = today + timedelta(days=1)
        work = work[
            (work.DOB.dt.month == t.month) &
            (work.DOB.dt.day == t.day)
        ]

    month = e.get('month')

    if e.get('relative_month') == 'next':
        month = 1 if today.month == 12 else today.month + 1

    if month:
        work = work[work.DOB.dt.month == month]

    if intent == 'count_birthdays':
        return f"I found {len(work)} matching birthdays."

    if intent == 'upcoming_birthdays':
        def days(r):
            cand = date(today.year, r.DOB.month, r.DOB.day)

            if cand < today:
                cand = date(today.year + 1, r.DOB.month, r.DOB.day)

            return (cand - today).days

        work = work.assign(_days=work.apply(days, axis=1))
        work = work[
            (work._days >= 0) & (work._days <= 30)
        ].sort_values('_days')

    if intent == 'birthday_search' and not any(
        key in e for key in (
            'relationship', 'month', 'relative_date', 'relative_month'
        )
    ):
        return "Whose birthday would you like to know? Please provide a name or relationship."

    return format_rows(work)
