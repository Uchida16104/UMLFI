import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LumOS - Universal Polyglot OS",
  description: "Next-generation web desktop environment based on Lumos Language",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <head>
        <script src="https://unpkg.com/htmx.org@1.9.10" defer></script>
        <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
        <script src="https://unpkg.com/hyperscript.org@0.9.12" defer></script>
      </head>
      <body className="bg-black antialiased overflow-hidden">
        {children}
      </body>
    </html>
  );
}
