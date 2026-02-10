import React, { useEffect, useState } from "react";

type AnalyzeResult = {
  mean_score?: number;
  algorithm?: string;
  timestamp?: string;
  model_used?: string;
  input_data?: number[];
  next_prediction?: number;
  status?: string;
  [key: string]: any;
};

export default function Dashboard(): JSX.Element {
  const [data, setData] = useState<AnalyzeResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "";

  useEffect(() => {
    // Build URL safely
    const url =
      apiBase?.length > 0
        ? `${apiBase.replace(/\/$/, "")}/api/v1/analyze`
        : "/api/v1/analyze"; // fallback for local dev (proxy or local server)

    const controller = new AbortController();
    const signal = controller.signal;

    (async () => {
      try {
        const res = await fetch(url, { method: "GET", signal });
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`HTTP ${res.status}: ${text}`);
        }
        const json = await res.json();
        setData(json);
      } catch (e: any) {
        console.error("fetch error", e);
        setError(e?.message || "Unknown error");
      }
    })();

    return () => controller.abort();
  }, [apiBase]);

  return (
    <main style={{ padding: 20, fontFamily: "system-ui, Arial" }}>
      <h1>UMLFI Multi-Language Infrastructure</h1>
      <h2>Real-time Analysis</h2>

      {error ? (
        <div style={{ color: "crimson" }}>
          <strong>Error:</strong> {error}
        </div>
      ) : data ? (
        <pre style={{ whiteSpace: "pre-wrap", background: "#f7f7f7", padding: 12 }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      ) : (
        <div>Loading...</div>
      )}

      <footer style={{ marginTop: 20, fontSize: 12, color: "#666" }}>
        API base: <code>{apiBase || "not set (using /api/v1/analyze)"}</code>
      </footer>
    </main>
  );
}
