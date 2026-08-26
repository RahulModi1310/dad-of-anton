"use client";

import { useEffect, useState } from "react";

export default function HealthCheck() {
  const [status, setStatus] = useState<string>("Checking...");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h2>Backend Health</h2>
      {error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : (
        <p>Status: {status}</p>
      )}
    </div>
  );
}