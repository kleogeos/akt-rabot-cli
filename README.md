# akt-rabot-cli

![Test CLI](https://github.com/kleogeos/akt-rabot-cli/actions/workflows/test.yml/badge.svg)

Generate a Russian "Акт выполненных работ" (work-completion act — the standard
RU document confirming a freelancer/contractor finished the agreed work) as a
print-ready HTML file, from a JSON file. No dependencies, no sign-up, just
Python 3.

```bash
python3 akt.py example.json -o akt.html
```

Produces a one-page act: executor/client details, itemized table of services
with quantities and prices, auto-calculated total, a standard acceptance
statement ("работы выполнены в полном объёме... заказчик не имеет претензий"),
and a signature block — ready to open in a browser, review, and print to PDF
or sign.

### Why this exists

Russian self-employed (самозанятые) and freelancers routinely need to close
out a project with a client-facing document that isn't the "Мой налог"
receipt — the acceptance act is what actually proves the work was delivered
and accepted, and it's the document most often asked for in a dispute. There
is no official single-form template (checked — none exists), but clients
expect something that looks like one.

### Install (optional)

```bash
pip install git+https://github.com/kleogeos/akt-rabot-cli
akt example.json -o akt.html
```

### JSON format

```json
{
  "executor": "Иванов Иван Иванович, ИНН 000000000000",
  "client": "ООО «Ромашка», ИНН 0000000000, ОГРН 0000000000000",
  "act_num": "1",
  "date": "15.10.2026",
  "city": "Москва",
  "contract": "№ 1 от 01.09.2026",
  "items": [
    {"name": "Разработка landing page", "qty": 1, "price": 45000},
    {"name": "Настройка аналитики", "qty": 1, "price": 8000}
  ]
}
```

Only `executor`, `client`, `date`, and `items` (at least one) are required.
`act_num`, `city`, and `contract` are optional.

### Is this legal advice?

No. There's no legally mandated single format for this act — this is a
general-purpose template covering what clients and accountants typically
expect: parties, itemized work, total, and an acceptance statement. For
high-value or disputed engagements, check the wording with a lawyer or
accountant. The generated document says so too, right above the signature
block.

### Where this fits

Same document as the [web generator](https://kleogeos.github.io/freelancer-tools/akt-vypolnennykh-rabot.html?src=cli-akt)
(same fields, runs entirely in-browser) — this CLI version is for anyone who'd
rather script it (batch-generate acts from a billing system export, pipe JSON
from another tool) than fill a form by hand.

[akt-rabot-js](https://github.com/kleogeos/akt-rabot-js) — same output, `npx` instead of `pip`, no install.

Part of the same family as
[usdt-rub-cli](https://github.com/kleogeos/usdt-rub-cli) and the RU
freelancer guides on the [Freelancer Toolbox](https://kleogeos.github.io/freelancer-tools/ru-kit.html?src=cli-akt) —
including the [акт-выполненных-работ explainer](https://kleogeos.github.io/freelancer-tools/akt-vypolnennykh-rabot.html?src=cli-akt-howto)
on why this document matters separately from the НПД receipt.

## Tests

```bash
python3 test_akt.py
```
