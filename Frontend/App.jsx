
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './App.css';

const COLORS = ['#2ecc71', '#95a5a6', '#e74c3c']; 

function App() {
  // We use state to hold our data and track if it's currently loading
  const [sentimentData, setSentimentData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // useEffect runs once when the component first mounts
  useEffect(() => {
    // Call our Python Flask API
    fetch('http://localhost:5000/api/sentiment-data')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch data from the server');
        }
        return response.json();
      })
      .then(data => {
        setSentimentData(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Error fetching data:", err);
        setError(err.message);
        setIsLoading(false);
      });
  }, []); // The empty array [] means this only runs once on load

  if (isLoading) {
    return <h2 style={{ textAlign: 'center', marginTop: '50px' }}>Loading Dashboard Data...</h2>;
  }

  if (error) {
    return <h2 style={{ textAlign: 'center', color: 'red', marginTop: '50px' }}>Error: {error}</h2>;
  }

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>AI Sentiment Analysis Dashboard</h1>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '40px' }}>
        Live analysis powered by Python, Flask, and the Gemini API.
      </p>

      <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}>
        
        {/* Bar Chart */}
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)', width: '45%', minWidth: '400px', marginBottom: '20px' }}>
          <h3 style={{ textAlign: 'center', color: '#444' }}>Sentiment Volume</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sentimentData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip cursor={{fill: 'transparent'}} />
              <Legend />
              <Bar dataKey="count" fill="#3498db" radius={[4, 4, 0, 0]}>
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart */}
        <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)', width: '45%', minWidth: '400px', marginBottom: '20px' }}>
          <h3 style={{ textAlign: 'center', color: '#444' }}>Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
}

export default App;
