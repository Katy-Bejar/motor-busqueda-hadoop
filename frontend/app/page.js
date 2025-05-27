'use client';
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Ingresa un término de búsqueda');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const response = await axios.get(`http://localhost:5000/search?q=${query}`);
      setResults(response.data);
    } catch (err) {
      setError('Error al buscar. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">🔍 Buscador</h1>

      {/* Barra de búsqueda */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ej: persona, auto..."
          className="flex-1 p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className={`px-5 py-3 font-semibold rounded-lg text-white ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {loading ? 'Buscando...' : 'Buscar'}
        </button>
      </div>

      {/* Mensajes de error */}
      {error && <p className="text-red-600 text-center mb-4">{error}</p>}

      {/* Resultados */}
      <div className="bg-gray-100 rounded-lg p-4 space-y-4">
        {results.length > 0 ? (
          results.map((result, index) => (
            <div
              key={index}
              className="bg-white p-4 rounded-lg shadow hover:shadow-md transition"
            >
              <span className="block text-lg font-bold text-gray-800">{result.camera_id}</span>
              <p className="text-gray-700 mt-1">📍 {result.location}</p>
              <p className="text-gray-500 text-sm">📅 {result.date}</p>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500">No hay resultados.</p>
        )}
      </div>
    </div>
  );
}
