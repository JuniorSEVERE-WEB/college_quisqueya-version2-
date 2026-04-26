import { BASE_URL } from "../api";

export function getMediaUrl(fileUrl) {
  if (!fileUrl) return "";
  if (/^https?:\/\//i.test(fileUrl)) return fileUrl;

  const root = (BASE_URL || "").replace(/\/api\/?$/, "").replace(/\/$/, "");
  const path = fileUrl.startsWith("/") ? fileUrl : `/${fileUrl}`;

  return `${root}${path}`;
}
