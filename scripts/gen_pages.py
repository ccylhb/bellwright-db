# -*- coding: utf-8 -*-
"""Generate BellwrightDB list + detail pages (token substitution, no str.format)."""
import os

BASE = "src/pages"

LIST_TPL = '''---
import Base from "../../layouts/Base.astro";
import DataTable from "../../components/DataTable.astro";
import Related from "../../components/Related.astro";
import @VAR@ from "../../data/bellwright_@BOARD@.json";

const n = (v) => {
  const m = String(v ?? "").match(/-?\\d+(?:\\.\\d+)?/);
  return m ? parseFloat(m[0]) : "";
};
const rows = @VAR@
  .map((x) => ({
    name: `<a href="/@BOARD@/${x.slug}/">${x.title}</a>${x.icon_file ? ` <img src="/icons/${x.icon_file}" alt="" width="22" height="22" style="vertical-align:middle" loading="lazy" />` : ""}`,
    _sort: x.title.toLowerCase(),
@ROWFIELDS@
  }))
  .sort((a, b) => a._sort.localeCompare(b._sort));
---
<Base
  title="@TITLE@ — ${@VAR@.length} entries with exact values"
  description="@DESC@ for ${@VAR@.length} Bellwright @LABELLOW@."
>
  <h1>@LABEL@</h1>
  <p class="muted">${@VAR@.length} entries · click a column to sort.</p>
  <DataTable
    id="@BOARD@"
    rows={rows}
    searchPlaceholder="Search @LABELLOW@..."
    columns={[
@COLUMNS@
    ]}
  />
  <Related
    links={[
@RELATED@
    ]}
  />
</Base>
'''

DETAIL_TPL = '''---
import Base from "../../layouts/Base.astro";
import Related from "../../components/Related.astro";
import EntryStats from "../../components/EntryStats.astro";
import @VAR@ from "../../data/bellwright_@BOARD@.json";

export function getStaticPaths() {
  return @VAR@.map((x) => ({ params: { slug: x.slug }, props: { x } }));
}

const { x } = Astro.props;
const f = x.fields || {};
const similar = @VAR@
  .filter((o) => o.slug !== x.slug && (o.fields?.categ || o.fields?.category || "") === (f.categ || f.category || ""))
  .slice(0, 6);
---
<Base
  title={`${x.title} — Bellwright @BOARD@ stats`}
  description={`${x.title}: Bellwright @BOARD@ values — exact stats from the wiki infobox.`}
>
  <h1 class="icon-h1">
    {x.icon_file ? <img src={`/icons/${x.icon_file}`} alt={x.title} loading="eager" /> : null}
    <span>{x.title}</span>
  </h1>
  {x.intro && <p>{x.intro}</p>}
  <EntryStats entry={x} keys={@DKEYS@} labels={@DLABELS@} />
  <Related
    links={[
      ...similar.map((s) => ({
        href: `/@BOARD@/${s.slug}/`,
        title: s.title,
        icon: s.icon_file ? `/icons/${s.icon_file}` : undefined,
      })),
      { href: "/@BOARD@/", title: "All @LABEL@", sub: "Sortable table" },
      { href: "/rankings/", title: "Rankings", sub: "Best picks" },
    ]}
  />
</Base>
'''

boards = {
    "armor": {
        "varname": "armor",
        "label": "Armor & Clothing",
        "desc": "armor ratings, speed penalties and slots",
        "row_fields": '''    slot: (x.fields?.slot || "").slice(0, 16),
    armor: n(x.fields?.armor),
    speed: (x.fields?.speed || "").slice(0, 12),
    categ: (x.fields?.categ || "").slice(0, 18),''',
        "columns": '''      { key: "name", label: "Piece" },
      { key: "slot", label: "Slot" },
      { key: "armor", label: "Armor", type: "number" },
      { key: "speed", label: "Speed" },
      { key: "categ", label: "Category" },''',
        "dkeys": '["armor", "speed", "slot", "categ", "requs"]',
        "dlabels": '{ armor: "Armor", speed: "Speed", slot: "Slot", categ: "Category", requs: "Required skill level" }',
    },
    "weapons": {
        "varname": "weapons",
        "label": "Weapons",
        "desc": "cutting and pierce damage, speed and reach",
        "row_fields": '''    cutti: n(x.fields?.cutti),
    mpier: n(x.fields?.mpier),
    speed: n(x.fields?.speed),
    lengt: n(x.fields?.lengt),
    hand: (x.fields?.hand || "").slice(0, 8),
    categ: (x.fields?.categ || "").slice(0, 16),''',
        "columns": '''      { key: "name", label: "Weapon" },
      { key: "cutti", label: "Cutting", type: "number" },
      { key: "mpier", label: "Pierce", type: "number" },
      { key: "speed", label: "Speed", type: "number" },
      { key: "lengt", label: "Length", type: "number" },
      { key: "hand", label: "Hand" },
      { key: "categ", label: "Category" },''',
        "dkeys": '["cutti", "mpier", "speed", "lengt", "hand", "categ", "requs"]',
        "dlabels": '{ cutti: "Cutting damage", mpier: "Pierce damage", speed: "Speed", lengt: "Length", hand: "Hand", categ: "Category", requs: "Required skill level" }',
    },
    "food": {
        "varname": "food",
        "label": "Food",
        "desc": "health, stamina and satiation values",
        "row_fields": '''    health: (x.fields?.health || "").slice(0, 10),
    stamina: (x.fields?.stamina || "").slice(0, 10),
    satiating: (x.fields?.satiating || "").slice(0, 10),
    regen: (x.fields?.regen_heath || "").slice(0, 10),
    category: (x.fields?.category || "").slice(0, 14),''',
        "columns": '''      { key: "name", label: "Food" },
      { key: "health", label: "Health" },
      { key: "stamina", label: "Stamina" },
      { key: "satiating", label: "Satiating" },
      { key: "regen", label: "HP regen" },
      { key: "category", label: "Category" },''',
        "dkeys": '["health", "regen_heath", "stamina", "regen_stamina", "satiating", "skill_exp", "category"]',
        "dlabels": '{ health: "Health", regen_heath: "HP regen", stamina: "Stamina", regen_stamina: "Stamina regen", satiating: "Satiating", skill_exp: "Skill EXP", category: "Category" }',
    },
    "tools": {
        "varname": "tools",
        "label": "Tools & Resources",
        "desc": "tools, resources and seeds",
        "row_fields": '''    category: (x.fields?.category || x.fields?.categ || "").slice(0, 16),''',
        "columns": '''      { key: "name", label: "Item" },
      { key: "category", label: "Category" },''',
        "dkeys": '["category", "categ"]',
        "dlabels": '{ category: "Category", categ: "Category" }',
    },
}

related_map = {
    "armor": '''      { href: "/loadout-builder/", title: "Loadout Builder", sub: "Build your armor set", tool: true },
      { href: "/weapons/", title: "Weapons", sub: "Damage values" },
      { href: "/rankings/", title: "Rankings", sub: "Best picks" },''',
    "weapons": '''      { href: "/armor/", title: "Armor", sub: "Armor values" },
      { href: "/rankings/", title: "Rankings", sub: "Best weapons" },
      { href: "/loadout-builder/", title: "Loadout Builder", sub: "Build your set", tool: true },''',
    "food": '''      { href: "/rankings/", title: "Rankings", sub: "Best food" },
      { href: "/armor/", title: "Armor", sub: "Armor values" },
      { href: "/tools/", title: "Tools & Resources", sub: "Gathering gear" },''',
    "tools": '''      { href: "/food/", title: "Food", sub: "Health & stamina" },
      { href: "/weapons/", title: "Weapons", sub: "Damage values" },
      { href: "/rankings/", title: "Rankings", sub: "Best picks" },''',
}


def fill(tpl, mapping):
    for k, v in mapping.items():
        tpl = tpl.replace(k, v)
    return tpl


for board, cfg in boards.items():
    mapping = {
        "@BOARD@": board,
        "@VAR@": cfg["varname"],
        "@TITLE@": "Bellwright " + cfg["label"],
        "@DESC@": cfg["desc"],
        "@LABEL@": cfg["label"],
        "@LABELLOW@": cfg["label"].lower(),
        "@ROWFIELDS@": cfg["row_fields"],
        "@COLUMNS@": cfg["columns"],
        "@RELATED@": related_map[board],
        "@DKEYS@": cfg["dkeys"],
        "@DLABELS@": cfg["dlabels"],
    }
    os.makedirs(f"{BASE}/{board}", exist_ok=True)
    open(f"{BASE}/{board}/index.astro", "w", encoding="utf-8").write(fill(LIST_TPL, mapping))
    open(f"{BASE}/{board}/[slug].astro", "w", encoding="utf-8").write(fill(DETAIL_TPL, mapping))

print("generated:", os.listdir(BASE))
