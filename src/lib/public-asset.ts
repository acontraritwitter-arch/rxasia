import { statSync } from "node:fs";
import path from "node:path";

/** Public file URL with `?v=` from mtime so replaced assets bypass browser cache. */
export function publicMediaUrl(relativePath: string): string {
  const normalized = relativePath.replace(/^\//, "");
  const filePath = path.join(process.cwd(), "public", normalized);

  try {
    const { mtimeMs } = statSync(filePath);
    return `/${normalized}?v=${Math.floor(mtimeMs)}`;
  } catch {
    return `/${normalized}`;
  }
}
