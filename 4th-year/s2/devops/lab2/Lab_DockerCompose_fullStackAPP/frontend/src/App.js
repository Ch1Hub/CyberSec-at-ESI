import { useEffect, useState } from "react";
import "./App.css";

const API_URL =  process.env.REACT_APP_BACKEND_URL;
console.log("Backend URL:", process.env.REACT_APP_BACKEND_URL);

console.log("API  URL:", API_URL);


function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchItems = async () => {
    const res = await fetch(`${API_URL}/items`);
    const data = await res.json();
    setItems(data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;

    setLoading(true);
    await fetch(`${API_URL}/items`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    setName("");
    setLoading(false);
    fetchItems();
  };

  return (
    <div className="container">
      <h1>📦 Items Manager</h1>

      <form className="item-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter item name..."
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add"}
        </button>
      </form>

      <ul className="item-list">
        {items.length === 0 && <p className="empty">No items yet.</p>}
        {items.map((item) => (
          <li key={item._id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
