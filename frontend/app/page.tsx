"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [skills, setSkills] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [gapResults, setGapResults] = useState<any[]>([]);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/resume/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResumeId(data.id);
        setSkills(data.extracted_skills);

        const gapRes = await fetch(`http://127.0.0.1:8000/gap-analysis/${data.id}`);
        const gapData = await gapRes.json();
        setGapResults(gapData.results);
      }
    } catch (err) {
      setError("Could not reach the backend. Is it running?");
    } finally {
      setUploading(false);
    }
  };

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "700px", margin: "0 auto" }}>
      <h1>Career Copilot</h1>
      <p>Upload your resume to see personalized opportunity matches.</p>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload} disabled={!file || uploading} style={{ marginLeft: "1rem" }}>
        {uploading ? "Uploading..." : "Upload Resume"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {resumeId && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Extracted Skills</h2>
          <p>Resume ID: {resumeId}</p>
          <ul>
            {skills.map((skill, i) => (
              <li key={i}>{skill}</li>
            ))}
          </ul>
        </div>
      )}

      {gapResults.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Recommended Opportunities</h2>
          {gapResults.map((opp) => (
            <div
              key={opp.opportunity_id}
              style={{
                border: "1px solid #444",
                borderRadius: "8px",
                padding: "1rem",
                marginBottom: "1rem",
              }}
            >
              <h3>{opp.title} ({opp.type})</h3>
              <p>Match: {opp.match_score}%</p>
              <p>✅ You have: {opp.matched_skills.join(", ") || "none"}</p>
              <p>❌ Missing: {opp.missing_skills.join(", ") || "none"}</p>
              <p>Deadline: {opp.deadline}</p>
              <a href={opp.url} target="_blank" rel="noopener noreferrer">View opportunity</a>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}