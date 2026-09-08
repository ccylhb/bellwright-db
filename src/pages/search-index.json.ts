import armor from "../data/bellwright_armor.json";
import weapons from "../data/bellwright_weapons.json";
import food from "../data/bellwright_food.json";
import tools from "../data/bellwright_tools.json";

export function GET() {
  const entries = [
    ...armor.map((x) => ({
      title: x.title,
      href: `/armor/${x.slug}/`,
      sub: `Armor · ${x.fields?.armor || "?"} armor · ${x.fields?.slot || "?"}`,
      icon: x.icon_file || "",
    })),
    ...weapons.map((x) => ({
      title: x.title,
      href: `/weapons/${x.slug}/`,
      sub: `Weapon · ${x.fields?.cutti || "?"} cut / ${x.fields?.mpier || "?"} pierce`,
      icon: x.icon_file || "",
    })),
    ...food.map((x) => ({
      title: x.title,
      href: `/food/${x.slug}/`,
      sub: `Food · ${x.fields?.health || "?"} health · ${x.fields?.stamina || "?"} stamina`,
      icon: x.icon_file || "",
    })),
    ...tools.map((x) => ({
      title: x.title,
      href: `/tools/${x.slug}/`,
      sub: `Tool · ${x.fields?.category || x.fields?.categ || ""}`,
      icon: x.icon_file || "",
    })),
  ].sort((a, b) => a.title.localeCompare(b.title));
  return new Response(JSON.stringify(entries), {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}
