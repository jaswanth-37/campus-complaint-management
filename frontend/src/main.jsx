import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [view, setView] = useState("home");
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [user, setUser] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [auth, setAuth] = useState({ email: "", password: "", name: "", student_id: "", department: "" });
  const [form, setForm] = useState({ title: "", description: "", category: "Infrastructure", department: "General", priority: "medium" });
  const [message, setMessage] = useState("");

  async function api(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (token) headers.Authorization = `Bearer ${token}`;
    const response = await fetch(API + path, { ...options, headers });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed");
    return data;
  }
  async function loadMe() { if (!token) return; try { setUser(await api("/api/auth/me")); } catch { logout(); } }
  async function loadComplaints() { try { setComplaints(await api("/api/complaints")); } catch (e) { setMessage(e.message); } }
  useEffect(() => { loadMe(); }, [token]);
  useEffect(() => { if (user) loadComplaints(); }, [user]);
  function logout() { localStorage.removeItem("token"); setToken(""); setUser(null); setView("home"); }
  async function submitAuth(e, register = false) {
    e.preventDefault();
    try {
      const data = await api(register ? "/api/auth/register" : "/api/auth/login", { method: "POST", body: JSON.stringify(register ? auth : { email: auth.email, password: auth.password }) });
      localStorage.setItem("token", data.access_token); setToken(data.access_token); setUser(data.user); setView("dashboard"); setMessage("");
    } catch (e) { setMessage(e.message); }
  }
  async function submitComplaint(e) {
    e.preventDefault();
    try { await api("/api/complaints", { method: "POST", body: JSON.stringify(form) }); setForm({ title:"",description:"",category:"Infrastructure",department:"General",priority:"medium" }); setMessage("Complaint submitted successfully."); setView("dashboard"); loadComplaints(); }
    catch (e) { setMessage(e.message); }
  }
  const statusLabel = s => s.replace("_", " ");
  return <main className="app">
    <nav className="nav"><button className="brand" onClick={() => setView("home")}>Campus<span>Care</span></button><div className="nav-actions">
      {user ? <><button onClick={() => setView("dashboard")}>Dashboard</button><button onClick={() => setView("new")}>New Complaint</button><button onClick={logout}>Logout</button></> : <><button onClick={() => setView("login")}>Login</button><button className="primary" onClick={() => setView("register")}>Register</button></>}
    </div></nav>
    {message && <div className="notice">{message}</div>}
    {view === "home" && <section className="hero"><div><span className="badge">CAMPUS SERVICES</span><h1>Report. Track. Resolve.</h1><p>A digital platform for students to report campus issues and administrators to manage them transparently.</p><div className="actions"><button className="primary large" onClick={() => setView(user ? "new" : "register")}>Submit a Complaint</button><button className="ghost large" onClick={() => setView(user ? "dashboard" : "login")}>Track Complaints</button></div></div><div className="hero-card"><div className="icon">✓</div><h3>One place for every issue</h3><p>Infrastructure, academics, hostel, transport and campus services.</p></div></section>}
    {(view === "login" || view === "register") && <section className="form-page"><div className="form-card"><span className="badge dark">CAMPUSCARE</span><h2>{view === "login" ? "Welcome back" : "Create student account"}</h2><p className="muted">{view === "login" ? "Sign in to track complaints." : "Register to submit and track complaints."}</p><form onSubmit={e => submitAuth(e, view === "register")}>
      {view === "register" && <><label>Name<input required value={auth.name} onChange={e=>setAuth({...auth,name:e.target.value})}/></label><label>Student ID<input value={auth.student_id} onChange={e=>setAuth({...auth,student_id:e.target.value})}/></label><label>Department<input value={auth.department} onChange={e=>setAuth({...auth,department:e.target.value})}/></label></>}
      <label>Email<input type="email" required value={auth.email} onChange={e=>setAuth({...auth,email:e.target.value})}/></label><label>Password<input type="password" required value={auth.password} onChange={e=>setAuth({...auth,password:e.target.value})}/></label><button className="primary full">{view === "login" ? "Login" : "Create Account"}</button></form><button className="link" onClick={() => setView(view === "login" ? "register" : "login")}>{view === "login" ? "Need an account? Register" : "Already registered? Login"}</button></div></section>}
    {view === "new" && <section className="form-page"><div className="form-card wide"><span className="badge dark">NEW COMPLAINT</span><h2>Tell us what happened</h2><form onSubmit={submitComplaint}><label>Complaint title<input required value={form.title} onChange={e=>setForm({...form,title:e.target.value})}/></label><label>Description<textarea required rows="6" value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label><div className="grid2"><label>Category<select value={form.category} onChange={e=>setForm({...form,category:e.target.value})}><option>Infrastructure</option><option>Hostel</option><option>Academics</option><option>Transport</option><option>IT Services</option><option>Other</option></select></label><label>Department<input value={form.department} onChange={e=>setForm({...form,department:e.target.value})}/></label></div><label>Priority<select value={form.priority} onChange={e=>setForm({...form,priority:e.target.value})}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="urgent">Urgent</option></select></label><button className="primary full">Submit Complaint</button></form></div></section>}
    {view === "dashboard" && <section className="dashboard"><div className="dash-head"><div><span className="badge dark">STUDENT DASHBOARD</span><h2>Hello, {user?.name}</h2><p className="muted">Track your submitted complaints.</p></div><button className="primary large" onClick={()=>setView("new")}>+ New Complaint</button></div><div className="stats"><div><b>{complaints.length}</b><span>Total</span></div><div><b>{complaints.filter(c=>c.status==="pending").length}</b><span>Pending</span></div><div><b>{complaints.filter(c=>c.status==="in_progress").length}</b><span>In Progress</span></div><div><b>{complaints.filter(c=>c.status==="resolved").length}</b><span>Resolved</span></div></div><div className="list">{complaints.length === 0 ? <div className="empty">No complaints yet. Submit your first complaint.</div> : complaints.map(c=><article className="complaint" key={c.id}><div><small>#{c.id} · {new Date(c.created_at).toLocaleDateString()}</small><h3>{c.title}</h3><p>{c.description}</p></div><span className={`status ${c.status}`}>{statusLabel(c.status)}</span></article>)}</div></section>}
  </main>;
}
createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
