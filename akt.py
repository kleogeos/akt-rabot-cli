#!/usr/bin/env python3
"""Generate an "Акт выполненных работ" (RU work-completion act, HTML) from a JSON file. Zero dependencies."""
import argparse
import html
import json
import sys

DISCLAIMER = (
    "Единой законодательно закреплённой формы акта выполненных работ не "
    "существует — это общий шаблон для фиксации факта оказания услуг между "
    "исполнителем и заказчиком. Для крупных или спорных сделок проверьте "
    "формулировки с юристом или бухгалтером."
)


def esc(s):
    return html.escape(str(s))


def fmt_money(v):
    return f"{v:,.2f}".replace(",", " ").replace(".", ",")


def render(data):
    executor = data["executor"]
    client = data["client"]
    act_num = data.get("act_num", "1")
    date = data["date"]
    city = data.get("city", "")
    contract = data.get("contract", "")
    items = data["items"]

    rows_html = []
    total = 0.0
    for i, item in enumerate(items, 1):
        qty = item.get("qty", 1)
        price = item["price"]
        amount = qty * price
        total += amount
        rows_html.append(
            f"<tr><td>{i}</td><td>{esc(item['name'])}</td><td>{esc(qty)}</td>"
            f"<td>{fmt_money(price)}</td><td>{fmt_money(amount)}</td></tr>"
        )
    rows = "\n".join(rows_html)

    contract_line = f"<p>К договору {esc(contract)}</p>" if contract else ""
    city_date = f"{esc(city)}" + (", " if city else "") + f"{esc(date)}"

    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Акт выполненных работ № {esc(act_num)}</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;max-width:760px;margin:40px auto;color:#1a1a1a;line-height:1.5}}
h1{{font-size:20px;text-align:center}}
table{{width:100%;border-collapse:collapse;margin-top:16px}}
th,td{{border:1px solid #999;padding:6px 8px;font-size:14px;text-align:left}}
th{{background:#f4f4f4}}
.total{{text-align:right;font-weight:bold;margin-top:10px}}
.meta{{display:flex;justify-content:space-between;color:#333;margin-top:8px}}
.disclaimer{{background:#fff8e6;border:1px solid #f0d58c;border-radius:6px;padding:12px 16px;font-size:13px;color:#664d03;margin-top:28px}}
.sig{{margin-top:40px;display:flex;gap:40px}}
.sig div{{flex:1;border-top:1px solid #999;padding-top:6px;font-size:13px;color:#666}}
@media print{{body{{margin:0}} .disclaimer{{background:none}}}}
</style></head><body>
<h1>Акт № {esc(act_num)} выполненных работ (оказанных услуг)</h1>
<p class="meta"><span>{city_date}</span></p>
{contract_line}
<p><b>Исполнитель:</b> {esc(executor)}</p>
<p><b>Заказчик:</b> {esc(client)}</p>

<table>
<thead><tr><th>№</th><th>Наименование работ (услуг)</th><th>Кол-во</th><th>Цена, ₽</th><th>Сумма, ₽</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p class="total">Итого: {fmt_money(total)} ₽</p>

<p>Исполнитель выполнил работы (оказал услуги) в полном объёме, в срок и с надлежащим
качеством. Заказчик принял результат работ (услуг) и не имеет претензий по объёму,
качеству и срокам выполнения работ (оказания услуг).</p>

<div class="sig">
<div>Исполнитель: ____________<br>{esc(executor)}</div>
<div>Заказчик: ____________<br>{esc(client)}</div>
</div>

<p class="disclaimer">{esc(DISCLAIMER)}</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="JSON act file (see example.json)")
    ap.add_argument("-o", "--output", help="output HTML file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    for required in ("executor", "client", "date", "items"):
        if required not in data:
            print(f"error: missing required field '{required}'", file=sys.stderr)
            sys.exit(1)
    if not data["items"]:
        print("error: 'items' must have at least one entry", file=sys.stderr)
        sys.exit(1)

    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
