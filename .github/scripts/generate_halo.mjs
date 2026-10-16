import { writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { svg } from "ascii.rest/svg";
import { dissolve } from "ascii.rest/pieces";

const __dirname = dirname(fileURLToPath(import.meta.url));
const assetsDir = resolve(__dirname, "../assets");
mkdirSync(assetsDir, { recursive: true });

const words = ["HALO", "HELLO"];
const seconds = words.length * 4.2; // 1.6s hold + 2.6s transition per word

const darkSvg = svg(dissolve, {
  dark: true,
  seconds,
  options: { words },
});

const lightSvg = svg(dissolve, {
  seconds,
  options: { words },
});

writeFileSync(resolve(assetsDir, "halo-dark.svg"), darkSvg);
writeFileSync(resolve(assetsDir, "halo-light.svg"), lightSvg);
console.log("Generated halo-dark.svg and halo-light.svg successfully.");
