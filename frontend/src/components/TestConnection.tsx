import { useState } from 'react';

export function TestConnection() {
  const [response, setResponse] = useState<{ message: string; timestamp: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const testConnection = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/test-connection');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rounded-lg border p-4 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold">Backend Connection Test</h2>
      <button
        onClick={testConnection}
        disabled={isLoading}
        className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:bg-blue-300"
      >
        {isLoading ? 'Testing...' : 'Test Connection'}
      </button>

      {error && <div className="mt-4 rounded bg-red-100 p-3 text-red-700">Error: {error}</div>}

      {response && (
        <div className="mt-4 rounded bg-green-100 p-3 text-green-700">
          <p>Message: {response.message}</p>
          <p>Timestamp: {response.timestamp}</p>
        </div>
      )}
    </div>
  );
}
