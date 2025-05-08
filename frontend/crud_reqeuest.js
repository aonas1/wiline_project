// App.js
import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:8000"; // Backend URL

export default function App() {
  const [users, setUsers] = useState([]);
  const [query, setQuery] = useState("");

  // Fetch users from the API
  const fetchUsers = async () => {
    const res = await fetch(`${API_URL}/users?query=${query}`);
    const data = await res.json();
    setUsers(data);
  };

  // Fetch on load
  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>User Directory</h2>
      <input
        placeholder="Search by name"
        value={query}
        onChange={e => setQuery(e.target.value)}
        onBlur={fetchUsers}
      />
      <ul>
        {users.map(user => (
          <li key={user._id}>
            <strong>{user.firstName} {user.lastName}</strong> — {user.email} {user.phoneNumber && `| 📞 ${user.phoneNumber}`}
          </li>
        ))}
      </ul>
    </div>
  );
}
