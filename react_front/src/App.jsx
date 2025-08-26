import { useState, useEffect } from "react";

function App() {
  const [posts, setPosts] = useState([]);

  const fetchPosts = async () => {
    const res = await fetch("/api/posts");
    const data = await res.json();
    setPosts(data);
  };

  const handleCreate = async () => {
    const content = prompt("내용을 입력하세요");
    if (!content) return;
    await fetch("/api/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    fetchPosts();
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  return (
    <div style={{ maxWidth: "600px", margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>📋 게시판</h1>
      <button onClick={handleCreate}>➕ 새 글</button>
      <ul>
        {posts.map((p) => (
          <li key={p.id}>
            <p>{p.content}</p>
            <small>{new Date(p.created_at).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
