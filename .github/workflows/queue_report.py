"""מתאר את תור ההגשות ל-issue שפותחת פעולת "תור ההגשות".

רץ גם על הרץ של גיטהאב וגם מקומית, ולכן אפשר לבדוק אותו לפני שהוא מגיע לענן:

    python3 .github/workflows/queue_report.py data/pending.json body.md

מדפיס שתי שורות ל-GITHUB_OUTPUT אם הוא מוגדר, ותמיד את הכותרת לפלט הרגיל.
"""
import json
import os
import sys

APP = 'https://orimosenzon.github.io/fun/vibe_coding/dereh_kitzur/'


def title_for(n):
    if n == 1:
        return 'הגשה אחת ממתינה בתור'
    return f'{n} הגשות ממתינות בתור'


def describe(item):
    kind = 'טיול משורשר' if item.get('parts') else 'שביל'
    by = item.get('by') or 'לא נמסר שם'
    note = (item.get('note') or '').strip()
    lines = [
        f"### {item.get('name') or 'בלי שם'}",
        '',
        f"- אורך: {item.get('length', '?')} מ׳",
        f"- נשלח: {(item.get('submitted') or '')[:10]}",
        f'- מאת: {by}',
        f'- סוג: {kind}',
        '',
        # ההערה של השולח היא לרוב הדבר הכי שימושי בהגשה: מצב הקרקע, גדר
        # שנסגרה, אם אפשר לעבור שם עם עגלה. היא מוצגת כציטוט ובלשונו.
        f'> {note}' if note else '_בלי הערה._',
        '',
    ]
    if item.get('photos'):
        lines.insert(6, f"- תמונות: {len(item['photos'])}")
    return lines


def body_for(items):
    out = ['יש בתור מה שעוד לא עלה למפה.', '']
    for item in items:
        out += describe(item)
    out += [
        '---',
        '',
        f'לאישור: לפתוח את [האפליקציה]({APP}) עם עריכה דלוקה. שכבת "ממתינים לאישור"',
        'מראה את ההגשות על המפה, ובלחיצה על אחת יש כפתור אישור וכפתור דחייה.',
        '',
        'ה-issue הזה נסגר מעצמו ברגע שהתור מתרוקן.',
    ]
    return '\n'.join(out) + '\n'


def main():
    src, dest = sys.argv[1], sys.argv[2]
    try:
        with open(src, encoding='utf-8') as fh:
            items = (json.load(fh) or {}).get('items') or []
    except FileNotFoundError:
        # אין קובץ תור זו בדיוק המשמעות של תור ריק, ולא תקלה.
        items = []

    if items:
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write(body_for(items))

    out = os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out, 'a', encoding='utf-8') as fh:
            fh.write(f'count={len(items)}\n')
            fh.write(f'title={title_for(len(items))}\n')
    print(f'בתור: {len(items)}')


if __name__ == '__main__':
    main()
